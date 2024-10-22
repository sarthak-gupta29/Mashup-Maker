# 🎵 Mashup WebApp

A powerful web application that creates custom song mashups from your favorite artists' YouTube videos! Built with Streamlit and Python, this app makes it easy to generate unique audio mashups.

## ✨ Features

- 🎧 Download audio from YouTube videos
- ⚡ Specify number of songs to include
- ⏱️ Control duration of each audio clip
- 🔄 Automatic audio processing and merging
- 💾 Easy one-click download of final mashup

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:
- Python 3.7+
- FFmpeg

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sarthak-gupta29/Mashup-Maker.git
cd Mashup-Maker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Install system dependencies:
```bash
# On Ubuntu/Debian
sudo apt-get install ffmpeg

# On MacOS using Homebrew
brew install ffmpeg

# On Windows
# Download FFmpeg from https://ffmpeg.org/download.html
```

## 💫 Usage

1. Start the Streamlit app:
```bash
streamlit run mashup_creator.py
```

2. Enter the following details in the web interface:
   - Singer's name
   - Number of videos to include (minimum 2)
   - Duration for each audio clip (minimum 30 seconds)
   - Desired output filename

3. Click "Create Mashup" and wait for the magic to happen!

4. Download your custom mashup when it's ready!

## 🛠️ Tech Stack

- **Streamlit** - Web interface
- **yt-dlp** - YouTube video downloading
- **MoviePy** - Audio processing
- **PyDub** - Audio file handling
- **FFmpeg** - Audio conversion

## 👥 Authors

- **Sarthak Gupta** - [GitHub](https://github.com/sarthak-gupta29)
- **Aakriti Jaluria** - [GitHub](https://github.com/aakriti-jaluria)

## ⭐ Support

If you find this project helpful, please consider giving it a star! Your support means a lot to us.
