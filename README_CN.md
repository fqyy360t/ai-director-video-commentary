# 🎬 AI Director Video Commentary

> 一集 40 分钟的电视剧 → 一段 5 分钟的病毒式解说。AI 驱动，全自动。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange)](https://claude.ai/code)
[![English Docs](https://img.shields.io/badge/Docs-English-blue.svg)](README.md)

---

**语言：** [English](README.md) | [中文](#)

---

## 这是什么

给一集电视剧或一部电影，AI 自动完成：剧情调研 → 多模态语义分析 → 病毒式解说文案生成 → 分镜脚本规划 → FFmpeg 渲染 → SRT 字幕输出。最终交付一个可直接导入剪映做 TTS 配音、BGM 和封面的完整解说成片。

**核心理念：** 不是先剪片子再配字幕，而是先生成语义图谱 → 写解说 → 绑定画面 → 渲染。Storyboard 是 AI 规划与 FFmpeg 渲染之间的唯一契约。

## 效果演示

输入：`赘婿` 第一集（40 分钟）  
输出：5 分钟解说成片 + 50 条 SRT 字幕

```
=== 校验报告 ===
视频时长:    272.694s (4.5min)
字幕末尾:    272.628s
差值:        0.066s
字幕条数:    50 条
状态:        ✓ 通过
```

## 整体架构

```
用户输入（视频 + 片名 + 主演 + 题材 + 时长）
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 1-2  任务配置 + 网络剧情调研                │
│            产出：Director's Brief                 │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 3     多模态时间线构建                      │
│             FFmpeg 提取音视频                     │
│             faster-whisper ASR 语音识别           │
│             PySceneDetect 场景检测                │
│             Qwen3-VL-Plus 视觉分析                │
│             产出：asr_timeline.json               │
│                   vision_analysis.json             │
│                   scenes.json                      │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 4     视频语义图谱融合                      │
│             场景/事件/角色/情绪节点 + 关系边       │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 5-6   Claude 故事导演 + 分镜脚本            │
│             病毒式叙事公式 → 解说词生成            │
│             ASR 时间戳交叉验证（强制）             │
│             产出：storyboard.json                 │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 7     用户确认故事板（必须）                 │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│  Step 8     FFmpeg 渲染 + 拼接 + SRT              │
│             校验：视频-SRT 对齐误差 < 0.5s        │
│             产出：final_preview.mp4               │
│                   narration_subtitle.srt           │
└──────────────────────────────────────────────────┘
```

## 模型分工

| 环节 | 模型 | 说明 |
|------|------|------|
| 视觉画面解析 | **Qwen3-VL-Plus** (DashScope) | 逐帧分析角色、情绪、动作、场景 |
| 语音识别 | **faster-whisper** (本地) | CTranslate2 模型，支持 CUDA/CPU 自动切换 |
| 文案撰写、剧情分析、分镜规划 | **Claude** (内置) | 无需额外 API 调用 |

## 前置依赖

### 系统工具
- **FFmpeg** 4.0+ — 视频编解码、提取音视频、变速、拼接
- **Python** 3.10+

### Python 包
```bash
pip install faster-whisper scenedetect opencv-python openai python-dotenv srt
```

### ASR 语音识别模型
下载 CTranslate2 格式的模型到 `D:\models\faster-whisper-medium\`：

```bash
huggingface-cli download Systran/faster-whisper-medium --local-dir D:\models\faster-whisper-medium
```

需要以下 4 个文件（共约 1.5 GB）：
```
model.bin         ← 核心模型
config.json       ← 模型配置
tokenizer.json    ← 分词器
vocabulary.txt    ← 词表
```

> 💡 **GPU 加速：** 有 NVIDIA 显卡时自动启用 CUDA。`pip install nvidia-cublas-cu12` 安装 CUDA 依赖。缺少 DLL 时自动回退 CPU。

### 视觉模型 API
在工作目录创建 `.env` 文件：

```env
QWEN_API_ENDPOINT=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
QWEN_VL_MODEL=qwen3-vl-plus
```

> 🔑 在 [DashScope 控制台](https://dashscope.console.aliyun.com/) 申请 API Key，开通 Qwen3-VL-Plus 模型。

## 操作步骤

> 全程 5 步，人工操作约 **5 分钟**，AI 自动运行约 **15-25 分钟**。

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  步骤 1  │    │  步骤 2  │    │  步骤 3  │    │  步骤 4  │    │  步骤 5  │
│  安装    │───▶│  配置    │───▶│  传入    │───▶│  AI 解说 │───▶│  成片    │
│  1 分钟  │    │  15 分钟 │    │  2 分钟  │    │ 15-25分钟│    │  5 分钟  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

### 步骤 1：安装 Skill

> 🎯 一次性操作。将本 Skill 注册到 Claude Code。

**方式一：命令行安装（推荐）**
```
/install ai-director-video-commentary
```

**方式二：Git 手动安装**
```bash
# Windows
git clone <repo-url> %USERPROFILE%\.claude\skills\ai-director-video-commentary

# macOS / Linux
git clone <repo-url> ~/.claude/skills/ai-director-video-commentary
```

重启 Claude Code 或 `/reload`。  
**验证：** 输入 `/ai` 按 Tab 键，看到 `ai-director-video-commentary` 即表示就绪。

---

### 步骤 2：配置运行环境

> 🎯 一次性操作。让管线脚本能在本机跑起来。

#### 2.1 系统依赖

| 工具 | 版本 | 用途 | Windows 安装 |
|------|------|------|-------------|
| **FFmpeg** | 4.0+ | 提取音视频、变速、拼接 | `winget install ffmpeg` |
| **Python** | 3.10+ | 运行所有管线脚本 | `winget install python` |

验证：
```bash
ffmpeg -version
python --version   # 应为 3.10+
```

#### 2.2 Python 依赖
```bash
pip install faster-whisper scenedetect opencv-python openai python-dotenv srt
```

验证：
```bash
python -c "import faster_whisper; import scenedetect; import cv2; import openai; print('OK')"
```

#### 2.3 ASR 模型（约 1.5 GB）
```bash
huggingface-cli download Systran/faster-whisper-medium --local-dir D:\models\faster-whisper-medium
```

或从 [HuggingFace](https://huggingface.co/Systran/faster-whisper-medium) 手动下载：
```
D:\models\faster-whisper-medium\
├── model.bin
├── config.json
├── tokenizer.json
└── vocabulary.txt
```

#### 2.4 视觉模型 API Key
在工作目录创建 `.env`：
```env
QWEN_API_ENDPOINT=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
QWEN_VL_MODEL=qwen3-vl-plus
```

#### ✅ 环境就绪检查清单
```
[ ] ffmpeg --version 成功
[ ] python --version 输出 3.10+
[ ] python -c "import faster_whisper" 无报错
[ ] D:\models\faster-whisper-medium\model.bin 存在
[ ] .env 文件中有 QWEN_API_KEY
```

---

### 步骤 3：传入视频及影片信息

> 🎯 告诉 AI 你手头是什么片子、想做什么风格、要多长。

#### 3.1 启动 Skill
```
/ai-director-video-commentary C:\path\to\video.mp4
```

#### 3.2 逐项确认配置

AI 会依次询问 8 个问题，逐一回答即可：

| 第几步 | AI 会问 | 怎么回答 | 示例 |
|--------|--------|---------|------|
| ① | 片名？ | 影视作品完整名称 | `赘婿` |
| ② | 主演？ | 逗号分隔 | `郭麒麟、宋轶` |
| ③ | 影视类型？ | 五选一 | `电视剧` |
| ④ | 影视题材？ | 从 20 种中选 | `奇幻` |
| ⑤ | 解说类型？ | 第一/第三人称 | `第三人称解说` |
| ⑥ | 解说时长？ | 指定分钟数 | `5分钟` |
| ⑦ | 第几集？ | 电视剧/动漫时 | `第一集` |
| ⑧ | 剧情梗概？ | 粘贴或回车跳过 | （可选） |

#### 📋 完整对话示例
```
用户：/ai-director-video-commentary C:\video\赘婿S01E01.mp4

AI：  请问片名是什么？
用户：赘婿

AI：  主演名单？
用户：郭麒麟、宋轶

AI：  影视类型？（电视剧/电影/动漫/短剧/外语解说）
用户：电视剧

AI：  影视题材？（20种可选）
用户：奇幻

AI：  解说类型？（第一人称/第三人称，默认第三人称）
用户：第三人称

AI：  解说时长？（1/2/3/5/8/10分钟，电视剧推荐5分钟）
用户：5分钟

AI：  第几集？
用户：第一集

AI：  有剧情梗概吗？（回车跳过，AI自动搜索）
用户：（回车）

AI：  配置确认完毕。[展示汇总表格]，开始执行管线...
```

> 💡 **智能默认值：** 电视剧→5 分钟 | 电影→5 分钟 | 短剧/动漫→3 分钟 | 外语解说→3 分钟。

---

### 步骤 4：AI 解说生成

> 🎯 AI 自动分析视频、撰写解说、规划分镜。有一个确认节点需要你介入。

#### 4.1 AI 自动执行流程

| 阶段 | 做什么 | 耗时 | 产出 |
|------|--------|------|------|
| 🔍 剧情调研 | 网络搜索剧情、角色关系、关键转折 | ~30s | `directors_brief.md` |
| 🎤 语音识别 | 提取音频 → faster-whisper 转写全片对话 | ~5-10min | `asr_timeline.json`（~690 段） |
| 🎬 场景检测 | PySceneDetect 切分场景 → 提取关键帧 | ~2min | `scenes.json` + 200+ 张关键帧 |
| 👁️ 视觉分析 | Qwen3-VL-Plus 逐帧分析角色/情绪/场景 | ~5-10min | `vision_analysis.json` |
| ✍️ 解说生成 | Claude 选叙事公式 → 写解说词 → 绑定画面 | ~2min | `storyboard.json` |

> 进度实时输出到对话中，可随时看到执行到哪一步。

#### 4.2 ⚠️ 故事板确认（必须手动确认）

AI 生成完分镜脚本后，展示概览并**等你确认**：

```
📋 故事板概览：《赘婿》第一集 · 5分钟解说

────────────────────────────────────────────
总体数据
────────────────────────────────────────────
字幕条数：  50 条
总时长：    272 秒（4 分 32 秒）
平均每条：  5.4 秒

────────────────────────────────────────────
第一幕：Hook + 穿越（0~57s，11条）
────────────────────────────────────────────
编辑深夜逼宫 → 江皓辰被兄弟背叛 → 作者不服 →
"新书主角还是江皓辰" → 穿越到武朝

────────────────────────────────────────────
第二幕：苏家风云（57~200s，24条）
────────────────────────────────────────────
宁毅苏醒 → 赘婿身份 → 错认新娘大妈 →
二房阴谋 → 议事厅舌战 → 惊艳全场

────────────────────────────────────────────
第三幕：蜕变展望（200~272s，15条）
────────────────────────────────────────────
契约婚姻 → 大婚前夜 → 花轿羞辱 →
"赘婿二字从来不是终点，而是起点"
```

此时你可以：

| 操作 | 输入 | 效果 |
|------|------|------|
| ✅ 确认通过 | `通过` / `确认` / `OK` | 立即进入步骤 5 渲染 |
| 🔧 局部调整 | `第二幕太长了，精简一点` | AI 重写指定段落后重新展示 |
| 🔄 推翻重来 | `推翻` / `重来` | 回到剧情分析阶段重新生成 |

> ⚠️ **不确认不会进入渲染。** 这是质量把关的最后一道门。

---

### 步骤 5：剪辑成片

> 🎯 拿到可在剪映中精修的成片 + 字幕。

#### 5.1 AI 自动渲染 + 校验

确认后全自动执行（约 3-5 分钟）：

```
[1/4] 渲染 50 条独立 clip（含变速处理）...
      clip_001 OK (src=5.5s -> out=4.6s, speed=1.2x)
      clip_002 OK (src=9.0s -> out=5.9s, speed=1.5x)
      ...
[2/4] 拼接为 final_preview.mp4...
[3/4] 生成 narration_subtitle.srt...
[4/4] 执行校验...

=== 校验报告 ===
视频时长:    272.694s (4.5min)
字幕末尾:    272.628s
差值:        0.066s
字幕条数:    50 条
状态:        ✓ 通过
```

> 如果校验失败（差值 > 0.5s），AI 会用 ffprobe 逐条探测实际时长重建 SRT，直到通过。

#### 5.2 获取交付物

```
📁 output/
├── 📁 pipeline/                    ← 中间产物（调试用，可忽略）
│   ├── directors_brief.md
│   ├── asr_timeline.json
│   ├── scenes.json
│   ├── vision_analysis.json
│   ├── storyboard.json
│   └── keyframes/
└── 📁 deliverables/                ← ⭐ 最终交付物
    ├── 🎬 final_preview.mp4         ← 完整解说成片
    └── 📝 narration_subtitle.srt    ← 解说字幕（时间轴已对齐）
```

#### 5.3 剪映后期（5 分钟）

| 步骤 | 操作 | 说明 |
|------|------|------|
| **① 导入视频** | 拖入 `final_preview.mp4` | 主轨道 |
| **② 导入字幕** | 拖入 `narration_subtitle.srt` | 自动对齐时间轴 |
| **③ TTS 配音** | 框选字幕 →「文本朗读」→ 选音色 | 推荐「解说男声」「阳光男声」 |
| **④ 添加 BGM** | 音频 → 音乐库 → 搜索 AI 推荐的曲名 | 音量 20-30%，不抢词 |
| **⑤ 微调** | 检查关键节点画面是否到位 | 参考 AI 给的踩点时间 |
| **⑥ 导出** | 1080p / 30fps / H.264 | 码率推荐 8-16 Mbps |

#### 5.4 BGM 快速参考

| 情绪段 | 推荐曲目（剪映可搜） | 备选 |
|--------|---------------------|------|
| 开场铺垫 | `Breath and Life` `幻昼` | `Not One` |
| 冲突逆转 | `Time Back` `踏山河` | `How on Make` |
| 收尾释放 | `A Little Story` `骁` | `Windy Hill` |

> 🎯 **省事方案：** 只搜 `Time Back` 一首从头铺到尾，影视解说圈公认万金油。

---

## 🔧 常见问题

<details>
<summary><b>Q: 字幕和画面内容对不上？</b></summary>

对 AI 说 **"字幕和画面对不上，校对一下"**，AI 会执行系统性校对：

1. 以 `asr_timeline.json` 为绝对时间参照，逐条交叉比对每个 clip
2. 标记所有 ASR 对话与解说剧情不一致的 clip
3. 按 30 秒分块打印完整 ASR 对话，重新确定正确时间戳
4. 重建 `storyboard.json` → 重新渲染 → 重新校验
</details>

<details>
<summary><b>Q: 解说风格/内容不满意？</b></summary>

在步骤 4 的故事板确认环节直接提要求：
- `太啰嗦了，精简到 3 分钟`
- `开头不够炸裂，换个更抓人的开场`
- `第三人称改第一人称`

AI 会调整解说词后重新展示故事板。
</details>

<details>
<summary><b>Q: 没有 NVIDIA 显卡能用吗？</b></summary>

可以。ASR 检测不到 CUDA 时会自动回退 CPU 模式。仅 ASR 速度从 ~5 分钟延长到 ~15 分钟，其余环节不受影响。
</details>

<details>
<summary><b>Q: 想批量处理多集？</b></summary>

每集单独执行一次 Skill：
1. 按 `S01E01.mp4`、`S01E02.mp4` 命名视频文件
2. 每次调用 Skill 传入对应文件
3. 环境和模型已就绪，后续集数配置更快
</details>

## 配置项速查

| 配置项 | 必填 | 可选值 |
|--------|------|--------|
| 输入视频 | ✓ | 本地 mp4 路径 |
| 片名 | ✓ | 任意影视作品名称 |
| 主演 | ✓ | 数组格式 |
| 解说类型 | ✓ | `first_person` / `third_person` |
| 影视类型 | ✓ | `tv_drama` / `movie` / `anime` / `short_drama` / `foreign` |
| 影视题材 | ✓ | 20 种题材 |
| 解说时长 | ✓ | 60 / 120 / 180 / 300 / 480 / 600 秒 |
| 集数 | 可选 | 电视剧/动漫时使用 |

## 输出目录结构

```
output/
├── pipeline/                     # 中间产物（调试/回溯）
│   ├── directors_brief.md        # 导演简报
│   ├── asr_timeline.json         # ASR 对话时间线
│   ├── scenes.json               # 场景检测结果
│   ├── semantic_blocks.json      # 语义块
│   ├── vision_analysis.json      # 视觉分析结果
│   ├── storyboard.json           # 分镜脚本
│   └── keyframes/                # 关键帧图片
└── deliverables/                 # 最终交付物
    ├── final_preview.mp4         # 完整成片
    └── narration_subtitle.srt    # 解说字幕
```

## 字幕规则

- 按自然语义断句，一句话 = 一条字幕
- 每条字幕时长 = 汉字数 ÷ 4 + 0.1s 缓冲，最短 1s
- SRT 时间轴与成片实际时长误差 < 0.5s（强制校验）

## 质量保障

### 渲染前：故事板时间戳验证
每条 clip 的 source 时间戳与 ASR 对话时间线逐条交叉比对，不一致项必须修正后才能进入渲染。

### 渲染后：视频-SRT 对齐校验
```python
diff = |ffprobe_video_duration - srt_last_end|
assert diff < 0.5  # 否则自动修复
```

### 交付后：字幕画面校对
用户反馈不匹配时，基于 ASR 时间线作为绝对参照完全重建时间戳，修正后重新渲染并校验。

## 病毒式叙事公式

内置多套叙事结构模板，按内容类型和目标时长自动选择：

| 目标时长 | 结构 | 解说句数 |
|----------|------|---------|
| 60-90s | Harmon 8 步 | 12-16 句 |
| 90-180s | Harmon 8 步 + 三幕骨架 | 18-28 句 |
| 3-15 分钟 | 三幕式 | 28-50 句 |

ABCD 因果链检查：「然后」是流水账，「所以/但是」才是故事。

## BGM 推荐

交付后按影片题材推荐三段式 BGM（优先剪映内置曲库）：

| 题材 | Hook/铺垫 | 冲突/逆转 | 释放/收尾 |
|------|----------|----------|----------|
| 古装/奇幻/穿越 | Breath and Life、幻昼 | Time Back、踏山河 | A Little Story、骁 |
| 悬疑/犯罪/烧脑 | Intro-The XX | Die Weck、Lord | River Flows In You |
| 喜剧/轻喜剧 | Sunny Day、小城夏天 | Time Back、Oops | Valder Fields |
| 动作/战争/超级英雄 | Breath and Life、Intro | How on Make、踏山河 | Faded |
| 温情/励志/浪漫 | 幻昼 | A Little Story | 所念皆星河、Windy Hill |
| 恐怖/惊悚 | 幻昼 | Void、Disaster | 风居住的街道 |

## 参考文件

```
references/
├── task-config.md           # 输入 schema 与验证规则
├── semantic-graph.md        # 视频语义图谱 schema
├── viral-formulas.md        # 病毒式叙事公式模板
├── storyboard-export.md     # 分镜脚本 schema 与导出规范
├── asr-vision-pipeline.md   # ASR + 视觉分析管线
└── dependencies.md          # 系统与 Python 依赖
```

## Scripts

- `scripts/storyboard_to_srt.py` — 将 `storyboard.json` 转为 SRT
- `scripts/validate_storyboard.py` — 验证 storyboard 字段与时间戳

## License

MIT
