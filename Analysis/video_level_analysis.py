from googleapiclient.discovery import build
from IPython.display import  JSON
import pandas as pd
from datetime import datetime 
from Analysis.channel_level_analysis import channel_analysis_id, playlist_id, collection_video_ids

api_key = "AIzaSyCUz0dbMXmuxgN0upbqjhlh9xTM3kexR5M"
pd.set_option('display.max_rows', None) 


api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)  

# 2 Main Coniditonals: 
#   1. Average of 30 k viewers
#   2. Upload Scedule is minimum twice a month

def fix_num_format(number):
    if number >= 1000000:
        return f"{number/1000000:.2f}M"
    elif number >= 1000:
        return f"{number/1000:.2f}K"
    else:
        return number 

def average_of_fifty_and_consistent(youtube, collection_video_ids, playlist_id):
     
    final_data = []

    for playlist in playlist_id:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id= ",".join(collection_video_ids[playlist])
        )

        response = request.execute()

        total = 0
        num_of_videos = 0
        published_months = []

        for video in response['items']:
            
            viewCount = int(video["statistics"].get("viewCount", 0))
            total += viewCount
            num_of_videos += 1


            published_at = video["snippet"].get("publishedAt")
            published_at = pd.to_datetime(published_at) # Convert to a datetime object

            published_months.append(published_at)

            
        
        average_view_count = int(total/num_of_videos)
        
        if average_view_count > 30000:
            
            monthly_uploads = {}
            for publish in published_months: 
                month_key = publish.strftime('%Y-%m')
                monthly_uploads[month_key] = monthly_uploads.get(month_key, 0) + 1 # Create a dict with month/yr as string key and its count as val
            
            current_month = datetime.now().strftime('%Y-%m')
            consecutive_check = True
            required_count = 1

            # 1. Check at least 2 videos in every month 
            for month, count in monthly_uploads.items():
                if month == current_month:
                    continue # skip 
                
                if count < required_count:
                    consecutive_check = False 
                    break 
                    
            # Create the Final Data 
            if len(published_months) >= 2 and consecutive_check:
                channel_id = channel_analysis_id[channel_analysis_id['playlistId'] == playlist]['channelId'].iloc[0]
                channel_name = channel_analysis_id[channel_analysis_id['playlistId'] == playlist]['channelName'].iloc[0]
                subscriber = channel_analysis_id[channel_analysis_id['playlistId'] == playlist]['subscriber'].iloc[0] # retrieve val from first row
                totalVids = channel_analysis_id[channel_analysis_id['playlistId'] == playlist]['totalVideos'].iloc[0]
                description = channel_analysis_id[channel_analysis_id['playlistId'] == playlist]['description'].iloc[0]

                fixed_sub_count = fix_num_format(subscriber)
                fixed_views_count = fix_num_format(average_view_count)

                data = {
                    'Channel Name':channel_name,
                    'Average Views': fixed_views_count,
                    'Total Videos': totalVids,
                    'Description': description,
                    'Subscribers': fixed_sub_count
                }
                final_data.append(data)

    df = pd.DataFrame(final_data)
    return df

final = average_of_fifty_and_consistent(youtube, collection_video_ids, playlist_id)









