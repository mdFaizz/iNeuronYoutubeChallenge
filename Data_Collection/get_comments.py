from googleapiclient.discovery import build
from Constants import api_key


def get_response_comments(youtube_build, videoId, nextPageToken=None):
    temp = []
    response_comments = youtube_build.commentThreads().list(
        part='snippet,replies',
        videoId=videoId,
        pageToken=nextPageToken
    ).execute()
    temp.extend(response_comments['items'])
    if 'nextPageToken' in response_comments:
        response = get_response_comments(youtube_build, videoId, nextPageToken=response_comments['nextPageToken'])
        if response:
            temp.extend(response)
    else:
        return temp
    return temp


def get_comments(videoId, videotitle):
    try:
        replies_keys = ['authorName', 'comment', 'likeCount', 'publishedAt']
        replies_vals = ['authorDisplayName', 'textOriginal', 'likeCount', 'publishedAt']

        youtube_build = build('youtube', 'v3', developerKey=api_key)
        response_comments = get_response_comments(youtube_build, videoId)
        commentCount = len(response_comments)
        comments = {
            'videoId': videoId,
            'title': videotitle,
            'commentCount': commentCount,
            'comments': []
        }
        for response in response_comments:
            totalReplyCount = response['snippet']['totalReplyCount']
            if totalReplyCount != 0:
                if 'replies' in response:
                    replies = [{k: val['snippet'][v] for k, v in zip(replies_keys, replies_vals)}
                               for val in response['replies']['comments']]
                else:
                    print('No reply although totalReplyCount is ', totalReplyCount)
                    replies = []
            else:
                replies = []
            comments['comments'].append(
                {
                    'authorName': response['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'comment': response['snippet']['topLevelComment']['snippet']['textOriginal'],
                    'publishedAt': response['snippet']['topLevelComment']['snippet']['publishedAt'],
                    'likeCount': response['snippet']['topLevelComment']['snippet']['likeCount'],
                    'replies': replies
                })

    except Exception as e:
        print(e)
        print(response)
        comments = {
            'videoId': videoId,
            'commentCount': 0,
            'comments': []
        }

    return comments