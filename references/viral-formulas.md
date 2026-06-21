# Viral Formula Templates

Viral templates are narrative structures, not fixed wording. Use them to select and order scenes from the Video Semantic Graph.

## Template Contract

```json
{
  "id": "suspense_twist",
  "name": "Suspense Twist",
  "target_duration": 120,
  "pov": "third_person",
  "beats": [
    {
      "id": "hook",
      "duration": 8,
      "goal": "Open with the strongest contradiction, danger, or reveal.",
      "preferred_plot_roles": ["reversal", "truth_reveal", "action_peak", "emotional_peak"]
    }
  ]
}
```

## Pre-Flight: Story Five Questions

Before selecting a formula or writing any narration, answer these five questions. Skip this step and you'll get a flat summary, not a story.

### Q1 主角是谁？
- 给出一两个让人"想靠近"的特质（勇气/智慧/幽默/对弱者的同情）
- 他是哪种欲望的化身？（野心/尊严/希望/爱/自由/复仇/证明自己）
- 他有什么"种子能力"？（结尾靠它赢，前面必须埋一下）

### Q2 目标是什么？
- 事件目标（外在可验证）：观众能说出"达成了"或"没达成"
- 情感目标（内在暗钩）：主角真正渴望的是什么
- 让观众也想要主角赢

### Q3 谁在阻碍主角？
- 外部阻碍（环境/制度/自然）
- 个人阻碍（具体的对手 — 最好和主角是镜像关系）
- 内心阻碍（恐惧/创伤/偏见）

### Q4 代价是什么？
- 失败了会失去什么？至少触及一种"死亡气息"：
  - 字面死亡 / 身份死亡 / 关系死亡 / 精神死亡
- 越具体越严重越好

### Q5 为什么是现在？
- 激励事件是什么？（意外发生 / 主角决定 / 主角醒悟）
- 为什么不是早一年、不是晚一年？

## 开篇钩子生成（Step 3）

在确定故事结构之前，先生成 10 个开篇钩子供用户选择。钩子是解说的前 1-2 句话，必须在 **3 秒内** 抓住观众。

### 核心原则：反差越大越好，越无厘头越爆

**3 分钟以内的短视频，钩子只有一个目的：让观众舍不得划走。**

做到这一点的方法就是——**把最极端的反差、最离谱的爽点、最无厘头的冲突，在第一句话就甩出来。**

不要铺垫，不要交代背景，不要"从前有个人"。上来就炸。

### 钩子公式

| 公式 | 结构 | 示例 |
|------|------|------|
| **身份反转** | 最低身份 → 最高结果 | "一个上门女婿，把整个家族掀翻了" |
| **被虐开局** | 惨到极致 → 逆天改命 | "被兄弟捅刀，被女人抛弃，结果他笑着回来了" |
| **无厘头穿越** | 荒诞前提 → 燃向目标 | "作者怒了：穿越！必须穿越！让这个废物逆天改命！" |
| **全员打脸** | 所有人都看不起 → 全部被反杀 | "所有人都等着看他笑话，结果全被他打了脸" |
| **一句话判死刑** | 瞬间毁灭 → 绝地反击 | "八年心血，编辑一句话：砍了吧" |
| **数字冲击** | 夸张数字 + 极端结果 | "被骂了一百次废物，第一千零一次他笑了" |
| **狗血反问** | 用问题制造不可思议感 | "赘婿？不好意思，你们全家加起来都不够他玩的" |

### 10 个钩子生成规则

每个钩子必须满足以下至少一条：
1. ✅ **反差极大**：起点和终点之间有巨大落差（废物→王者、被踩→踩人）
2. ✅ **爽点前置**：把最爽的那一刻提前到第一句话（打脸、逆袭、翻盘）
3. ✅ **无厘头**：荒诞到让人忍不住想看下去（"一个写小说的，把自己写进去了"）
4. ✅ **情绪爆破**：愤怒、委屈、不甘、狂喜——上来就给强烈情绪
5. ❌ **禁止平淡**：不要"从前有个人""这个故事讲的是""今天给大家讲一个"
6. ❌ **禁止铺垫**：背景信息放到第二句以后，第一句只管炸

### 10 个钩子的风格分配

