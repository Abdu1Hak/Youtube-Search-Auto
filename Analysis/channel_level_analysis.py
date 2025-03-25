from googleapiclient.discovery import build
from IPython.display import  JSON
import pandas as pd
from googleapiclient.errors import HttpError
from Analysis.search_request import channel_ids, keywords

import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

pd.set_option('display.max_rows', None) 


api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)  # service object with the build() function to access various resources



def channel_level_analysis(youtube, channel_ids): 

    all_data = [] 
    MAX_CHANNELS = 50

    try:
        for i in range(0, len(channel_ids), MAX_CHANNELS):
            batch_ids = ','.join(channel_ids[i:i+MAX_CHANNELS])

            request = youtube.channels().list(
                part="snippet,contentDetails,statistics,topicDetails", # Topic Details return Topic Categories for Niche Targeting 
                id= batch_ids,
            ) 

            response = request.execute() # Execute & return python dictionary
                
            for item in response['items']:
                
                if int(item['statistics'].get("subscriberCount", "0")) < 50000:
                    continue # Skip current Iteration
                
                topics = item.get("topicDetails", {}).get("topicCategories", [])

                for keyword in keywords:
                    for topic in topics:
                        if topic == f"https://en.wikipedia.org/wiki/{keyword}":

                            data = {'channelName': item["snippet"].get('title', 'N/A'),
                                    'subscriber': int(item["statistics"].get('subscriberCount', "0")),
                                    'totalVideos': int(item["statistics"].get('videoCount', "0")),
                                    'playlistId': item.get("contentDetails", {}).get('relatedPlaylists',{}).get('uploads','N/A'),
                                    'channelId': item['id'],
                                    'description': item["snippet"].get("description", "N/A")
                            }
                        
                            all_data.append(data)
                             

    except HttpError as e:
        print(f"API Error: {e}")

    df = pd.DataFrame(all_data)
    return df

channel_analysis_id = channel_level_analysis(youtube, channel_ids)
playlist_id = channel_analysis_id['playlistId'].tolist()




def get_video_ids(youtube, playlist_id):

    total_video_ids = {}

    for playlist in playlist_id:
        video_ids = []
        request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist,
                maxResults = 8
        )

        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
        
        total_video_ids[playlist] = video_ids 
    
    return total_video_ids
        
collection_video_ids = get_video_ids(youtube, playlist_id)


