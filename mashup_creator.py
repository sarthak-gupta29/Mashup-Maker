import streamlit as st
import yt_dlp
import os
from moviepy.editor import AudioFileClip, concatenate_audioclips
import ffmpeg

# Ensure the download directory exists
DOWNLOAD_DIR = './downloads/'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_videos(singer_name, number_of_videos):
    search_query = f"ytsearch{number_of_videos}:{singer_name}"
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best available audio
        'noplaylist': True,
        'extract-audio': True,
        'audio-format': 'mp3',  # Attempt to convert to mp3
        'outtmpl': os.path.join(DOWNLOAD_DIR, 'video_%(id)s.%(ext)s'),  # Save to the download directory
    }
    downloaded_files = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            entries = info.get('entries', [])[:number_of_videos]
            for entry in entries:
                video_id = entry['id']
                file_ext = entry.get('ext', 'mp3')  # Default to mp3, though it may not always be correct
                file_name = os.path.join(DOWNLOAD_DIR, f"video_{video_id}.{file_ext}")

                # Convert to mp3 if not already in mp3
                if file_ext != 'mp3':
                    mp3_file = os.path.join(DOWNLOAD_DIR, f"video_{video_id}.mp3")
                    ffmpeg.input(file_name).output(mp3_file).run(overwrite_output=True)
                    downloaded_files.append(mp3_file)  # Append mp3 file instead
                else:
                    downloaded_files.append(file_name)  # Append original mp3 file

    except Exception as e:
        st.warning(f"An error occurred while downloading the videos: {e}")

    return downloaded_files

def convert_videos_to_audio(downloaded_files, audio_duration):
    audio_clips = []
    for i, video_file in enumerate(downloaded_files):
        try:
            if os.path.exists(video_file):  # Ensure file exists
                trimmed_file = os.path.join(DOWNLOAD_DIR, f"trimmed_audio_{i}.mp3")
                # Using MoviePy for processing
                with AudioFileClip(video_file) as audio:
                    # Trim the audio to the specified duration
                    trimmed_audio = audio.subclip(0, min(audio_duration, audio.duration))
                    trimmed_audio.write_audiofile(trimmed_file)
                    audio_clips.append(trimmed_file)
            else:
                st.warning(f"File not found: {video_file}. Skipping this video.")
        except Exception as e:
            st.warning(f"Error processing video {i + 1}. Skipping this video: {e}")
    return audio_clips

def merge_audios(audio_clips, output_file_name):
    output_file_path = os.path.join(DOWNLOAD_DIR, output_file_name)
    try:
        # Use MoviePy to concatenate the audio clips
        clips = [AudioFileClip(clip) for clip in audio_clips]
        final_clip = concatenate_audioclips(clips)

        # Save the merged audio
        final_clip.write_audiofile(output_file_path)
        st.success(f"Successfully created {output_file_name}!")

        # Close all clips to free resources
        final_clip.close()
        for clip in clips:
            clip.close()

    except Exception as e:
        st.error(f"An error occurred while merging audio files: {e}")

    return output_file_path

def cleanup(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def main():
    st.title("Mashup WebApp 🎶")
    st.write("Create a custom mashup of your favorite singer's songs by downloading YouTube videos and merging their audios.")

    # Input fields for user input
    singer_name = st.text_input("Enter the Singer Name (e.g. 'Arijit Singh')", value="Arijit Singh")
    number_of_videos = st.number_input("Enter the Number of Videos to Download (must be greater than 2)", min_value=2, step=1, value=2)  # Minimum 2 videos
    audio_duration = st.number_input("Enter Audio Duration for Each Video (in seconds, must be greater than 30)", min_value=30, step=1, value=30)  # Minimum 30 seconds
    output_file_name = st.text_input("Enter the Output File Name (e.g. 'mashup.mp3')", value="mashup.mp3")

    # When user clicks the button, execute the mashup creation
    if st.button("Create Mashup"):
        try:
            # Step 1: Download videos
            downloaded_files = download_videos(singer_name, number_of_videos)

            # Step 2: Convert videos to audio and trim
            audio_clips = convert_videos_to_audio(downloaded_files, audio_duration)

            # Step 3: Merge audio clips
            if len(audio_clips) > 0:
                output_file_path = merge_audios(audio_clips, output_file_name)

                # Step 4: Cleanup downloaded and processed files
                cleanup(downloaded_files + audio_clips)

                # Provide download link for the final mashup file
                st.write(f"Mashup created successfully! Download your file below:")
                with open(output_file_path, 'rb') as f:
                    st.download_button(label="Download Mashup", data=f, file_name=output_file_name)

            else:
                st.warning("No valid audio clips could be processed for the mashup.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
