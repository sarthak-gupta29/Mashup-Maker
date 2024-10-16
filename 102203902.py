import sys
import os
from pytube import Search
from moviepy.editor import VideoFileClip, concatenate_audioclips

def download_videos(singer_name, number_of_videos):
    search_query = Search(singer_name)
    results = search_query.results
    downloaded_files = []
    
    if len(results) < number_of_videos:
        print(f"Only {len(results)} videos found. Downloading all of them.")
        number_of_videos = len(results)

    for i, video in enumerate(results[:number_of_videos]):
        try:
            print(f"Downloading video {i + 1}/{number_of_videos}: {video.title}")
            video_file = video.streams.filter(only_audio=True).first().download(filename=f"video_{i}.mp4")
            downloaded_files.append(video_file)
        except Exception as e:
            print(f"Error downloading video {i + 1}: {e}. Skipping this video.")

    return downloaded_files

def convert_videos_to_audio(downloaded_files, audio_duration):
    audio_clips = []

    for i, video_file in enumerate(downloaded_files):
        try:
            print(f"Processing video {i + 1}/{len(downloaded_files)}: Converting to audio and cutting {audio_duration} seconds.")
            video_clip = VideoFileClip(video_file)
            audio_clip = video_clip.audio.subclip(0, audio_duration)
            audio_clips.append(audio_clip)
            video_clip.close()
        except Exception as e:
            print(f"Error processing video {i + 1}: {e}. Skipping this file.")

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
