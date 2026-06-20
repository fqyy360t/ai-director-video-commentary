#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def fmt_time(seconds: float) -> str:
    if seconds < 0:
        raise ValueError(f"negative timestamp: {seconds}")
    millis = int(round(seconds * 1000))
    hours, rem = divmod(millis, 3600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def wrap_caption(text: str, max_chars: int) -> list[str]:
    text = " ".join(str(text).split())
    if len(text) <= max_chars:
        return [text]

    parts = []
    current = ""
    for token in text.replace("，", "， ").replace("。", "。 ").replace(",", ", ").replace(".", ". ").split():
        candidate = (current + " " + token).strip()
        if current and len(candidate) > max_chars:
            parts.append(current)
            current = token
        else:
            current = candidate
    if current:
        parts.append(current)
    return parts or [text]


def iter_entries(storyboard: dict):
    timeline = storyboard.get("timeline")
    if not isinstance(timeline, list):
        raise ValueError("storyboard must contain a timeline array")
    for item in timeline:
        output = item.get("output", {})
        yield {
            "clip_id": item.get("clip_id", ""),
            "text": item.get("sentence", ""),
            "start": float(output["start"]),
            "end": float(output["end"]),
        }


def build_srt(entries: list[dict], max_chars: int) -> str:
    blocks = []
    index = 1
    for entry in entries:
        captions = wrap_caption(entry["text"], max_chars)
        start = entry["start"]
        end = entry["end"]
        duration = max(end - start, 0.001)
        step = duration / len(captions)
        for i, caption in enumerate(captions):
            seg_start = start + i * step
            seg_end = end if i == len(captions) - 1 else start + (i + 1) * step
            blocks.append(
                f"{index}\n{fmt_time(seg_start)} --> {fmt_time(seg_end)}\n{caption}\n"
            )
            index += 1
    return "\n".join(blocks)


def main():
    parser = argparse.ArgumentParser(description="Convert AI Director storyboard.json to SRT.")
    parser.add_argument("storyboard", help="Path to storyboard.json")
    parser.add_argument("--out", default="narration_subtitle.srt", help="Output SRT path")
    parser.add_argument("--max-chars", type=int, default=24, help="Max characters per subtitle line before splitting")
    args = parser.parse_args()

    storyboard_path = Path(args.storyboard)
    data = json.loads(storyboard_path.read_text(encoding="utf-8"))
    entries = list(iter_entries(data))
    srt = build_srt(entries, args.max_chars)
    Path(args.out).write_text(srt, encoding="utf-8")


if __name__ == "__main__":
    main()
