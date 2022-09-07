from googleapiclient.discovery import build
from Constants import api_key
import pandas as pd

def get_video_details(playlistId, username, maxResults=5):
    try:
        youtube_build = build('youtube', 'v3', developerKey=api_key)
        response_playlist = youtube_build.playlistItems().list(
            part="snippet",
            playlistId=playlistId,
            maxResults=maxResults
        ).execute()
        data = {
            'username': [],
            'channelTitle': [],
            'title': [],
            'publishedAt': [],
            'thumbnailLink': [],
            'videoLink': [],
            'videoId': []
        }
        for item in response_playlist['items']:
            snippet = item['snippet']
            data['username'].append(username)
            data['channelTitle'].append(snippet['channelTitle'])
            data['title'].append(snippet['title'])
            data['publishedAt'].append(snippet['publishedAt'])
            data['thumbnailLink'].append(snippet['thumbnails']['default']['url'])
            videoId = snippet['resourceId']['videoId']
            data['videoId'].append(videoId)
            videoLink = f"https://www.youtube.com/watch?v={videoId}"
            data['videoLink'].append(videoLink)

        data_temp = {
            'viewCount': [],
            'likeCount': [],
            'commentCount': []
        }

        for videoId in data['videoId']:
            response_video = youtube_build.videos().list(
                part="statistics",
                id=videoId
            ).execute()
            data_temp['viewCount'].append(response_video['items'][0]['statistics']['viewCount'])
            data_temp['likeCount'].append(response_video['items'][0]['statistics']['likeCount'])
            data_temp['commentCount'].append(response_video['items'][0]['statistics']['commentCount'])

        data = {**data, **data_temp}
        # data = [dict(zip(data, v)) for v in zip(*data.values())]
        data = pd.DataFrame(data)
        return data
    except Exception as e:
        print(e)
        return None
