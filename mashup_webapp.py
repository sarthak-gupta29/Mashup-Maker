import streamlit as st
import re
import yt_dlp
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
import os

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title)

def download_videos(singer_name, number_of_videos):
    downloaded_files = []
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }

    search_url = f"https://www.youtube.com/results?search_query={singer_name}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(search_url, download=False)
            entries = info_dict['entries']
            if len(entries) < number_of_videos:
                st.warning(f"Only {len(entries)} videos found. Downloading all of them.")
                number_of_videos = len(entries)

            for i in range(number_of_videos):
                video_title = sanitize_filename(entries[i]['title'])
                st.write(f"Downloading video {i + 1}/{number_of_videos}: {video_title}")
                ydl.download([entries[i]['url']])
                downloaded_files.append(f"{video_title}.mp3")
                
        except Exception as e:
            st.warning(f"Error downloading videos: {e}")
            return []

    return downloaded_files

def convert_videos_to_audio(downloaded_files, audio_duration):
    audio_clips = []

    for i, video_file in enumerate(downloaded_files):
        try:
            st.write(f"Processing audio {i + 1}/{len(downloaded_files)}: Trimming to {audio_duration} seconds.")
            audio_clip = AudioFileClip(video_file).subclip(0, audio_duration)
            audio_clips.append(audio_clip)
        except Exception as e:
            st.warning(f"Error processing audio {i + 1}: {e}. Skipping this file.")

    return audio_clips

def merge_audios(audio_clips, output_file_name):
    combined = AudioSegment.empty()

    for i, audio_file in enumerate(audio_clips):
        st.write(f"Merging audio {i + 1}/{len(audio_clips)}.")
        audio = AudioSegment.from_mp3(audio_file)
        combined += audio

    combined.export(output_file_name, format="mp3")
    st.success(f"Successfully created {output_file_name}!")

def cleanup(files):
    for file in files:
        os.remove(file)

def main():
    st.title("Mashup WebApp 🎶")
    st.write("Create a custom mashup of your favorite singer's songs by downloading YouTube videos and merging their audios.")

    # Input fields for user input
    singer_name = st.text_input("Enter the Singer Name (e.g. 'Sharry Maan')", value="Sharry Maan")
    number_of_videos = st.number_input("Enter the Number of Videos to Download (must be greater than 1)", min_value=2, step=1, value=2)
    audio_duration = st.number_input("Enter Audio Duration for Each Video (in seconds, must be greater than 20)", min_value=20, step=1, value=30)
    output_file_name = st.text_input("Enter the Output File Name (e.g. 'mashup.mp3')", value="mashup.mp3")

    # When user clicks the button, execute the mashup creation
    if st.button("Create Mashup"):
        try:
            # Step 1: Download videos
            st.write("Starting video downloads...")
            downloaded_files = download_videos(singer_name, number_of_videos)

            # Step 2: Convert videos to audio and trim
            st.write("Processing videos to audio...")
            audio_clips = convert_videos_to_audio(downloaded_files, audio_duration)

            # Step 3: Merge audio clips
            st.write("Merging audio files...")
            merge_audios(audio_clips, output_file_name)

            # Step 4: Cleanup downloaded files
            cleanup(downloaded_files)

            st.write(f"Mashup created successfully! Download your file: {output_file_name}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
