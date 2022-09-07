import os
from flask import send_file
from pytube import YouTube, exceptions
from io import BytesIO

def resolution_generator(resolutions):
    for res in resolutions:
        yield res


def download_video(videoId):
    url = f"https://www.youtube.com/watch?v={videoId}"
    filename = f"{videoId}.mp4"
    buffer = BytesIO()
    rgen = resolution_generator(['360p', '480p', '720p', '144p'])

    yt_video = YouTube(url)
    video = None

    while video is None:
        res = next(rgen)
        print('trying ', res)
        try:
            video = yt_video.streams.get_by_resolution(res)
        except StopIteration:
            print('Could not manually select the proper resolution\nRetrying with the highest resolution')
            try:
                video = yt_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            except Exception as e:
                return "Unable to download video"
        except exceptions.LiveStreamError as e:
            return f"video: {videoId} is streaming live and cannot be loaded"

    video.stream_to_buffer(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=filename)