| 编号 | 方向 | 技巧 |
|------|------|------|
| 1-3 | **反差+爽点** | 身份反转、被虐开局、全员打脸 |
| 4-6 | **无厘头+狗血** | 荒诞前提、夸张情绪、标题党 |
| 7-8 | **悬念+冲突** | 信息差、正邪对峙、致命一击 |
| 9 | **提问型** | 向观众抛出不可思议的问题 |
| 10 | **数据+情绪** | 数字冲击 + 极端情绪 |

### 钩子决定基调

用户选定钩子后，整篇解说的情感风格由钩子决定：
- 选了反差型 → 全篇围绕"所有人都看走眼了"展开，爽点层层递进
- 选了无厘头型 → 全篇可以更夸张、更有情绪张力，节奏更快
- 选了悬念型 → 全篇保持悬念感，信息逐步释放，最后大反转
- 选了冲突型 → 全篇强调对抗、升级、打脸

## Structure Selection

| 目标时长 | 推荐结构 | 剪辑数 | 解说句数 |
|----------|---------|--------|---------|
| 30秒-3分钟 | 黄金五段式 | 8-15 clips | 12-25 lines |
| 90-180秒 | Harmon 8步 + 三幕骨架 | 12-18 clips | 18-28 lines |
| 3-15分钟 | 三幕式 | 18-30 clips | 28-50 lines |

### Harmon 8-Step Circle (default for short video)

```
1. You   角色 — 舒适区中的主角
2. Need  需要 — 不满或渴望
3. Go    出发 — 踏出舒适区
4. Search 寻找 — 适应、试错、遇阻
5. Find  找到 — 发现真正需要的东西
6. Take  代价 — 要得到它必须付出什么
7. Return 归来 — 带着改变回到原点
8. Change 改变 — 已不是出发时的那个人
```

上半圆(1-4)=熟悉世界 | 下半圆(5-8)=陌生世界

主角从1出发顺时针走，降入陌生世界，再上升回到起点——但已经变了。

### 黄金五段式（30秒-3分钟首选）

经典商业叙事结构：**吸引钩子 → 提出问题 → 核心内容/解决方案 → 转化推高潮 → 行动呼吁 CTA**

最适合 1-3 分钟短视频/中视频，是小红书、B站、微信公众号视频的黄金区间。

#### 30秒-1分钟（极速爆款）

适用平台：抖音、快手、视频号、TikTok、Reels

每个部分极度精简，"提出问题"和"核心内容"可合并。

| 时间 | 节拍 | 要求 |
|------|------|------|
| 0-3s | 钩子 | 最劲爆的视觉或悬念，必须 3 秒内抓住 |
| 3-10s | 痛点 | 快速引发共鸣 |
| 10-45s | 核心剧情 | 毫无废话的干货输出 |
| 45-55s | 情绪推高潮 | 转折/升华/爆发 |
| 55-60s | CTA | 强引导关注 |

#### 1分钟-3分钟（黄金核心区间 ✨ 最推荐）

适用平台：小红书、B站短内容、微信公众号视频

有足够时间把问题讲透、反转做足，观众又不容易审美疲劳。

| 时间 | 节拍 | 要求 |
|------|------|------|
| 0-10s | 钩子 | 抛出最强悬念/矛盾/视觉冲击 |
| 10-30s | 问题展开 | 痛点/冲突/背景铺陈 |
| 30-90s | 核心内容 | 层层递进，提供真正价值或剧情推进 |
| 90-110s | 价值升华/情绪高潮 | 反转、升华、情感爆发 |
| 110-120s | CTA | 行动呼吁（关注/评论/下一集） |

#### 使用原则

- **钩子决定生死**：前 3 秒必须抛出最强信息，不要铺垫
- **问题要具体**：不说"他遇到了困难"，说"他只有 24 小时找到解药"
- **核心内容层层递进**：每一层比上一层更深入/更意外/更紧张
- **CTA 融入叙事**：最好的行动呼吁是让观众"不得不"看下一集/关注，而非生硬引导
- **ABCD 因果检验仍然适用**：五段之间必须是"所以/但是"关系，不能是"然后"

### Three-Act Checkpoints (for 120s)

