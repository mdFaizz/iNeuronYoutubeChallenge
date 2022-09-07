import requests
import re
from bs4 import BeautifulSoup

def get_channel_Ids(youtube_url):
    try:
        response = requests.get(youtube_url)
    except Exception as e:
        print(e)
        return 'INVALID'
    if response.ok:
        doc = BeautifulSoup(response.text, 'html.parser')
    else:
        youtube_url = youtube_url.replace("user", "c")
        response = requests.get(youtube_url)
        doc = BeautifulSoup(response.text, 'html.parser')
    channelId = doc.find('link', rel=re.compile("canonical"))['href'].split('/')[-1]
    return channelId