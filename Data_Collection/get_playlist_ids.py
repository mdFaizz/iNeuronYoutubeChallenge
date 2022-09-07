from googleapiclient.discovery import build
from Constants import api_key

def get_playlist_ids(channelId):
    try:
        youtube_build = build('youtube', 'v3', developerKey=api_key)
        response = youtube_build.channels().list(
            part='contentDetails',
            id=channelId
        ).execute()
        playlistId = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return playlistId
    except Exception as e:
        print(e)
        return "INVALID"

