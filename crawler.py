from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv('API_KEY')
print('API_KEY:', API_KEY)
username = 'davidpinpunhuang8372'

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
    resp = requests.get(search_url)
    data = resp.json()
    for item in data.get('items', []):
        title = item['snippet']['title']
        if '伴奏版' in title:
            idx = title.rfind(')')
            if idx != -1 and idx + 1 < len(title):
                parsed_title = title[idx+1:].strip()
                if not parsed_title:
                    parsed_title = title[:idx].strip()
            else:
                parsed_title = title
                
            videos.append({
                'id': item['id']['videoId'],
                'title': title.replace('(伴奏版)', '').replace('(DIY卡拉OK字幕)', '').strip(),
                'artist': item['snippet']['channelTitle']
            })
    next_page_token = data.get('nextPageToken')
    if not next_page_token:
        break

print(videos)



result = []
for item in videos:
    if '-' in item['title']:
        artist, title = item['title'].split('-', 1)
        result.append({
            'id': item['id'],
            'title': title.strip(),
            'artist': artist.strip()
        })
    else:
        # 若沒有 -，就保留原本的
        result.append(item)

print(result)