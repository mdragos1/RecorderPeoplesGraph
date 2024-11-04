import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from tqdm import tqdm

API_KEY = "KEY"
CHANNEL_ID = 'UChDQ6nYN6XyRU-8IEgbym1g'
CHANNEL_USERNAME = '@RecorderRomania'

# Step 1: Search for the channel using the @username
search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={CHANNEL_USERNAME}&key={API_KEY}'
search_response = requests.get(search_url).json()

# Check if the response contains any channel items
if 'items' in search_response and len(search_response['items']) > 0:
    # Extract the channel ID
    channel_id = search_response['items'][0]['snippet']['channelId']
    print(f'Channel ID: {channel_id}')

    # Step 2: Use the channel ID to get the total video count
    stats_url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={API_KEY}'
    stats_response = requests.get(stats_url).json()

    # Extract the total number of videos
    if 'items' in stats_response and len(stats_response['items']) > 0:
        video_count = stats_response['items'][0]['statistics']['videoCount']
        print(f'Total number of videos: {video_count}')
    else:
        print("Error: Couldn't retrieve channel statistics.")
else:
    print("Error: Channel not found.")


# Initialize the base URL
base_url = 'https://www.googleapis.com/youtube/v3/'

# Step 1: Get the Uploads Playlist ID
url = f'{base_url}channels?part=contentDetails&id={CHANNEL_ID}&key={API_KEY}'
response = requests.get(url).json()
uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Step 2: Get all video details from the uploads playlist
videos_data = []
next_page_token = None
i=1
print(f"Fetching videos from the playlist...")
with open('recorder_channel_videos.jsonl', 'w', encoding='utf-8') as file:
    while True:
        print(f"Page {i}/9")
        playlist_url = f'{base_url}playlistItems?part=contentDetails,snippet&playlistId={uploads_playlist_id}&maxResults=50&key={API_KEY}'
        if next_page_token:
            playlist_url += f'&pageToken={next_page_token}'

        response = requests.get(playlist_url).json()
        
        for item in tqdm(response['items']):
            video_id = item['contentDetails']['videoId']
            title = item['snippet']['title']
            published_at = item['snippet']['publishedAt']
            description = item['snippet']['description']

            # Fetch transcript if available
            transcript_text = ""
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([t['text'] for t in transcript])
            except (TranscriptsDisabled, NoTranscriptFound):
                transcript_text = "Transcript not available"
                continue
            
            # Create a JSON object for each video
            video_data = {
                "video_id": video_id,
                "title": title,
                "published_at": published_at,
                "description": description,
                "transcript": transcript_text
            }

            # Append video data
            videos_data.append([video_id, title, published_at, description, transcript_text])
            file.write(json.dumps(video_data, ensure_ascii=False) + '\n')

        # Check for next page
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
        i+=1
   
print("JSONL file with transcripts has been created successfully!")