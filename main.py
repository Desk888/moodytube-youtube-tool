# /////////////////////////////////////////////////////////////////////////////////////////////

# --- Instructions ---

"""
MoodyTube || YouTube Sentiment Analysis Tool || Initial v1.0.0 || Data Only

The main functionality of this script, is to extract comments for all active YouTube videos for a given channel.
Once the data gets extracted through requests made to the YouTube Data API v3, the data gets cleaned with Pandas, 
and then stored in the in the apposited data folder, in a .csv format. Once the data is extracted a ML model will take
the data and run a sentiment analysis and return a final description of how users are engaging with the channel's content.

Future Implementations:

1. Setup an Airflow system to create a data pipeline to automate data extraction process and storage. (On Hold)
2. Develop ML model for final sentiment analysis (in progress)

For further information, review the README.md for the final documentation.
"""
# /////////////////////////////////////////////////////////////////////////////////////////////

# --- Libraries ---

from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from db import conn
from services import ChannelDataManager, CommentsDataManager, VideosManager

# /////////////////////////////////////////////////////////////////////////////////////////////

# --- Configurations --- 

load_dotenv()
api_key = os.environ.get('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)
channel_id = ['UCIE0qJTh0mRbGq880RQh2TA'] # Add channel ID here

# /////////////////////////////////////////////////////////////////////////////////////////////
            
# --- Main Execution ---

if __name__ == "__main__":
    channel_stats_manager = ChannelDataManager()
    comments_manager = CommentsDataManager()
    videos_manager = VideosManager()

for channels in channel_id:
    print(f"Processing data for channel: {channel_id}")
    
    # Get channel statistics
    channel_stats_manager.get_channel_statistics(youtube, channel_id)

    # Get all active videos in the channel
    videos = comments_manager.select_all_videos(youtube, channel_id)

    # Get comments data for each video
    for video_id in videos:
        comments_manager.get_comments_data(youtube, video_id)
    
    # Get videos average duration
    videos_manager.get_videos_average_duration(youtube, channel_id)


conn.close() # Close connection to the database
