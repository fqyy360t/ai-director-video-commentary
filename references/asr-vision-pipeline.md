# ASR And Vision Pipeline

Use this file when implementing the multimodal extraction pipeline.

## Preprocessing

1. Probe video duration, resolution, audio tracks, and frame rate.
2. Extract audio with FFmpeg.
3. Detect scene/shot boundaries.
4. Extract representative frames per scene.
5. Optionally extract short frame sequences for scenes with motion/action.

## ASR

两种引擎可选，由 `task_config.asr_engine` 决定。

### Option A: Local faster-whisper (`asr_engine: "local"`)

用于离线或本地 GPU 环境。模型路径由 `task_config.asr_model_path` 指定。

**Prerequisites:**
- CTranslate2 格式模型目录（含 `model.bin`, `config.json`, `tokenizer.json`, `vocabulary.txt`）
- 默认路径：`D:\models\faster-whisper-medium`
- GPU 模式需要 `cublas64_12.dll` 和 `cudart64_12.dll`（由 `nvidia-cublas-cu12` + `nvidia-cuda-runtime-cu12` pip 包提供）
- 如 DLL 在 `site-packages/nvidia/*/bin/` 但 ctranslate2 找不到，手动复制到 ctranslate2 目录：
  ```bash
  cp site-packages/nvidia/cublas/bin/cublas64_12.dll site-packages/ctranslate2/
  cp site-packages/nvidia/cublas/bin/cublasLt64_12.dll site-packages/ctranslate2/
  cp site-packages/nvidia/cuda_runtime/bin/cudart64_12.dll site-packages/ctranslate2/
  ```
- 如缺少 cublas，自动回退 CPU 模式（`device='cpu', compute_type='int8'`）

**Usage:**
```python
from faster_whisper import WhisperModel
import json

model_path = task_config.get("asr_model_path", r"D:\models\faster-whisper-medium")
device = task_config.get("asr_device", "cuda")

try:
    model = WhisperModel(model_path, device=device, compute_type="float16")
    # Quick test to verify CUDA works
except RuntimeError as e:
    if "cublas" in str(e):
        print("cublas64_12.dll missing, falling back to CPU")
        model = WhisperModel(model_path, device="cpu", compute_type="int8")

segments, info = model.transcribe("audio.wav", language="zh", vad_filter=True)

results = []
for seg in segments:
    results.append({
        "start": round(seg.start, 2),
        "end": round(seg.end, 2),
        "text": seg.text.strip(),
        "confidence": round(seg.avg_logprob, 4)
    })

with open("asr_timeline.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### Option B: Volcengine 火山引擎 (`asr_engine: "volcengine"`)

用于无本地 GPU 或需要更高精度的场景。使用火山引擎录音文件识别 API（异步模式）。

**Prerequisites:**
- `.env` 文件中配置 `VOLCENGINE_API_KEY`
- 音频文件需上传到公网可访问的 URL

**Usage:**
```bash
# 1. Upload audio to a public URL first
# 2. Run the Volcengine transcription script
./volcengine_transcribe.sh <audio_url>

# Output: volcengine_result.json
```

**Python equivalent:**
```python
import requests, json, time

API_KEY = os.getenv("VOLCENGINE_API_KEY")
AUDIO_URL = "<public_audio_url>"

# Submit task
resp = requests.post(
    "https://openspeech.bytedance.com/api/v1/vc/submit",
    params={"language": "zh-CN", "use_itn": "True", "max_lines": "1", "words_per_line": "15"},
    headers={"x-api-key": API_KEY, "content-type": "application/json"},
    json={"url": AUDIO_URL}
)
task_id = resp.json()["id"]

