# Video Semantic Graph

The Video Semantic Graph is the product's core asset. It is not a subtitle list. It is a graph of scenes, events, characters, dialogue, visual evidence, emotions, and plot relationships.

## Core Nodes

```json
{
  "nodes": [
    {
      "id": "scene_0018",
      "type": "scene",
      "start": 4700.0,
      "end": 4708.0,
      "summary": "The male lead discovers the contract signature was forged.",
      "location": "office",
      "characters": ["char_male_lead", "char_lawyer"],
      "emotion": "shock",
      "visual_intensity": 0.86,
      "plot_tags": ["evidence", "reversal", "fraud"]
    },
    {
      "id": "dialogue_0091",
      "type": "dialogue",
      "start": 4702.0,
      "end": 4704.0,
      "speaker": "speaker_01",
      "text": "This is not my signature."
    },
    {
      "id": "visual_0277",
      "type": "visual_event",
      "start": 4701.5,
      "end": 4706.5,
      "action": "The male lead points at the contract and freezes in shock.",
      "evidence": "forged signature on contract"
    }
  ],
  "edges": [
    {
      "from": "dialogue_0091",
      "to": "scene_0018",
      "type": "belongs_to"
    },
    {
      "from": "visual_0277",
      "to": "scene_0018",
      "type": "belongs_to"
    },
    {
      "from": "visual_0277",
      "to": "dialogue_0091",
      "type": "supports"
    }
  ]
}
```

## Fusion Rules

- Align all modalities by source-video seconds.
- Use scene boundaries as the primary grouping unit.
- Attach ASR segments to scenes when their time ranges overlap.
- Attach Qwen3-VL-Plus summaries to scenes from representative frames or frame groups.
- Attach OCR only when enabled or when important screen text is detected.
- Preserve uncertain labels with confidence scores instead of overclaiming.

## Scene Scoring Features

Score scenes using:
- plot importance
- emotional intensity
- visual conflict
- dialogue information density
- action intensity
- evidence/reveal value
- genre relevance
- template fit

Example:

```json
{
  "scene_id": "scene_0018",
  "scores": {
    "plot_importance": 0.94,
    "emotion": 0.82,
    "dialogue": 0.76,
    "visual_conflict": 0.71,
    "genre_fit": 0.91,
    "template_fit": 0.88
  },
  "plot_role": "truth_reveal"
}
```

## Plot Roles

Use these stable labels when possible:
- `hook`
- `character_setup`
- `inciting_incident`
- `conflict_escalation`
- `evidence`
- `foreshadowing`
- `reversal`
- `truth_reveal`
- `emotional_peak`
- `action_peak`
- `payoff`
- `cliffhanger`
- `transition`
