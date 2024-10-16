import streamlit as st
import urllib.parse
from pytube import Search
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os

# Function to download videos from YouTube based on singer name
def download_videos(singer_name, number_of_videos):
    # Encode singer name to handle special characters in the URL
    singer_name_encoded = urllib.parse.quote(singer_name)
    search_query = Search(singer_name_encoded)
    results = search_query.results
    downloaded_files = []

    if len(results) < number_of_videos:
        st.warning(f"Only {len(results)} videos found. Downloading all of them.")
        number_of_videos = len(results)

    for i, video in enumerate(results[:number_of_videos]):
        st.write(f"Downloading video {i + 1}/{number_of_videos}: {video.title}")
        video_file = video.streams.filter(only_audio=True).first().download(filename=f"video_{i}.mp4")
        downloaded_files.append(video_file)

    return downloaded_files

# Function to convert videos to audio and trim the audio
def convert_videos_to_audio(downloaded_files, audio_duration):
    audio_clips = []

    for i, video_file in enumerate(downloaded_files):
        st.write(f"Processing video {i + 1}/{len(downloaded_files)}: Converting to audio and trimming to {audio_duration} seconds.")
        video_clip = VideoFileClip(video_file)
        audio_clip = video_clip.audio.subclip(0, audio_duration)
        audio_clip.write_audiofile(f"audio_{i}.mp3")
        audio_clips.append(f"audio_{i}.mp3")
        video_clip.close()

    return audio_clips

# Function to merge all audio clips into one
def merge_audios(audio_clips, output_file_name):
    combined = AudioSegment.empty()

    for i, audio_file in enumerate(audio_clips):
        st.write(f"Merging audio {i + 1}/{len(audio_clips)}.")
        audio = AudioSegment.from_mp3(audio_file)
        combined += audio

    combined.export(output_file_name, format="mp3")
    st.success(f"Successfully created {output_file_name}!")

# Function to cleanup downloaded files after processing
def cleanup(files):
    for file in files:
        os.remove(file)

def main():
    st.title("Mashup WebApp 🎶")
    st.write("Create a custom mashup of your favorite singer's songs by downloading YouTube videos and merging their audios.")

    # Input fields for user input
    singer_name = st.text_input("Enter the Singer Name (e.g. 'Sharry Maan')", value="Sharry Maan")
    number_of_videos = st.number_input("Enter the Number of Videos to Download (must be greater than 10)", min_value=10, step=1, value=10)
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
            cleanup(downloaded_files + audio_clips)

            st.write(f"Mashup created successfully! Download your file: {output_file_name}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
