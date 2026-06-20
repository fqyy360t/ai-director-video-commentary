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

## Structure Selection

| 目标时长 | 推荐结构 | 剪辑数 | 解说句数 |
|----------|---------|--------|---------|
| 60-90秒 | Harmon 8步 | 8-10 clips | 12-16 lines |
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

For 60 seconds: 5-8 clips, 8-12 narration lines.

For 120 seconds: 10-18 clips, 16-28 narration lines.

For 180 seconds (default): 16-28 clips, 25-42 narration lines.

Do not over-pack narration. Leave visual room for key reactions, reveals, and action.
