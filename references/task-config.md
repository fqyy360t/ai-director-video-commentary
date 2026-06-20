# Task Configuration

Use this schema to capture the user's creative direction before analysis or rendering.

## Input Schema

```json
{
  "input_video": "source.mp4",
  "title": "赘婿",
  "actors": ["郭麒麟", "宋轶"],
  "episode": 1,
  "plot_summary": "赘婿第一集...",
  "narration_pov": "third_person",
  "content_type": "tv_drama",
  "genre": "comedy",
  "target_duration": 300,
  "buffer_after_speech": 0.1,
  "min_duration": 1.0,
  "asr_engine": "local",
  "asr_model_path": "D:\\models\\faster-whisper-medium",
  "asr_device": "cuda"
}
```

`asr_engine`:
- `local`: use local faster-whisper model. Requires `model_path` pointing to a CTranslate2 model directory (e.g. `D:\models\faster-whisper-medium`).
- `volcengine`: use Volcengine (火山引擎) 录音文件识别 API. Requires `VOLCENGINE_API_KEY` in `.env`. Audio file is uploaded to a public URL first, then submitted to the async API. Uses the `volcengine_transcribe.sh`.

## Allowed Values

`title`（**必填**）：影视作品名称。触发剧情搜索，产出 Director's brief。

`actors`（**必填**）：主演名单，数组格式。

`episode`（选填）：电视剧/动漫的集数。

`plot_summary`（选填）：用户提供的剧情梗概。如未提供，由 AI 搜索补充。

`narration_pov`（**必填**）：
- `first_person`：第一人称沉浸式解说
- `third_person`：第三人称解说频道风格（默认）

`content_type`（**必填**）：
- `movie`：电影
- `tv_drama`：电视剧
- `anime`：动漫/漫剧
- `short_drama`：短剧
- `foreign_language_commentary`：外语解说

`genre`（**必填**）：
- `superhero`：超级英雄
- `action`：动作片
- `crime`：犯罪
- `high_iq_crime`：高智商犯罪
- `palace_intrigue`：宫斗
- `drama`：剧情
- `sci_fi`：科幻
- `sci_fi_disaster`：科幻灾难
- `horror_thriller`：恐怖惊悚
- `romance`：浪漫爱情
- `inspirational`：励志
- `fantasy`：奇幻
- `fairy_tale`：童话故事
- `warm_emotional`：温情感人
- `comedy`：喜剧片
- `suspense_thriller`：悬疑惊悚
- `mystery_brain_burn`：悬疑烧脑
- `disaster`：灾难
- `war`：战争
- `revenge`：主角复仇

`target_duration`（**必填**，有智能默认）：
- 电视剧 → 默认 **300 秒**（5 分钟）
- 短剧、动漫 → 默认 **180 秒**（3 分钟）
- 电影 → 默认 **180 秒**（3 分钟）
- 外语解说 → 默认 **180 秒**（3 分钟）
- 用户可选范围：60、120、180、300、480、600 秒

`buffer_after_speech`：配音朗读结束后的缓冲秒数。**默认 0.1 秒。** 每条字幕的 output 时长 = 字数÷4 + buffer_after_speech，最短 1 秒。

`min_duration`：clip 最短保底时长。**默认 1.0 秒。**

## Defaults

- `narration_pov`: `third_person`
- `content_type`: 需用户确认，不可自行假设
- `genre`: 需用户确认，不可自行假设
- `target_duration`: 根据 content_type 智能推荐
  - `tv_drama` → 300s（5分钟）
  - `movie` → 300s（5分钟）
  - `short_drama` / `anime` → 180s（3分钟）
  - `foreign_language_commentary` → 180s（3分钟）
- `buffer_after_speech`: 0.1
- `min_duration`: 1.0
- `asr_engine`: `local`
- `asr_model_path`: `D:\models\faster-whisper-medium`
- `asr_device`: `cuda`（如 cublas64_12.dll 缺失则自动回退 `cpu`）

## Validation

**启动前必须确认以下必填项**，缺任何一项都不可开始渲染：
1. `input_video` — 视频文件路径存在
2. `title` — 片名已知
3. `narration_pov` — 解说类型已确认
4. `content_type` — 影视类型已确认
5. `genre` — 影视题材已确认
6. `target_duration` — 解说时长已确认（或已告知用户智能默认值并获得同意）

ASR 引擎验证：
- `asr_engine` 为 `local` 时，验证 `asr_model_path` 目录包含 `model.bin`, `config.json`, `tokenizer.json`, `vocabulary.txt`
- 如 `asr_device` 为 `cuda` 但 `cublas64_12.dll` 缺失，自动回退 `cpu` + `compute_type=int8`
