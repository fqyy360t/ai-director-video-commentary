# Storyboard And Export

The Storyboard is the binding contract between generated narration and rendered video. It determines which source clip appears when each narration subtitle is on screen.

## Storyboard Schema

```json
{
  "task": {
    "input_video": "source.mp4",
    "target_duration": 120,
    "narration_pov": "third_person",
    "content_type": "movie",
    "genre": "high_iq_crime"
  },
  "timeline": [
    {
      "clip_id": "clip_001",
      "sentence_id": "sent_001",
      "sentence": "The man never imagined the safest room in the bank was actually the trap.",
      "source": {
        "scene_ids": ["scene_0042"],
        "start": 4810.0,
        "end": 4818.0
      },
      "output": {
        "start": 0.0,
        "end": 8.0
      },
      "visual_summary": "The protagonist steps into the vault and the door locks behind him.",
      "match_reason": "The narration describes a trap, and the selected scene visually shows the vault door locking.",
      "match_score": 0.91,
      "edit": {
        "crop": "9:16_center",
        "speed": 1.0,
        "original_audio": "duck",
        "transition": "cut"
      },
      "review_flags": []
    }
  ]
}
```

## Subtitle Rules

The main subtitle is narration, not original dialogue.

Generate `narration_subtitle.srt` from `timeline[].sentence` and `timeline[].output`.

### 字幕断句规则

**按自然语义断句：一句话 = 一条字幕。** 不要为凑字数强行拆句，也不要为省字数强行合并。

原则：
- 一句话表达一个完整的语义，对应一条字幕和一个 clip
- 不要在词组中间切开（如"苏家的/大小姐"应为一条，不是两条）
- 复合句可以按逗号拆分为独立的短句，前提是每句语义完整
- 句子长短自然即可，重要的是 TTS 读起来流畅不断句

### 片段时长规则

**每条字幕对应的输出时长 = 配音朗读时长 + 0.1 秒缓冲。**

- 配音朗读时长估算：汉字数 ÷ 4 字/秒（中文 TTS 语速）
- 缓冲时间（默认 0.1 秒）：配音结束后仅留极短间隔，保持 TTS 音频紧凑连贯
- 最短时长保底：1 秒（防止超短字幕一闪而过）

示例：
```
字幕："商战小说没人看了，编辑让他改写喜剧。"（16字）
配音时长：16 ÷ 4 = 4.0s
输出时长：4.0 + 0.1 = 4.1s
```

### Narration Quality Standards

### Narration Quality Standards

写解说词时对照以下检查项。每一项不合格就打回重写：

| 检查项 | 要求 | 失败症状 |
|--------|------|----------|
| **因果链** | 每两句之间用"所以/但是"连接，禁止"然后" | 流水账，看完没感觉 |
| **在乎主角** | 前 2 句内让观众知道为什么要在乎主角 | "这人跟我有什么关系？" |
| **升级感** | 每一段比前一段更严重/更深入/更紧张 | 冲突重复，观众疲了 |
| **情感注入** | 不只是"发生了什么"，还有"这让人感觉如何" | 像新闻播报 |
| **释放点** | 最后 3 句给观众一个情绪出口 | 结尾平淡收场 |

### Narration Self-Check (每次写完后执行)

```
1. 逐句标记连接词：然后 / 所以 / 但是
2. "然后"出现 > 2 次 → 重写因果链
3. 前 2 句里有让观众"在乎主角"的信息吗？没有 → 加
4. 冲突在升级还是在重复？重复 → 引入更深层阻碍（外部→个人→内心）
5. 最后 3 句是情绪出口还是流水账收尾？流水账 → 加重情感释放
```

Source-dialogue subtitles are optional. If exporting them, remap ASR times:

```text
output_start = source_dialogue_start - clip_source_start + clip_output_start
output_end = source_dialogue_end - clip_source_start + clip_output_start
```

## Matching Rules

**匹配不仅是"画面跟文字对上"，更是"画面服务于叙事节拍"。**

Every clip must serve the narrative beat it belongs to. Don't just find any scene that vaguely matches the words — find the scene that delivers the EMOTION of that beat.

| 节拍类型 | 画面要求 | 例子 |
|----------|---------|------|
| Hook | 视觉冲突/反常/强情绪 | 背叛、爆炸、哭泣、揭露 |
| 角色介绍 | 展现主角特质（救猫咪/欲望/能力） | 善举、专注、孤独 |
| 阻碍升级 | 越来越强的对抗画面 | 被赶出→被追杀→被最爱的人背叛 |
| 代价/低谷 | 丧失的具象化 | 空房间、离去背影、手中掉落之物 |
| 释放/结局 | 情绪出口 | 微笑、拥抱、日出、转身离开 |

Strong matches:
- death, betrayal, fight, chase, explosion, crying, key evidence, confession, reveal, identity reversal.

Medium matches:
- character setup, relationship setup, preparation, travel, investigation, emotional transition.

Weak matches:
- landscape, atmosphere, room tone, filler reaction, neutral walking.

**Do not use weak matches for plot-critical narration** unless no better visual exists and the Storyboard marks a review flag.

**New rule: Every clip's `match_reason` must explain WHY this scene serves the narrative beat, not just WHAT it shows.**

## Output Timeline

The rendered final preview has a new timeline. Source timestamps are only references.

每条字幕的 output 时长由字幕长度规则自动计算（见上方），各 clip 之间无缝拼接。

Example:

```text
字幕A（8字）：配音2.0s + 缓冲2s = 4.0s
  source clip A: 01:20:10 - 01:20:14
  output clip A: 00:00:00 - 00:00:04

字幕B（10字）：配音2.5s + 缓冲2s = 4.5s
  source clip B: 00:35:05 - 00:35:09.5
  output clip B: 00:00:04 - 00:00:08.5
```

All exported subtitles must use output time.

## Export Package

输出分两层：`pipeline/` 存中间产物，`deliverables/` 存最终交付物。两者互不覆盖。

```text
output/
  pipeline/                     ← 中间产物（调试/回溯用）
    directors_brief.md
    asr_timeline.json
    scenes.json
    semantic_blocks.json
    keyframes/
    vision_analysis.json
    storyboard.json
  deliverables/                 ← 最终交付物
    final_preview.mp4           ← 完整成片（所有片段无缝拼接）
    narration_subtitle.srt      ← 与成片时间轴完全对齐
```

- 所有片段按顺序无缝拼接为 `final_preview.mp4`。
- SRT 时间轴必须与 `final_preview.mp4` 实际时长一致（误差 < 0.5s）。
- 不导出 TTS、BGM 或封面，除非用户明确要求。

### 渲染后校验（必须执行）

渲染完成后，必须执行以下校验，通过后才能交付：

1. `ffprobe` 探测 `final_preview.mp4` 实际时长 → `video_dur`
2. 读取 SRT 最后一条 end 时间戳 → `srt_end`
3. `diff = |video_dur - srt_end|`，必须 < 0.5s
4. 如失败：用 ffprobe 逐条探测 clip 实际时长，用实际时长纯累加重建 SRT，重新校验

校验报告格式：
```
=== 校验报告 ===
视频时长:    XXX.XXXs (X.Xmin)
字幕末尾:    XXX.XXXs
差值:        X.XXXs
字幕条数:    XX 条
状态:        ✓ 通过 / ✗ 失败
```
