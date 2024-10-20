import sys
import os
import re
import yt_dlp
from moviepy.editor import AudioFileClip, concatenate_audioclips

def sanitize_filename(title):
    # Remove any characters that are invalid for filenames
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
        'noplaylist': True,  # Avoid downloading playlists
    }

    search_url = f"https://www.youtube.com/results?search_query={singer_name}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(search_url, download=False)
            entries = info_dict['entries']
            if len(entries) < number_of_videos:
                print(f"Only {len(entries)} videos found. Downloading all of them.")
                number_of_videos = len(entries)

            for i in range(number_of_videos):
                video_title = sanitize_filename(entries[i]['title'])
                print(f"Downloading video {i + 1}/{number_of_videos}: {video_title}")
                ydl.download([entries[i]['url']])
                downloaded_files.append(f"{video_title}.mp3")
                
        except Exception as e:
            print(f"Error downloading videos: {e}")
            return []

    return downloaded_files

def convert_videos_to_audio(downloaded_files, audio_duration):
    audio_clips = []

    for i, video_file in enumerate(downloaded_files):
        try:
            print(f"Processing audio {i + 1}/{len(downloaded_files)}: Trimming to {audio_duration} seconds.")
            audio_clip = AudioFileClip(video_file).subclip(0, audio_duration)
            audio_clips.append(audio_clip)
        except Exception as e:
            print(f"Error processing audio {i + 1}: {e}. Skipping this file.")

    return audio_clips

def merge_audios(audio_clips, output_file_name):
    print(f"Merging {len(audio_clips)} audio clips into {output_file_name}")
    merged_audio = concatenate_audioclips(audio_clips)
    merged_audio.write_audiofile(output_file_name)

def cleanup(downloaded_files):
    for file in downloaded_files:
        os.remove(file)

def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    try:
        singer_name = sys.argv[1]
        number_of_videos = int(sys.argv[2])
        audio_duration = int(sys.argv[3])
        output_file_name = sys.argv[4]

        if number_of_videos < 2:
            print("Please specify a number of videos greater than 2.")
            sys.exit(1)

        if audio_duration < 20:
            print("Please specify an audio duration greater than 20 seconds.")
            sys.exit(1)

        # Step 1: Download videos
        downloaded_files = download_videos(singer_name, number_of_videos)

        # Step 2: Convert videos to audio and cut duration
        audio_clips = convert_videos_to_audio(downloaded_files, audio_duration)

        # Step 3: Merge audio clips
        merge_audios(audio_clips, output_file_name)

        # Step 4: Cleanup
        cleanup(downloaded_files)

        print(f"Successfully created {output_file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
