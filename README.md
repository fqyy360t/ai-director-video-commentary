# 🎬 AI Director Video Commentary

> Turn a 40-minute episode into a 5-minute viral commentary. AI-powered, fully automated.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange)](https://claude.ai/code)
[![中文文档](https://img.shields.io/badge/文档-中文-red.svg)](README_CN.md)

---

**Language:** [English](#) | [中文](README_CN.md)

---

## What Is This

Feed it a long video of any TV episode or movie. It automatically handles: plot research → multimodal semantic analysis → viral narration writing → storyboard planning → FFmpeg rendering → SRT subtitle export. The final deliverable is a complete commentary video ready for CapCut (Jianying) TTS dubbing, BGM, and cover art.

**Core principle:** Don't cut clips first and force subtitles later. Generate a Video Semantic Graph → write narration → bind to source scenes in a Storyboard → render everything from that contract.

## Demo

Input: `赘婿` (My Heroic Husband) Episode 1 — 40 minutes  
Output: 5-minute commentary + 50 subtitles

```
=== Validation Report ===
Video duration:    272.694s (4.5min)
SRT last end:      272.628s
Difference:        0.066s
Subtitle count:    50
Status:            ✓ PASS
```

## Architecture

```
User Input (video + title + actors + genre + duration)
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 1-2  Task Config + Plot Research           │
│            Output: Director's Brief              │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 3     Multimodal Timeline                  │
│             FFmpeg audio/video extraction        │
│             faster-whisper ASR                   │
│             PySceneDetect scene detection        │
│             Qwen3-VL-Plus vision analysis        │
│             Output: asr_timeline.json            │
│                     vision_analysis.json          │
│                     scenes.json                   │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 4     Video Semantic Graph Fusion          │
│             Scene/event/character nodes + edges  │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 5-6   Claude Story Director + Storyboard   │
│             Viral formula → narration            │
│             ASR timestamp verification (MUST)    │
│             Output: storyboard.json              │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 7     User Confirmation (MUST)             │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 8     FFmpeg Render + Concat + SRT         │
│             Validate: video-SRT diff < 0.5s      │
│             Output: final_preview.mp4            │
│                     narration_subtitle.srt        │
└──────────────────────────────────────────────────┘
```

## Model Routing

| Task | Model | Notes |
|------|-------|-------|
| Visual scene analysis | **Qwen3-VL-Plus** (DashScope) | Character, emotion, action, location per frame |
| Speech recognition | **faster-whisper** (local) | CTranslate2 model, CUDA/CPU auto-switch |
| Narration, plot analysis, storyboard | **Claude** (built-in) | No external API call required |

## Prerequisites

### System Tools
- **FFmpeg** 4.0+ — video encode/decode, concat
- **Python** 3.10+

### Python Packages
```bash
pip install faster-whisper scenedetect opencv-python openai python-dotenv srt
```

### ASR Model
Download the CTranslate2 Whisper model to `D:\models\faster-whisper-medium\`:

```bash
huggingface-cli download Systran/faster-whisper-medium --local-dir D:\models\faster-whisper-medium
```

Required files (1.5 GB total):
```
model.bin         ← core model
config.json       ← model config
tokenizer.json    ← tokenizer
vocabulary.txt    ← vocabulary
```

> 💡 **GPU Acceleration:** NVIDIA GPU auto-detected via CUDA. Install `nvidia-cublas-cu12` for GPU support. Falls back to CPU automatically if DLLs are missing.

### Vision Model API
Create a `.env` file in your working directory:

```env
QWEN_API_ENDPOINT=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
QWEN_VL_MODEL=qwen3-vl-plus
```

> 🔑 Get your key from [DashScope Console](https://dashscope.console.aliyun.com/).

## Operation Guide

> Total: 5 steps. ~5 minutes of human time, ~15-25 minutes of AI runtime.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Step 1  │    │  Step 2  │    │  Step 3  │    │  Step 4  │    │  Step 5  │
│  Install │───▶│  Setup   │───▶│  Input   │───▶│  AI Run  │───▶│  Export  │
│  1 min   │    │  15 min  │    │  2 min   │    │ 15-25 min│    │  5 min   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

### Step 1: Install the Skill

> 🎯 One-time setup. Register this Skill with Claude Code.

**Option A: Marketplace (recommended)**
```
/install ai-director-video-commentary
```

**Option B: Manual git clone**
```bash
# Windows
git clone <repo-url> %USERPROFILE%\.claude\skills\ai-director-video-commentary

# macOS / Linux
git clone <repo-url> ~/.claude/skills/ai-director-video-commentary
```

Restart Claude Code or run `/reload`.  
**Verify:** Type `/ai` then press Tab — you should see `ai-director-video-commentary` in the completion list.

---

### Step 2: Configure the Environment

> 🎯 One-time setup. Get all dependencies running locally.

#### 2.1 System Dependencies

| Tool | Version | Purpose | Windows |
|------|---------|---------|---------|
| **FFmpeg** | 4.0+ | Audio/video extraction, speed change, concat | `winget install ffmpeg` |
| **Python** | 3.10+ | All pipeline scripts | `winget install python` |

Verify:
```bash
ffmpeg -version
python --version   # should be 3.10+
```

#### 2.2 Python Dependencies
```bash
pip install faster-whisper scenedetect opencv-python openai python-dotenv srt
```

Verify:
```bash
python -c "import faster_whisper; import scenedetect; import cv2; import openai; print('OK')"
```

#### 2.3 ASR Model (~1.5 GB)
```bash
huggingface-cli download Systran/faster-whisper-medium --local-dir D:\models\faster-whisper-medium
```

Or manually download from [HuggingFace](https://huggingface.co/Systran/faster-whisper-medium):
```
D:\models\faster-whisper-medium\
├── model.bin
├── config.json
├── tokenizer.json
└── vocabulary.txt
```

#### 2.4 Vision API Key
Create `.env` in your working directory:
```env
QWEN_API_ENDPOINT=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
QWEN_VL_MODEL=qwen3-vl-plus
```

#### ✅ Readiness Checklist
```
[ ] ffmpeg --version passes
[ ] python --version shows 3.10+
[ ] python -c "import faster_whisper" passes
[ ] D:\models\faster-whisper-medium\model.bin exists
[ ] .env contains QWEN_API_KEY
```

---

### Step 3: Provide Video & Metadata

> 🎯 Tell the AI what you're working with and what you want.

#### 3.1 Launch the Skill
```
/ai-director-video-commentary C:\path\to\your\video.mp4
```

#### 3.2 Answer Configuration Prompts

The AI will ask 8 questions. Answer each one:

| # | AI asks | How to answer | Example |
|---|---------|---------------|---------|
| ① | Title? | Full show/movie name | `My Heroic Husband` |
| ② | Lead actors? | Comma-separated | `Guo Qilin, Song Yi` |
| ③ | Content type? | Pick one from list | `TV Drama` |
| ④ | Genre? | Pick one from 20 options | `Fantasy` |
| ⑤ | Narration POV? | First-person or Third-person | `Third-person` |
| ⑥ | Target duration? | 1/2/3/5/8/10 minutes | `5 minutes` |
| ⑦ | Episode number? | TV/anime only | `Episode 1` |
| ⑧ | Plot summary? | Paste or hit Enter to skip | (Optional) |

#### 📋 Example Conversation
```
User: /ai-director-video-commentary C:\video\S01E01.mp4

AI:   What's the title?
User: My Heroic Husband

AI:   Lead actors?
User: Guo Qilin, Song Yi

AI:   Content type? (TV drama / Movie / Anime / Short drama / Foreign)
User: TV drama

AI:   Genre? (20 options available)
User: Fantasy

AI:   Narration POV? (First-person / Third-person, default third)
User: Third-person

AI:   Target duration? (1/2/3/5/8/10 min, TV drama defaults to 5 min)
User: 5 minutes

AI:   Episode number?
User: Episode 1

AI:   Plot summary? (press Enter to let me search)
User: (presses Enter)

AI:   Configuration confirmed. Starting pipeline...
```

> 💡 **Defaults:** TV dramas → 5 min | Movies → 5 min | Short drama / Anime → 3 min | Foreign → 3 min.

---

### Step 4: AI Narration Generation

> 🎯 The AI does all the heavy lifting. One confirmation checkpoint.

#### 4.1 Automated Pipeline

| Stage | What happens | Duration | Output |
|-------|-------------|----------|--------|
| 🔍 Plot Research | Web search for plot, characters, twists | ~30s | `directors_brief.md` |
| 🎤 ASR | Extract audio → transcribe all dialogue | ~5-10min | `asr_timeline.json` (~690 segments) |
| 🎬 Scene Detection | PySceneDetect → extract keyframes | ~2min | `scenes.json` + 200+ frames |
| 👁️ Vision Analysis | Qwen3-VL-Plus per-frame analysis | ~5-10min | `vision_analysis.json` |
| ✍️ Narration + Storyboard | Claude: viral formula → script → scene binding | ~2min | `storyboard.json` |

> Progress is displayed live in the conversation.

#### 4.2 ⚠️ Storyboard Confirmation (Required)

Before rendering, the AI shows a summary and **waits for your approval**:

```
📋 Storyboard Summary: My Heroic Husband Ep.1 · 5-min Commentary

────────────────────────────────────────────
Overview
────────────────────────────────────────────
Subtitles:     50
Total duration: 272s (4 min 32s)
Average:       5.4s per subtitle

────────────────────────────────────────────
Act 1: Hook + Setup (0~57s, 11 lines)
────────────────────────────────────────────
Author pressured by editor → Protagonist betrayed →
Author refuses to give up → Time-travel decision

────────────────────────────────────────────
Act 2: Conflict & Reversal (57~200s, 24 lines)
────────────────────────────────────────────
Wake up in ancient China → Mistaken bride →
Family conspiracy → Courtroom showdown → Victory

────────────────────────────────────────────
Act 3: Transformation (200~272s, 15 lines)
────────────────────────────────────────────
Contract marriage → Wedding day humiliation →
"Being a live-in son-in-law is not the end. It's the beginning."
```

Your options:

| Action | Say | What happens |
|--------|-----|-------------|
| ✅ Approve | `OK` / `Approve` | Move to Step 5 rendering |
| 🔧 Revise | `Act 2 is too long, trim it` | AI rewrites, re-presents |
| 🔄 Redo | `Start over` | Back to plot analysis |

> ⚠️ **Rendering will NOT start until you confirm.** This is the final quality gate.

---

### Step 5: Export & Final Cut

> 🎯 Get the deliverable into CapCut and add finishing touches.

#### 5.1 AI Render + Validate

After confirmation, fully automatic (~3-5 min):

```
[1/4] Rendering 50 clips (with speed adjustment)...
      clip_001 OK (src=5.5s -> out=4.6s, speed=1.2x)
      clip_002 OK (src=9.0s -> out=5.9s, speed=1.5x)
      ...
[2/4] Concatenating into final_preview.mp4...
[3/4] Generating narration_subtitle.srt...
[4/4] Running validation...

=== Validation Report ===
Video duration:    272.694s (4.5min)
SRT last end:      272.628s
Difference:        0.066s
Subtitle count:    50
Status:            ✓ PASS
```

> If validation fails (diff > 0.5s), the AI auto-probes actual clip durations and rebuilds the SRT until it passes.

#### 5.2 Get Your Files

```
📁 output/
├── 📁 pipeline/                    ← Intermediate artifacts (debugging)
│   ├── directors_brief.md
│   ├── asr_timeline.json
│   ├── scenes.json
│   ├── vision_analysis.json
│   ├── storyboard.json
│   └── keyframes/
└── 📁 deliverables/                ← ⭐ Final output
    ├── 🎬 final_preview.mp4         ← Complete commentary video
    └── 📝 narration_subtitle.srt    ← Narration subtitles (timecode-aligned)
```

#### 5.3 CapCut Post-Production (5 min)

| Step | Action | Detail |
|------|--------|--------|
| **① Import video** | Drag `final_preview.mp4` into CapCut | Main track |
| **② Import subtitles** | Drag `narration_subtitle.srt` into subtitle track | Auto timecode-aligned |
| **③ TTS dubbing** | Select all subtitles → Text-to-Speech | Recommend "Commentary Male" voice |
| **④ Add BGM** | Audio → Music → Search AI-recommended tracks | Volume 20-30% |
| **⑤ Fine-tune** | Check key scenes, adjust clip boundaries if needed | See beat timestamps from AI |
| **⑥ Export** | 1080p / 30fps / H.264 | Bitrate 8-16 Mbps recommended |

#### 5.4 BGM Quick Reference

| Section | Recommended Tracks | Search in CapCut |
|---------|-------------------|------------------|
| Hook/Setup | `Breath and Life` `Illusionary Daytime` | Search track name |
| Conflict/Reversal | `Time Back` `踏山河` | Search track name |
| Resolution/Ending | `A Little Story` `骁` | Search track name |

> 🎯 **Lazy mode:** Just use `Time Back` throughout — the Swiss Army knife of commentary BGM.

---

## FAQ

<details>
<summary><b>Q: Subtitles don't match the video?</b></summary>

Tell the AI: **"The subtitles don't match the video, fix it."**

The AI will run a systematic audit:
1. Cross-reference every clip's source timestamp against `asr_timeline.json`
2. Flag all mismatches (wrong dialogue, wrong scene, silence used as dialogue)
3. Print the full ASR transcript in 30s chunks to find correct timestamps
4. Rebuild `storyboard.json` with verified timestamps
5. Re-render → re-validate → re-deliver
</details>

<details>
<summary><b>Q: Don't like the narration style?</b></summary>

At Step 4's storyboard confirmation, just ask:
- `Make it more punchy, shorter sentences`
- `Switch to first-person perspective`
- `Cut it down to 3 minutes`

The AI rewrites and shows the updated storyboard.
</details>

<details>
<summary><b>Q: No NVIDIA GPU — still works?</b></summary>

Yes. ASR auto-falls back to CPU (`device=cpu, compute_type=int8`). ASR takes ~15 min instead of ~5 min. Everything else is unaffected.
</details>

<details>
<summary><b>Q: Batch processing multiple episodes?</b></summary>

Run the Skill once per episode:
1. Name files consistently (`S01E01.mp4`, `S01E02.mp4`, ...)
2. Call `/ai-director-video-commentary` for each
3. Environment and model are already set up — subsequent episodes are faster to configure
</details>

## Configuration Reference

| Setting | Required | Options |
|---------|----------|---------|
| Input video | ✓ | Local mp4 path |
| Title | ✓ | Any show/movie name |
| Lead actors | ✓ | Array format |
| Narration POV | ✓ | `first_person` / `third_person` |
| Content type | ✓ | `tv_drama` / `movie` / `anime` / `short_drama` / `foreign` |
| Genre | ✓ | 20 genres (see task-config.md) |
| Duration | ✓ | 60 / 120 / 180 / 300 / 480 / 600 seconds |
| Episode | Optional | For TV/anime |

## Output Structure

```
output/
├── pipeline/                     # Intermediate artifacts (debugging)
│   ├── directors_brief.md        # Director's brief
│   ├── asr_timeline.json         # ASR dialogue timeline
│   ├── scenes.json               # Scene detection
│   ├── semantic_blocks.json      # Semantic blocks
│   ├── vision_analysis.json      # Vision analysis
│   ├── storyboard.json           # Storyboard (source + output timestamps)
│   └── keyframes/                # Keyframe images
└── deliverables/                 # Final output
    ├── final_preview.mp4         # Complete video
    └── narration_subtitle.srt    # Subtitle (aligned to video)
```

## Subtitle Rules

- Natural semantic segmentation: one sentence = one subtitle
- Subtitle duration = character count ÷ 4 + 0.1s buffer (min 1s)
- SRT timecode must match video duration within 0.5s (enforced)

## Quality Assurance

### Pre-Render: Storyboard Timestamp Verification
Every clip's source timestamp is cross-referenced against the ASR dialogue timeline before rendering. Mismatched clips are rejected and must be corrected.

### Post-Render: Video-SRT Alignment Check
```python
diff = |ffprobe_video_duration - srt_last_end|
assert diff < 0.5  # auto-fix if failed
```

### Post-Delivery: Subtitle-Video Audit
If the user reports subtitle mismatches, the AI runs a full audit using ASR as ground truth to rebuild all timestamps.

## Viral Story Formulas

Built-in narrative templates auto-selected by content type and duration:

| Duration | Structure | Narration Lines |
|----------|-----------|----------------|
| 60-90s | Harmon 8-Step | 12-16 lines |
| 90-180s | Harmon + Three-Act | 18-28 lines |
| 3-15 min | Three-Act | 28-50 lines |

ABCD Causality Check: "And then" = laundry list. "Therefore / But" = story.

## BGM Recommendation

Post-delivery, the AI recommends 3-section BGM based on genre:

| Genre | Hook/Setup | Conflict/Reversal | Resolution |
|-------|-----------|-------------------|-------------|
| Historical/Fantasy | Breath and Life, Illusionary Daytime | Time Back, 踏山河 | A Little Story, 骁 |
| Suspense/Crime | Intro-The XX | Die Weck, Lord | River Flows In You |
| Comedy | Sunny Day | Time Back, Oops | Valder Fields |
| Action/War | Breath and Life, Intro | How on Make, 踏山河 | Faded |
| Drama/Romance | Illusionary Daytime | A Little Story | Windy Hill |
| Horror/Thriller | Illusionary Daytime | Void, Disaster | 风居住的街道 |

## References

```
references/
├── task-config.md           # Input schema & validation
├── semantic-graph.md        # Video Semantic Graph schema
├── viral-formulas.md        # Viral narrative formulas
├── storyboard-export.md     # Storyboard schema & export rules
├── asr-vision-pipeline.md   # ASR + vision pipeline details
└── dependencies.md          # System & Python dependencies
```

## Scripts

- `scripts/storyboard_to_srt.py` — convert `storyboard.json` to SRT
- `scripts/validate_storyboard.py` — validate storyboard fields & timestamps

## License

MIT
