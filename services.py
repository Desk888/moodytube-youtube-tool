import pandas as pd
import os
from psycopg2 import extras
from db import conn, cursor, ensure_tables_exist
import isodate

class ChannelStatsManager():

    def get_channel_statistics(self, youtube, channel_id):
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        channel_stats = []
        
        if 'items' in response and len(response['items']) > 0:
            for item in response['items']:
                snippet = item['snippet']
                statistics = item['statistics']
                channel_stats.append([
                    item['id'],
                    snippet['title'],              
                    snippet['description'],        
                    int(statistics['viewCount']),       
                    int(statistics['subscriberCount']), 
                    int(statistics['videoCount']),      
                    snippet['publishedAt'],        
                ])
        
   
        df = pd.DataFrame(channel_stats, columns=['channel_id', 'title', 'description', 'view_count', 'subscriber_count', 'video_count', 'published_at'])
        file_path = f'./data/channel_data/channel_stats_id_{channel_id}.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        print(df)
        
        self.store_channel_data(df)
        return df

    def store_channel_data(self, df):
        data = df.to_dict('records')
        with conn:
            with conn.cursor() as cur:
                extras.execute_batch(cur, """
                INSERT INTO channels_data (channel_id, title, description, view_count, subscriber_count, video_count, published_at)
                VALUES (%(channel_id)s, %(title)s, %(description)s, %(view_count)s, %(subscriber_count)s, %(video_count)s, %(published_at)s)
                ON CONFLICT (channel_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    view_count = EXCLUDED.view_count,
                    subscriber_count = EXCLUDED.subscriber_count,
                    video_count = EXCLUDED.video_count,
                    published_at = EXCLUDED.published_at
                """, data)

class CommentsManager():
    
    def select_all_videos(self, youtube, channel_id):
        response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        videos = []
        next_page_token = None
        
        while True:
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            for item in playlist_response['items']:
                videos.append(item['snippet']['resourceId']['videoId'])
            
            next_page_token = playlist_response.get('nextPageToken')
            if next_page_token is None:
                break
        
        return videos

    def get_comments_data(self, youtube, video_id):
        comments = []
        next_page_token = None
        
        while True:
            try:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append([
                        video_id,
                        comment['authorDisplayName'],
                        comment['publishedAt'], 
                        comment['updatedAt'],
                        int(comment['likeCount']),
                        comment['textDisplay']
                    ])
                
                next_page_token = response.get('nextPageToken')
                if next_page_token is None:
                    break
            except Exception as e:
                print(f"An error occurred while fetching comments for video {video_id}: {str(e)}")
                break

        df = pd.DataFrame(comments, columns=['video_id', 'author', 'published_at', 'updated_at', 'like_count', 'text'])
        file_path = f'./data/comments_data/comments_videoid_{video_id}.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"Saved comments for video {video_id}")

        self.store_comments_data(df)
        
        return df
        
    def store_comments_data(self, df):
        data = df.to_dict('records')
        with conn:
            with conn.cursor() as cur:
                extras.execute_batch(cur, """
                INSERT INTO comments_data (video_id, author, published_at, updated_at, like_count, text)
                VALUES (%(video_id)s, %(author)s, %(published_at)s, %(updated_at)s, %(like_count)s, %(text)s)
                ON CONFLICT (video_id, author, published_at) DO UPDATE SET
                    updated_at = EXCLUDED.updated_at,
                    like_count = EXCLUDED.like_count,
                    text = EXCLUDED.text
                """, data)

class VideosDurationManager():
    
    def get_videos_average_duration(self, youtube, channel_id):
        request = youtube.videos().list(
            part="contentDetails",
            chart="mostPopular",
            regionCode="US",
            maxResults=50,
        )
        response = request.execute()
        videos = []
        
        for item in response['items']:
            duration = isodate.parse_duration(item['contentDetails']['duration'])
            formatted_duration = str(duration)
            videos.append([
                item['id'],
                formatted_duration
            ])
        
        df = pd.DataFrame(videos, columns=['video_id', 'duration'])
        file_path = f'./data/videos_data/videos_duration_id_{channel_id}.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        print(df)
        
        self.store_videos_data(df)
        return df
    
    def store_videos_data(self, df):
        data = df.to_dict('records')
        with conn:
            with conn.cursor() as cur:
                extras.execute_batch(cur, """
                INSERT INTO video_duration_data (video_id, duration)
                VALUES (%(video_id)s, %(duration)s)
                ON CONFLICT (video_id) DO UPDATE SET
                    duration = EXCLUDED.duration
                """, data)