---
name: ai-director-video-commentary
description: 搭建一套「AI 影视导演」自动化工作流，可将长视频素材剪辑生成 1–3 分钟的第一人称 / 第三人称影视解说短片。
适用场景：用户需要制作影视剧解说、电影解说、短剧解说、动漫解说、外语影视解说、爆款模板化解说；同时支持视频语义图谱、分镜脚本规划、智能镜头片段筛选、字幕时序匹配，以及导出可直接在剪映中二次编辑的工程素材包。
模型分工推荐方案：
视觉画面解析环节使用通义千问 Qwen3-VL-Plus；
文案逻辑、剧情架构、配音文稿撰写、分镜脚本生成环节使用内置 Claude 大模型。
---

# AI Director Video Commentary

## Overview

Use this skill to design or implement a pipeline that transforms one long video file into a short commentary edit package: a complete preview video, matching narration subtitles, optional split clips, and `storyboard.json`.

The core product principle is: do not cut clips first and force subtitles later. Generate a Video Semantic Graph, use a viral story formula to write narration, bind every narration sentence to source scenes in a Storyboard, then render the video and subtitles from that Storyboard.

## Workflow

1. Collect the task configuration (**所有必填项必须向用户确认，不可自行假设**）：

   **必填项：**
   - **输入视频文件**：用户提供的视频路径
   - **片名**：影视作品名称（用于搜索剧情资料）
   - **剧情梗概 + 主演**：用户描述或由 AI 搜索补充
   - **解说类型**：`第一人称解说` 或 `第三人称解说`（默认第三人称）
   - **影视类型**：`电视剧` / `电影` / `动漫` / `短剧` / `外语解说`（默认电影）
   - **影视题材**：从以下列表选择——超级英雄、动作片、犯罪、高智商犯罪、宫斗、剧情、科幻、科幻灾难、恐怖惊悚、浪漫爱情、励志、奇幻、童话故事、温情感人、喜剧片、悬疑惊悚、悬疑烧脑、灾难、战争、主角复仇

   **有智能默认值的项（仍需告知用户）：**
   - **解说时长**：根据影视类型自动推荐，用户可覆盖
     - 电视剧（长片解说）→ 默认 **5 分钟**
     - 电影 → 默认 **5 分钟**
     - 短剧、漫剧（动漫）→ 默认 **3 分钟**
     - 外语解说 → 默认 **3 分钟**
   - **解说时长可选范围**：1 分钟、2 分钟、3 分钟、5 分钟、8 分钟、10 分钟

   **可选项：**
   - 集数（电视剧时需要）
   - 其他备注

2. Plot research (when video metadata is provided):

   - If the user provides a title, actors, episode number, or any identifying info, search the web for the plot synopsis, character relationships, key turning points, and major twists of that specific content.
   - For a single episode, search for that episode's plot summary specifically.
   - Extract and save: main characters and their goals/motivations, central conflict, emotional arc, key reversals, foreshadowing, and ending.
   - This research becomes the "Director's brief" — it feeds into Step 5 (Story Director) so that the narration is grounded in real plot knowledge rather than only inferred from visual frames.
   - Skip this step only if the user provides no identifying information about the video.

3. **开篇钩子选择（必须）：**

   基于剧情调研结果，生成 **10 个开篇钩子**供用户选择。钩子是解说视频的前 1-2 句话，必须在 3 秒内抓住观众。

   **核心原则：反差越大越好，越无厘头越爆。不要铺垫，上来就炸。**

   **10 个钩子必须覆盖的 4 个方向：**
   - 3 个**反差+爽点**：身份反转、被虐开局、全员打脸（"一个上门女婿，把整个家族掀翻了"）
   - 3 个**无厘头+狗血**：荒诞前提、夸张情绪、标题党（"作者怒了：穿越！必须穿越！让这个废物逆天改命！"）
   - 2 个**悬念+冲突**：信息差、致命一击（"所有人都以为他输了，但没人看到他嘴角的笑"）
   - 1 个**提问型**：不可思议的问题（"赘婿？不好意思，你们全家加起来都不够他玩的"）
   - 1 个**数据+情绪**：数字冲击 + 极端情绪（"被骂了一百次废物，第一千零一次他笑了"）

   **❌ 禁止平淡开头**：不要"从前有个人""这个故事讲的是""今天给大家讲一个"
   **❌ 禁止铺垫**：背景信息放到第二句以后，第一句只管炸

   **展示格式：**
   ```
   === 开篇钩子（请选择 1 个）===
   1. [悬念] "..."
   2. [悬念] "..."
   3. [冲突] "..."
   ...
   10. [数据] "..."

   请选择编号，或告诉我你想用什么样的开头。
   ```

   **用户选定钩子后，该钩子决定整篇解说的情感基调和叙事方向，后续 Step 5-6 的故事板必须围绕这个钩子展开。**

   如用户不满意 10 个选项，可要求重新生成（换风格/换角度/更夸张/更克制），直到满意为止。

4. Build the multimodal timeline:
   
   - Use FFmpeg to extract audio, scenes, and representative frames.
   - Use ASR to create a Dialogue Timeline. Prefer faster-whisper with VAD for the MVP.
   - Use Qwen3-VL-Plus on scene keyframes or short frame sets to create visual summaries, characters, actions, emotions, locations, shot types, and tags.
   - Keep OCR optional. Enable it for foreign-language hard subtitles, phone/chat/news/document screens, crime/suspense/high-IQ crime, or when Qwen3-VL-Plus detects important on-screen text.

5. Fuse timelines into a Video Semantic Graph:
   
   - Do not treat subtitles as the main object.
   - Create scene/event nodes and relationship edges.
   - Preserve source-video timestamps for every node.

6. Use Claude (built-in) as the story director:

   - Analyze plot roles, emotional arcs, hooks, reversals, foreshadowing, key evidence, conflict, and character motivation.
   - If a Director's brief exists from Step 2, use it as the primary plot knowledge source. Cross-reference with the Video Semantic Graph to validate timestamps and identify the most visually impactful moments.
   - **以用户选定的开篇钩子（Step 3）为基调**，整篇解说的情感风格、叙事节奏必须与钩子一致。
   - Select or synthesize a viral formula based on content type, genre, target duration, and point of view.
   - Generate narration. 每句解说词按自然语义断句，不要为凑字数强行拆句。一句话就是一个完整的表达，对应一条字幕。

7. Generate the Storyboard:

   - Bind each narration sentence to one or more semantic scenes/events.
   - Store source timestamps, output timestamps, visual summary, match reason, edit instructions, and subtitle text.
   - **每条字幕的 output 时长 = 配音朗读时长（字数÷4）+ 0.1 秒缓冲，最短 1 秒。**
   - Reject low-confidence visual/text matches instead of forcing a clip.
   - **故事板时间戳验证（生成后必须执行，不可跳过）：**
     1. 将 storyboard 中每条 clip 的 source 时间戳与 `asr_timeline.json` 对话时间线逐条交叉比对
     2. 对每条 clip，查找 source 时间范围内重叠的 ASR 片段，检查对话内容是否与解说词描述的剧情一致
     3. 查找最近的 `vision_analysis.json` 条目（按 source 中位时间匹配），确认视觉分析中的画面描述与解说词匹配
     4. 标记所有不一致项：ASR 对话与解说剧情不符、vision 画面距离 > 15s、ASR 静音区被误用作对话场景
     5. **任何一条 clip 未通过验证，必须修正其 source 时间戳后重新全量验证。不得在存在未修复的不一致项时进入 Step 9 渲染。**

8. **用户确认故事板（必须）：**

   - 生成故事板后，**必须先向用户展示解说内容概览**，等待用户确认后才能进入渲染环节。
   - 展示格式：按"幕"分组，每幕列出标题、字幕条数、时间范围、核心解说词摘要。
   - 同时展示总字幕条数、总时长、平均每条时长。
   - 用户可以：
     - **确认通过** → 进入 Step 9 渲染
     - **要求调整** → 指出哪些部分需要修改（太长/太短/剧情不准/节奏不对），回到 Step 6-7 重新生成故事板
     - **推翻重来** → 回到 Step 5 甚至 Step 3 重新选择钩子
   - **不得跳过此步骤直接渲染。**

9. Render the export package:

   - **源时间戳前移**：渲染前，每条 clip 的 `source.start` 按 `字数 ÷ 4` 秒前移。公式：`new_source_start = max(0, source_start - char_count / 4)`。这样 TTS 配音播完后原声淡入时，听到的内容刚好对应当前字幕描述的剧情。`source.end` 保持与 `source.start` 的原始间距不变。
   - 先逐条渲染独立 clip 到临时目录，然后按顺序无缝拼接成一个完整的 `final_preview.mp4`。
   - 渲染完成后，**必须执行"校验规则"章节中的字幕-视频结束时间校验**。
   - SRT 时间轴必须与 `final_preview.mp4` 实际时长一致（误差 < 0.5s）。如校验失败，用 ffprobe 探测实际 clip 时长重建 SRT，直到校验通过。
   - 不生成 TTS、BGM 或封面，用户默认在剪映中完成。

## Required Output Shape

输出目录分为两层：`pipeline/` 存中间产物，`deliverables/` 存最终交付物。

```text
output/
  pipeline/                     ← 中间产物，供调试和回溯
    directors_brief.md
    asr_timeline.json
    scenes.json
    semantic_blocks.json
    keyframes/
      block_001.jpg ...
    vision_analysis.json
    storyboard.json
  deliverables/                 ← 最终交付物
    final_preview.mp4           ← 完整成片
    narration_subtitle.srt      ← 与成片时间轴完全对齐
```

- `pipeline/storyboard.json` 是 AI 规划与 FFmpeg 渲染之间的契约，保留源视频时间戳和输出时间戳。
- `deliverables/final_preview.mp4` 和 `narration_subtitle.srt` 时间轴必须一致，可直接导入剪映。
- 不生成 TTS、BGM 或封面，用户默认在剪映中完成。

## Model Routing

Use Qwen3-VL-Plus for visual understanding. Use Claude (built-in, no API call needed) for text reasoning, plot analysis, viral formula selection, narration generation, and storyboard planning. Avoid making Qwen3-VL-Plus write the final viral narration, and avoid making Claude infer raw visual details without Qwen3-VL-Plus's scene summaries.

## References

Read only the reference files needed for the current task:

- `references/task-config.md`: input schema, option values, and validation rules.
- `references/semantic-graph.md`: Video Semantic Graph schema and fusion rules.
- `references/viral-formulas.md`: viral narrative formula templates by genre and point of view.
- `references/storyboard-export.md`: Storyboard schema, subtitle matching, output timeline rules, and export package contract.
- `references/asr-vision-pipeline.md`: ASR, Qwen3-VL-Plus, optional OCR, scene detection, and model routing details.
- `references/dependencies.md`: system and Python dependencies for local implementation.

## Scripts

- `scripts/storyboard_to_srt.py`: convert `storyboard.json` into full and optional per-clip SRT files.
- `scripts/validate_storyboard.py`: validate required storyboard fields, monotonic output timestamps, source durations, and subtitle text.

## Implementation Guardrails

- Treat the Storyboard as the contract between AI planning and FFmpeg rendering.
- Always keep both source timeline and output timeline.
- Match narration to semantic scenes/events, not raw subtitle timestamps.
- Use ASR primarily as Dialogue Timeline for understanding and matching; the main exported subtitle is the generated narration subtitle.
- Keep OCR as an optional enhancement, not an MVP blocker.
- Prefer complete preview video plus complete SRT as the main handoff to CapCut.
- Keep split clips as optional editing material.
- When confidence is low, emit review flags in `storyboard.json` instead of silently producing mismatched clips.

## 校验规则（渲染后必须执行）

渲染完成后，**必须执行以下校验**，校验通过才能交付给用户：

### 1. 字幕-视频结束时间校验

```
步骤：
1. ffprobe 探测 final_preview.mp4 的实际时长 → video_dur
2. 读取 SRT 最后一条的 end 时间戳 → srt_end
3. 计算 diff = |video_dur - srt_end|
4. 如果 diff > 0.5s → 校验失败，必须修复后重新校验
```

### 2. 修复流程（校验失败时）

```
1. 用 ffprobe 逐条探测 deliverables/clips/ 中每个 clip 的实际时长
2. 用实际时长重新计算 SRT 累积时间戳（纯累加，不加间隔）
3. 重新保存 narration_subtitle.srt
4. 重新执行校验步骤 1
```

### 3. 校验报告格式

校验完成后，输出以下信息：
```
=== 校验报告 ===
视频时长:    XXX.XXXs (X.Xmin)
字幕末尾:    XXX.XXXs
差值:        X.XXXs
字幕条数:    XX 条
状态:        ✓ 通过 / ✗ 失败
```

## 字幕画面匹配校对（交付后用户反馈不匹配时执行）

当用户反馈"字幕和画面对不上"时，说明故事板中的 source 时间戳与实际画面内容不一致。**根本原因**是生成故事板时 time-stamping 基于猜测而非 ASR 对话验证。必须执行以下系统性校对流程：

### 校对步骤

```
1. 读取 asr_timeline.json（ASR 对话时间线）作为绝对时间参照
2. 对 storyboard 中每条 clip，交叉比对：
   a. 查找 source 时间范围内重叠的 ASR 片段
   b. 检查 ASR 对话内容是否与解说词描述的剧情一致
   c. 查找最近的 vision_analysis 条目（按 source 中位时间匹配）
   d. 评估 vision 画面描述是否与解说词语义匹配
3. 标记所有不匹配的 clip，列出：clip_id、当前时间戳、ASR 实际内容、vision 实际画面、问题类型
4. 基于 ASR 时间线全文（按 30s 分块打印完整对话），逐条重新确定每条解说词的正确 source 时间戳
5. 用修正后的时间戳完全重建 storyboard.json
6. 重新渲染所有 clip → 拼接 → 生成 SRT → 校验
```

### 时间戳修正原则

- **ASR 对话是时间戳的绝对参照**：任何描述对话场景的解说词，source 时间戳必须在对应 ASR 片段的起止范围内
- **vision_analysis 是二级验证**：确认画面内容与解说词描述一致
- **收紧 source 窗口**：每条 clip 的 source 时长控制在 6-30s，避免过高倍速
- **速度比控制**：source_duration / output_duration 尽量 < 4x，极端情况下 < 6x
- **不使用 ASR 静音区来描述对话场景**：如果 source 范围内无 ASR 片段，解说词不应描述对话

### 修正后必须重新校验

修正并重新渲染后，必须执行"校验规则"章节中的完整校验流程（视频-SRT 对齐），校验通过才能再次交付。

## BGM 推荐（交付后可选）

用户交付后可能要求推荐 BGM。按影片题材和情绪结构推荐三段式配乐，优先推荐剪映曲库内可直接搜索到的曲目。

### 推荐原则

- **三段式结构**：对应解说的 Hook→发展→收尾 三个情绪段，各推荐不同风格
- **优先剪映内置曲库**：推荐曲名在剪映「音频 → 音乐库」可直接搜索到
- **每段给 2-3 首备选**：用户可能找不到某首，给替代方案
- **给出关键踩点时间**：标注 BGM 切换点在解说时间轴上的位置

### 按题材的常用 BGM 速查表

| 题材 | 第一段（Hook/铺垫） | 第二段（冲突/逆转） | 第三段（释放/收尾） |
|------|-------------------|-------------------|-------------------|
| 古装/奇幻/穿越 | Breath and Life、幻昼、Not One | Time Back、踏山河、How on Make | A Little Story、骁、Windy Hill |
| 悬疑/犯罪/烧脑 | Intro-The XX、幻昼 | Die Weck、Lord、Void | River Flows In You、风居住的街道 |
| 喜剧/轻喜剧 | Sunny Day、小城夏天 | Time Back、Oops、布谷鸟 | Valder Fields、A Little Story |
| 动作/战争/超级英雄 | Breath and Life、Intro | How on Make、踏山河、Wild | Faded、平凡之路 |
| 温情/励志/浪漫 | 幻昼、夜的钢琴曲五 | A Little Story、River Flows In You | 所念皆星河、Windy Hill |
| 恐怖/惊悚 | 幻昼、悬疑氛围 | Void、Disaster | 风居住的街道 |

### 推荐格式

交付 BGM 推荐时，按以下格式输出：

```
## BGM 推荐

### 第一段：Hook + 铺垫（0~Xs）
> 情绪方向

| 曲名 | 风格 | 剪映搜索 |
|------|------|---------|
| xxx | xxx | 搜 xxx |

...（三段）

### 省事方案：只用一首
推荐一首通用 BGM

### 关键踩点提示
- Xs（叙事转折点）→ 切下一段 BGM
```

### 文言文/古风类搜索技巧

古风剧（宫斗、奇幻、武侠等）在剪映中可额外使用以下中文关键词搜索：
- `古风` `国潮` `江湖` `武侠` `中国风`
- `搞笑古风` `轻喜剧`（古装喜剧类）
- `逆袭` `燃向` `热血`（爽剧高潮段落）

## Minimal Acceptance Criteria

- `pipeline/storyboard.json` 包含完整的故事板数据（源时间戳 + 输出时间戳 + 匹配理由）。
- `deliverables/final_preview.mp4` 是完整成片，所有片段无缝拼接。
- `deliverables/narration_subtitle.srt` 时间轴与 `final_preview.mp4` 实际时长完全一致（误差 < 0.5s）。
- 每条字幕按自然语义断句（一句话 = 一条字幕），时长 = 字数÷4 + 0.1s 缓冲，最短 1s。
- 故事板生成后必须经用户确认，确认后才渲染 deliverables。
- 输出可直接在剪映中导入使用，用于后续 TTS 配音、BGM、封面和精修。
