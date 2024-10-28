import os
import sys
import json
import time
from youtube_transcript_api import YouTubeTranscriptApi

def process_video_requests(folder_name):
    # Path to the output.json file within the folder
    output_file_path = os.path.join(folder_name, 'output.json')

    # Check if the file exists
    if not os.path.exists(output_file_path):
        print(f"The file {output_file_path} does not exist.")
        return

    # Read output.json and load the JSON content
    with open(output_file_path, 'r', encoding='utf-8') as file:
        video_data = json.load(file)  # Load the content as a list of dictionaries (JSON array of objects)

    # List to store transcriptions and errors
    transcriptions_data = []
    
    # Counter for processed videos
    video_counter = 0

    # Iterate through the array of videos and limit to the first 20 for testing
    for index, video in enumerate(video_data, start=1):
        # if index > 20:  # You can limit to only 20 videos for the test
        #     break

        video_id = video.get('id')  # Get the video ID from the JSON object
        title = video.get('title')  # Get the video title from the JSON object
        if video_id:
            try:
                # Retrieve the transcript using YouTubeTranscriptApi, specifying the language (Spanish in this case)
                print(f"Getting Spanish transcript for video {index} with ID: {video_id}")
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])

                # Convert transcript to plain text
                transcription_text = ' '.join([entry['text'] for entry in transcript])

                # Store transcription in JSON, including title
                transcriptions_data.append({
                    "id": video_id,
                    "title": title,
                    "transcription": transcription_text,
                    "status": "success"
                })

                print(f"Transcript obtained for video {index} (ID: {video_id})")

            except Exception as e:
                # Handle errors like videos without transcripts or network issues
                transcriptions_data.append({
                    "id": video_id,
                    "title": title,
                    "error": str(e),
                    "status": "failed"
                })
                print(f"Error getting transcript for video {index} (ID: {video_id}): {str(e)}")

            # Increment the counter for processed videos
            video_counter += 1

            # Wait 1 second before making the next request
            time.sleep(1)

    # Save all transcriptions and errors to a JSON file
    transcriptions_file_path = os.path.join(folder_name, 'transcriptions.json')
    with open(transcriptions_file_path, 'w', encoding='utf-8') as transcriptions_file:
        json.dump(transcriptions_data, transcriptions_file, ensure_ascii=False, indent=4)

    print(f"All transcriptions and errors saved to {transcriptions_file_path}")
    print(f"Total videos processed: {video_counter}")

if __name__ == '__main__':

    # Check if folder name is passed as an argument
    if len(sys.argv) < 2:
        print("Usage: python video_requests.py <folder_name>")
        sys.exit(1)

    # Get the folder name from the arguments
    folder_name = sys.argv[1]

    # Process the requests for videos in output.json
    process_video_requests(folder_name)
