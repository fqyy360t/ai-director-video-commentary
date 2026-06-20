#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_ITEM_FIELDS = ["clip_id", "sentence_id", "sentence", "source", "output", "visual_summary", "match_reason"]


def validate(data: dict) -> list[str]:
    errors = []
    timeline = data.get("timeline")
    if not isinstance(timeline, list) or not timeline:
        return ["storyboard.timeline must be a non-empty array"]

    previous_end = 0.0
    seen_clip_ids = set()

    for idx, item in enumerate(timeline, start=1):
        prefix = f"timeline[{idx}]"
        for field in REQUIRED_ITEM_FIELDS:
            if field not in item:
                errors.append(f"{prefix} missing required field: {field}")

        clip_id = item.get("clip_id")
        if clip_id in seen_clip_ids:
            errors.append(f"{prefix} duplicate clip_id: {clip_id}")
        seen_clip_ids.add(clip_id)

        sentence = str(item.get("sentence", "")).strip()
        if not sentence:
            errors.append(f"{prefix} sentence is empty")

        source = item.get("source", {})
        output = item.get("output", {})
        try:
            source_start = float(source["start"])
            source_end = float(source["end"])
            output_start = float(output["start"])
            output_end = float(output["end"])
        except Exception as exc:
            errors.append(f"{prefix} invalid source/output timestamps: {exc}")
            continue

        if source_end <= source_start:
            errors.append(f"{prefix} source.end must be greater than source.start")
        if output_end <= output_start:
            errors.append(f"{prefix} output.end must be greater than output.start")
        if output_start < previous_end - 0.001:
            errors.append(f"{prefix} output.start overlaps or goes backward")
        previous_end = output_end

        match_score = item.get("match_score")
        if match_score is not None:
            try:
                score = float(match_score)
                if not 0 <= score <= 1:
                    errors.append(f"{prefix} match_score must be between 0 and 1")
            except Exception:
                errors.append(f"{prefix} match_score must be numeric")

        flags = item.get("review_flags", [])
        if flags is not None and not isinstance(flags, list):
            errors.append(f"{prefix} review_flags must be an array")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate AI Director storyboard.json.")
    parser.add_argument("storyboard", help="Path to storyboard.json")
    args = parser.parse_args()

    data = json.loads(Path(args.storyboard).read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("OK: storyboard is valid")


if __name__ == "__main__":
    main()
