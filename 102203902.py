# 102203902.py
import yt_dlp
import moviepy.editor as mp
import os
import zipfile

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

# Example usage
video_urls = [
    'https://www.youtube.com/watch?v=example1',  # Replace with actual URLs
    'https://www.youtube.com/watch?v=example2'
]
output_folder = 'downloads/audio_files'  # Update this to your path
merged_output = os.path.join(output_folder, 'merged_audio.mp3')
zip_output = os.path.join(output_folder, 'merged_audio.zip')

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Download videos
for video_url in video_urls:
    download_video(video_url, output_folder)

# Merge audio files
merge_audio_files(output_folder, merged_output)

# Zip the merged file
zip_audio_file(merged_output, zip_output)
