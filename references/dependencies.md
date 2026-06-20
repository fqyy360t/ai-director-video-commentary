# Dependencies

This skill assumes FFmpeg is available on PATH and Python packages are installed from `requirements.txt`.

## Required System Tool

- FFmpeg: video probing, audio extraction, trimming, concatenation, subtitle burn-in if needed.

## Python Packages

- `faster-whisper`: ASR and Dialogue Timeline.
- `scenedetect`: scene/shot boundary detection.
- `opencv-python`: frame extraction and image preprocessing.
- `openai`: OpenAI-compatible API client for Qwen-compatible endpoints (text reasoning is handled by Claude built-in, no API needed).
- `pydantic`: structured data validation.
- `python-dotenv`: local API key loading.
- `ffmpeg-python`: optional Python wrapper for FFmpeg command generation.
- `srt`: SRT parsing and writing.

## Model API Notes

Text reasoning (plot analysis, narration writing, storyboard planning) is handled by Claude directly within the agent session — no external API call or key needed.

Qwen3-VL-Plus can be called either through an OpenAI-compatible endpoint or provider SDK. Prefer OpenAI-compatible routing when available so the pipeline has one client abstraction.

### Local faster-whisper

Requires a CTranslate2 format model at `D:\models\faster-whisper-medium` (default). The directory must contain:
- `model.bin`
- `config.json`
- `tokenizer.json`
- `vocabulary.txt`

For CUDA GPU acceleration, the system needs `cublas64_12.dll`. If missing:
- Install CUDA Toolkit 12.x, or
- `pip install nvidia-cublas-cu12`, or
- The pipeline auto-falls back to CPU (`device='cpu', compute_type='int8'`)

### Volcengine ASR (optional)

Requires `VOLCENGINE_API_KEY` in `.env` file. Uses the async speech recognition API at `openspeech.bytedance.com`.
