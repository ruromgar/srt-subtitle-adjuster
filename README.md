# Subtitle Timing Adjustment CLI Tool Specification

## Overview
The CLI's primary function is to adjust the timing of subtitles in `.srt` files, either by delaying or advancing them.

## Command-Line Interface

```plaintext
Usage: srt-adjuster.py [OPTIONS] FILE

Options:
  -t, --time <TIME>     Time adjustment in format [A/D]HH:MM:SS,MS or [A/D]SS,MS. A is for advance, D is for delay.
  -o, --output <FILE>   Output file name. If not specified, overwrite the original file.
  --help                Show this message and exit.
```

Example:

```bash
python srt_adjuster.py example.srt -t A00:00:05,000 -o adjusted_example.srt
python srt_adjuster.py example.srt -t D00:00:02,500 -o adjusted_example.srt
```

Full tutorial [here](https://python.plainenglish.io/how-to-synchronize-your-subtitle-files-with-python-5866ff58bc6c), but the code is pretty self-explanatory :) feel free to pass by and clap or something if you feel like it, tho.
