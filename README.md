# Youtube Transcript

This project allows you to download YouTube video transcripts, audio, and video content.

## Prerequisites

- Python 3.x
- ffmpeg (required for audio conversion)
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Dependencies

- youtube-transcript-api >= 0.6.1
- yt-dlp >= 2025.1.26

## Project Structure

```
.
├── srcs/
│   ├── main.py
│   ├── youtube_service.py
│   └── urls.txt
├── audio/          # Downloaded audio files
├── video/          # Downloaded video files
├── transcripts/    # Generated transcripts
├── requirements.txt
└── setup.sh
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/afuma/Youtube_transcript.git
cd Youtube_transcript
```

2. Run the setup script to create a virtual environment and install dependencies:
```bash
./setup.sh
```

## Usage

1. Add YouTube URLs to `srcs/urls.txt`, one URL per line.
2. Run the main script:
```bash
python srcs/main.py
```

The script will:
- Download video transcripts to the `transcripts/` directory
- Download audio files to the `audio/` directory
- Download video files to the `video/` directory

## Deactivating Virtual Environment

When you're done, you can deactivate the virtual environment:
```bash
deactivate