# Poll for result (max 10 min)
for _ in range(120):
    time.sleep(5)
    resp = requests.get(
        "https://openspeech.bytedance.com/api/v1/vc/query",
        params={"id": task_id},
        headers={"x-api-key": API_KEY}
    )
    data = resp.json()
    if data["code"] == 0:
        with open("asr_timeline.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        break
```

**Volcengine response to ASR timeline:**
```python
# Convert Volcengine utterances to standard ASR timeline format
results = []
for utterance in volcengine_result.get("utterances", []):
    results.append({
        "start": round(utterance["start_time"] / 1000, 2),
        "end": round(utterance["end_time"] / 1000, 2),
        "text": utterance["text"].strip(),
        "confidence": utterance.get("confidence", 0.0)
    })
```

```json
{
  "start": 12.34,
  "end": 15.82,
  "text": "What are you hiding from me?",
  "language": "en",
  "confidence": 0.91
}
```

Use ASR for:
- plot understanding
- dialogue information density
- locating spoken reveals
- optional source-dialogue subtitle export

Do not use ASR as the main narration subtitle unless the user explicitly asks for original dialogue subtitles.

## Qwen3-VL-Plus

Use Qwen3-VL-Plus for visual scene summaries:

```json
{
  "scene_id": "scene_0018",
  "visual_summary": "The male lead discovers a forged signature on a contract.",
  "characters": ["male lead", "lawyer"],
  "location": "office",
  "actions": ["reads contract", "points at signature", "freezes in shock"],
  "emotion": "shock",
  "shot_type": "close-up",
  "visual_intensity": 0.86,
  "tags": ["evidence", "fraud", "reversal"]
}
```

Prompt Qwen3-VL-Plus for concrete visible facts first, then interpretation. Keep timestamps attached to the scene being analyzed.

## OCR

OCR is optional, not an MVP blocker.

Enable OCR when:
- content type is `foreign_language_commentary`
- hard subtitles appear in frames
- phone chats, messages, news, contracts, reports, ID cards, medical records, or screen text are important
- genre is `crime`, `high_iq_crime`, `suspense_thriller`, or `mystery_brain_burn`

Do not run expensive full-video OCR by default. Detect likely text regions first, then OCR only those scenes.

## Claude (built-in)

Use Claude (the built-in agent model, no API call needed) after multimodal fusion:
- analyze plot roles
- choose viral formula
- plan scene order
- write narration
- generate Storyboard
- flag low-confidence matches

Claude should consume structured scene summaries, ASR text, OCR text if any, and task configuration. It should not be asked to guess raw visual facts that Qwen3-VL-Plus has not provided.

## Rendering

**Critical rule: `final_preview.mp4` MUST match the storyboard output timeline.** The video duration must equal the SRT duration. Every clip is speed-adjusted so its actual duration equals `output.end - output.start`.

### Output Duration Calculation

每条字幕的 output 时长按以下公式计算，**不是**沿用源视频片段时长：

```python
import re

CHARS_PER_SEC = 4.0   # 中文 TTS 语速
BUFFER_AFTER = 0.1     # 配音结束后的缓冲秒数
MIN_DURATION = 1.0     # 最短保底秒数

def calc_output_duration(sentence: str) -> float:
    # 去标点，只数汉字
    clean = re.sub(r'[，。！？、；：""''——…\-\s\?\!\.\,]', '', sentence)
    char_count = len(clean)
    speech_dur = char_count / CHARS_PER_SEC
    return max(speech_dur + BUFFER_AFTER, MIN_DURATION)
```

### Source Timestamp Shift（源时间戳前移）

渲染前必须执行：每条 clip 的 `source.start` 按该条字幕的 TTS 朗读时长前移。

**公式：** `new_source_start = max(0, source_start - char_count / CHARS_PER_SEC)`

**原理：** 用户在剪映中生成 TTS 配音后，配音占据 clip 前 N 秒（N = 字数÷4）。TTS 播完后原声淡入。如果不前移，淡入时听到的是片段开头的内容，与字幕剧情不对应。前移后，TTS 结束时原声淡入的内容正好是字幕所描述的对话/画面。

```python
for item in timeline:
    char_count = count_chinese_chars(item["sentence"])
    tts_dur = char_count / CHARS_PER_SEC
    src_duration = item["source"]["end"] - item["source"]["start"]
    item["source"]["start"] = max(0.0, item["source"]["start"] - tts_dur)
    item["source"]["end"] = item["source"]["start"] + src_duration
```

### Algorithm

1. **Shift source timestamps** by TTS duration: `source.start -= char_count / 4`
2. For each clip in `storyboard.timeline`:
   a. Extract source range `[source.start, source.end]` from input video
   b. Trim to `output_duration`（使用 `-t output_duration`，不使用源视频完整时长）
   c. Apply audio ducking: TTS 期间原声降至 0.15，结束前 1.5s 线性淡入到 1.0
   d. Save to temp clip file

2. Concat all temp clips (无缝拼接, no gaps) into `final_preview.mp4`

3. **SRT 对齐验证**：用 ffprobe 探测每条实际 clip 时长，用实际时长重新计算 SRT 累积时间戳，确保 `narration_subtitle.srt` 与 `final_preview.mp4` 时间轴一致。

4. 验证：`ffprobe final_preview.mp4` 的总时长应与 SRT 最后一条的 end 时间误差 < 0.5s。

### Python Implementation

```python
import json, subprocess, os

with open("storyboard.json", "r", encoding="utf-8") as f:
    sb = json.load(f)

input_video = sb["task"]["input_video"]
os.makedirs("output/clips", exist_ok=True)

temp_files = []
concat_inputs = []

for i, item in enumerate(sb["timeline"]):
    src = item["source"]
    out = item["output"]
    
    src_dur = src["end"] - src["start"]
    out_dur = out["end"] - out["start"]
    speed = src_dur / out_dur
    
    clip_path = f"output/clips/{item['clip_id']}.mp4"
    temp_files.append(clip_path)
    concat_inputs.append(f"file '{os.path.abspath(clip_path)}'")
    
    # CRITICAL: Use -t (input duration) BEFORE -i, NOT -to.
    # When using -filter_complex with setpts, -to truncates based on
    # source timeline which conflicts with the speed-adjusted output.
    # Instead: -ss for seek, -t for how much input to read.
    src_dur = src["end"] - src["start"]
    
    if abs(speed - 1.0) < 0.01:
        # No speed change needed, just trim
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(src["start"]), "-t", str(src_dur),
            "-i", input_video,
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-c:a", "aac", "-b:a", "128k",
            clip_path
        ]
    else:
        # Speed adjust: setpts for video, atempo for audio
        # atempo range is [0.5, 2.0]; chain multiple if needed
        atempo_parts = []
        remaining = speed
        while remaining > 2.0:
            atempo_parts.append("atempo=2.0")
            remaining /= 2.0
        while remaining < 0.5:
            atempo_parts.append("atempo=0.5")
            remaining /= 0.5
        atempo_parts.append(f"atempo={remaining:.4f}")
        atempo_chain = ",".join(atempo_parts)
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(src["start"]), "-t", str(src_dur),
            "-i", input_video,
            "-filter_complex",
            f"[0:v]setpts={1/speed:.4f}*PTS[v];[0:a]{atempo_chain}[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-c:a", "aac", "-b:a", "128k",
            clip_path
        ]
    
    subprocess.run(cmd, capture_output=True)
    actual_dur = out["end"] - out["start"]
    print(f"{item['clip_id']}: src={src_dur:.1f}s -> out={actual_dur:.1f}s (speed={speed:.2f}x)")

# Concatenate
concat_file = "concat_list.txt"
with open(concat_file, "w", encoding="utf-8") as f:
    f.write("\n".join(concat_inputs))

# Re-encode concat (NOT -c copy) to ensure proper timeline
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_file,
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac", "-b:a", "128k",
    "output/final_preview.mp4"
], capture_output=True)

print(f"final_preview.mp4 rendered, duration should match SRT")
```

### Validation

After rendering, verify:
```bash
# Video duration should match SRT last timestamp
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output/final_preview.mp4
# Compare with last entry in narration_subtitle.srt
```

If durations don't match within 0.5s, re-render.