| 时间 | 节拍 | 做什么 |
|------|------|--------|
| 0-12s | Hook + 激励事件 | 打破平衡，观众"在乎"主角 |
| 12-30s | 第一情节点 | 踏上旅程，回不去了 |
| 30-65s | 进展纠葛 | 阻碍不断升级，不重复 |
| 55-65s | 中点反转 | 重大转折 |
| 65-90s | 灵魂黑夜 | 最低谷 |
| 90-115s | 高潮 | 最后行动 |
| 115-120s | 结局+释放 | 情绪出口 |

## ABCD Causality Check

来自《南方公园》主创：

> **"然后"是流水账，"但是/所以"才是故事。**

写完全部 narration 后，逐句检查：
- 如果两句之间是"然后" → 重写
- 如果两句之间是"所以"或"但是" → 通过

格式：**某人想要 A，所以做了 B，但是发生了 C，因此不得不做 D。**

## Genre Mapping

`high_iq_crime`:
```text
hook: impossible crime or shocking result
setup: protagonist, target, or victim
misdirection: false clue or wrong suspect
plan: hidden operation or logic chain
twist: real mastermind or method
cliffhanger: one unanswered risk
```

`revenge`:
```text
hook: humiliation or betrayal
setup: protagonist's weakness or disguise
escalation: enemies press harder
reveal: protagonist's hidden identity or plan
payoff: first counterattack
cliffhanger: bigger revenge target
```

`suspense_thriller` / `mystery_brain_burn`:
```text
hook: impossible event or disturbing clue
setup: normal world breaks
investigation: clue chain
danger: protagonist gets too close
twist: meaning of clue changes
ending: unresolved threat or final question
```

`horror_thriller`:
```text
hook: abnormal event
setup: place, rule, or taboo
first_scare: proof that danger is real
escalation: escape fails
truth: what the monster/curse wants
ending: last scare or survival hook
```

`romance`:
```text
hook: emotional contradiction
setup: first meeting or relationship state
obstacle: misunderstanding, class, family, timing
peak: confession, breakup, sacrifice, or missed chance
resolution: reconciliation or regret
```

`sci_fi` / `sci_fi_disaster` / `disaster`:
```text
hook: large-scale crisis or impossible phenomenon
setup: rule of the world
outbreak: disaster begins
survival: key choices and sacrifices
reveal: cause or hidden truth
ending: survival, loss, or next wave
```

`action` / `superhero` / `war`:
```text
hook: fight, chase, explosion, impossible threat
setup: mission or stakes
escalation: stronger enemy or deadline
turning_point: failed plan or sacrifice
payoff: decisive action
ending: victory cost or next mission
```

`palace_intrigue`:
```text
hook: betrayal, accusation, or secret order
setup: power relationship
scheme: hidden alliance or trap
countermove: protagonist survives the plot
reveal: true patron or enemy
cliffhanger: next political danger
```

`comedy`:
```text
hook: absurd conflict
setup: normal goal
mistake_chain: escalating misunderstandings
peak: public embarrassment or reversal
payoff: punchline or ironic ending
```

`warm_emotional` / `inspirational` / `fairy_tale` / `fantasy`:
```text
hook: emotional promise or magical problem
setup: protagonist's wound or wish
journey: trials and helpers
choice: sacrifice or courage
payoff: transformation
ending: warmth, wonder, or moral echo
```

## POV Rules

First person:
- Write as lived experience.
- Use "I" only if it is clear whose viewpoint the story follows.
- Prefer internal emotion, regret, fear, realization, and resolve.
- Avoid omniscient facts the viewpoint character could not know at that moment unless framed as later reflection.

Third person:
- Write like a commentary channel.
- Name characters by role if names are unknown: "the man", "the woman", "the doctor", "the killer".
- Use suspenseful cause-effect phrasing and concise transitions.

## Duration Budget

For 30-60 seconds (黄金五段式 极速版): 5-8 clips, 8-12 narration lines.

For 60-120 seconds (黄金五段式 黄金区间): 8-15 clips, 12-25 narration lines.

For 120-180 seconds: 12-18 clips, 18-28 narration lines.

For 180+ seconds (default): 16-30 clips, 28-50 narration lines.

Do not over-pack narration. Leave visual room for key reactions, reveals, and action.
