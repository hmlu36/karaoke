from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()
API_KEY = os.getenv('API_KEY')
print('API_KEY:', API_KEY)
username = '@@q19660215'

# 取得 channelId
url = f'https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={username}&key={API_KEY}'
resp = requests.get(url)
data = resp.json()
if 'items' in data and data['items']:
    channel_id = data['items'][0]['id']
else:
    # 如果 forUsername 查不到，改用 search
    search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={username}&key={API_KEY}'
    resp = requests.get(search_url)
    data = resp.json()
    channel_id = data['items'][0]['snippet']['channelId']
print('channelId:', channel_id)

videos = []
next_page_token = ''
while True:
    search_url = (
        f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}'
        f'&channelId={channel_id}&part=snippet,id&order=date&maxResults=50&type=video'
        + (f'&pageToken={next_page_token}' if next_page_token else '')
    )
    print(search_url)
    resp = requests.get(search_url)
    data = resp.json()
    for item in data.get('items', []):
        title = item['snippet']['title']
        #if 'Karaoke伴奏' in title:
        idx = title.rfind(')')
        if idx != -1 and idx + 1 < len(title):
            parsed_title = title[idx+1:].strip()
            if not parsed_title:
                parsed_title = title[:idx].strip()
        else:
            parsed_title = title

        # 先清理標題
        clean_title = title.replace('(伴奏版)', '').replace('(DIY卡拉OK字幕)', '').replace('(Karaoke伴奏)', '').strip()
        parts = clean_title.split('-')
        if len(parts) > 1:
            artist = parts[1].strip()
            song_title = parts[0].strip()
        else:
            artist = 'Unknown Artist'
            song_title = clean_title
        videos.append({
            'id': item['id']['videoId'],
            'title': song_title,
            'artist': artist
        })
    next_page_token = data.get('nextPageToken')
    if not next_page_token:
        break

print(videos)

df = pd.DataFrame(videos)
df.to_excel('songs.xlsx', index=False)
print("已匯出為 songs.xlsx")