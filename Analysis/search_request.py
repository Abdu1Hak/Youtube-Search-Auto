from googleapiclient.discovery import build

import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)

Query = input("Include your Search Keyword: ")
include2 = input("Include your first keyword: ")
include3 = input("Include your second keyword: ")
include4 = input("Include your third keyword: ")
include5 = input("Include your fourth keyword: ")
include6 = input("Include your fifth keyword: ")

keywords = [Query, include2, include3, include4, include5, include6]
search_query = Query

# Search user lesser words
def get_channel_ids(query = f"{Query}", max_pages=20, results_per_page=50):
    channel_ids = set()
    next_page_token = None 

    for _ in range(max_pages):
        request = youtube.search().list(
                part="snippet",
                maxResults=results_per_page,
                q=query,
                type="channel",
                pageToken = next_page_token
            )

        response = request.execute()

        channel_ids.update(item["snippet"]["channelId"] for item in response['items']) #
        next_page_token = response.get("nextPageToken")
        
        # If no next page
        if not next_page_token:
            break 

    return channel_ids


og_channel_ids = get_channel_ids()
channel_ids = list(og_channel_ids)

