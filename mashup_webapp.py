# mashup_web.py
import yt_dlp
import moviepy.editor as mp
import os
import zipfile
import streamlit as st

# Function to download videos using yt-dlp
def download_video(video_url, output_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Function to extract and merge audio files, starting from 2 seconds
def merge_audio_files(audio_folder, output_file):
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]
    audio_clips = [mp.AudioFileClip(os.path.join(audio_folder, f)).subclip(2) for f in audio_files]  # Start at 2 seconds
    merged_audio = mp.concatenate_audioclips(audio_clips)
    merged_audio.write_audiofile(output_file)
    print(f"Merged audio saved to {output_file}")

# Zipping the final merged audio file
def zip_audio_file(audio_file, zip_file):
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        zipf.write(audio_file, os.path.basename(audio_file))
    print(f"{audio_file} has been zipped into {zip_file}")

# Streamlit Web Interface
st.title("YouTube Mashup Maker")
st.write("Download and merge YouTube audio clips into a single mashup!")

video_urls = st.text_area("Enter YouTube Video URLs (one per line)")
if st.button("Create Mashup"):
    video_url_list = video_urls.splitlines()
    output_folder = 'downloads/audio_files'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    merged_output = os.path.join(output_folder, 'merged_audio.mp3')
    zip_output = os.path.join(output_folder, 'merged_audio.zip')

    # Download videos
    for video_url in video_url_list:
        if video_url:
            download_video(video_url, output_folder)
    
    # Merge audio files
    merge_audio_files(output_folder, merged_output)
    
    # Zip the merged file
    zip_audio_file(merged_output, zip_output)
    
    st.success(f"Mashup created successfully! Download the ZIP file [here](./{zip_output}).")
