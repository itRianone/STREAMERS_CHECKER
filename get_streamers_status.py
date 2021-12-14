
#from script import db, DATABASE
import re
import requests
import json
import time
from settings import CLIENT_ID, APP_ACCESS_TOKEN, API_KEY
from mydb import db, cursor
import threading
import urllib.request
from transliterate import translit

trigger = ')'

#СЛАВА ГОСПОДУ 1 ИЗ 2 УДАЛОСЬ ПОЛУЧИТЬ ЕФЮЧЮ
def get_twitch_data(streamers: str):

  #print(streamers)
  req = []
  streamer_names = []
  for streamer in streamers:
    if 'youtube' in streamer[1]:
      continue
    else:
      #print(streamer)
      streamer_name = streamer[1].replace('https://www.twitch.tv/', '')
      streamer_names.append(streamer_name)
      req.append(f'&user_login={streamer_name}')
  
  #print(streamer_names)
  if len(req) == 0:
    return
  if len(req) == 1:
    #print(req)
    req = ''.join(req[0])
  else:
    req[0] = req[0].replace('&', '')
    req = ''.join(req)

  #print('streamers: ',streamer_names)
  url = f"https://api.twitch.tv/helix/streams?" + req # user_login={streamer_name}

  head = {
    'Client-ID': CLIENT_ID,
    'Authorization': 'Bearer ' + APP_ACCESS_TOKEN
  }

  request = requests.get(url=url, headers=head)
  #print(request.text)
  res = json.loads(request.text)

  # print(res['data'])
  for name in streamer_names:
    if name in f'{res["data"]}':
      continue
    else:
      #print(1, name)
      cursor.execute("UPDATE streamers SET streamer_status=(?), stream_img=(?), stream_title=(?), streamer_username=(?) WHERE streamer_name=(?)",
                     (None, None, None, name, 'https://www.twitch.tv/' + name))
      db.commit()

  for res in res['data']:
    #print(res)
    title = res['title']
    img = res['thumbnail_url'].replace(r'{width}x{height}', '1920x1080')
    username = res['user_name']
    cursor.execute("UPDATE streamers SET streamer_status=(?), stream_img=(?), stream_title=(?), streamer_username=(?) WHERE streamer_name=(?)",
                   ('Online', img, title, username, 'https://www.twitch.tv/' + username.lower()))
    db.commit()
    #print(img, title, username)

# def get_youtuber(streamer):
#     r = requests.get(streamer)  
#     username_pattern = r'{"title":"([^"]*)"'
#     username_pattern = username_pattern
#     username = re.findall(username_pattern, r.text)
#     username = username[-1].replace('{', '')
#     username = username.replace('}', '')

#     cursor.execute("UPDATE streamers SET streamer_status=(?), stream_img=(?), stream_title=(?), streamer_username=(?) WHERE streamer_name=(?)",
#                    (None, None, None, username.replace(' ', ''), streamer))
#     db.commit()

def get_yt_username(streamer: str):
  r = requests.get(streamer)  
  username_pattern = r'{"title":"([^"]*)"'
  username_pattern = username_pattern
  username = re.findall(username_pattern, r.text)
  username = username[-1].replace('{', '')
  username = username.replace('}', '')

  return username

def get_youtube_data(streamer: str):

  r = requests.get(streamer)
  reg = r'"externalId":"([^"]*)"'
  channelId = re.findall(reg, r.text)
  channelId = ''.join(channelId)
  #print(channelId)

  # url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channelId}&eventType=live&type=video&key={API_KEY}'
  url = f'https://www.youtube.com/embed/live_stream?channel={channelId}'
  r = requests.get(url)

  cyrillic_symbols = r'[а-яА-ЯёЁ]'

  #print(channelId)
  if 'videoTitle' in r.text:
    try:
      # stream_url = r'videoShareUrl\\":\\"[\S]+\\"'
      # stream_url = re.findall(stream_url, r.text)
      stream_pattern = r'videoTitle\\":\\"([^"]*)\\"}},'
      stream_title = re.findall(stream_pattern, r.text)
      #print(r.text)
      stream_title = stream_title[0].replace('{', '')
      stream_title = stream_title.replace('}', '')
      channel_pattern = r'"text\\":\\"([^"]*)\\"'
      channel_name = re.findall(channel_pattern, r.text)
      #print(channel_name[3])
      channel_name = channel_name[3]
      img_pattern = r'"url\\":\\"https://i.ytimg.com/vi([^"]*)\\"'
      stream_img = re.findall(img_pattern, r.text)
      is_cyrillic = re.findall(cyrillic_symbols, channel_name)
      #print(f'username: {channel_name}, {is_cyrillic}')

      if len(is_cyrillic) > 0:
        channel_name = translit(channel_name, language_code='ru', reversed=True)
        #print(f'username in lat: {channel_name}')  

      cursor.execute("UPDATE streamers SET streamer_status=(?), stream_img=(?), stream_title=(?), streamer_username=(?) WHERE streamer_name=(?)",
                    ('Online', 'https://i.ytimg.com/vi' + stream_img[-1], stream_title, channel_name.replace(' ',''), streamer))
      db.commit()
      #print(streamer, 1)
    except IndexError as e:
      username = get_yt_username(streamer)

      is_cyrillic = re.findall(cyrillic_symbols, username)
      #print(f'username: {username}, {is_cyrillic}')

      if len(is_cyrillic) > 0:
        username = translit(username, language_code='ru', reversed=True)
        #print(f'username in lat: {username}')        
      
      cursor.execute("UPDATE streamers SET streamer_status=(?), stream_img=(?), stream_title=(?), streamer_username=(?) WHERE streamer_name=(?)",
                    (None, None, None, username.replace(' ', ''), streamer))
      db.commit()
  else:
    username = get_yt_username(streamer)
    
    is_cyrillic = re.findall(cyrillic_symbols, username)
    #print(f'username: {username}, {is_cyrillic}')

    if len(is_cyrillic) > 0:
      username = translit(username, language_code='ru', reversed=True)
      #print(f'username in lat: {username}')  

    cursor.execute("UPDATE streamers SET streamer_status=(?), stream_img=(?), stream_title=(?), streamer_username=(?) WHERE streamer_name=(?)",
                   (None, None, None, username.replace(' ', ''), streamer))
    db.commit()
    
    # # headers = {
    # #     'Authorization': 'Bearer' + APP_ACCESS_TOKEN,
    # #     'Accept': 'application/json'
    # # }

    # res = requests.get(url=url)
    # res = res.json()
  #   channelId = streamer.replace('https://www.youtube.com/channel/', '')
  #   url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channelId}&eventType=live&type=video&key={API_KEY}'
  #   r = requests.get(url)


def GET_API_DATA():
  import datetime
  while True:
    print('Parser is working... ', datetime.datetime.now())
    # streams_status = {}
    cursor.execute("SELECT * FROM streamers")
    streamers = cursor.fetchall()
    for item in streamers:
      try:
        # print('saving img .. in ', item[3],
              # "static/images/" + str(item[0]) + '.jpeg')
        urllib.request.urlretrieve(
            item[3], "static/images/" + str(item[0]) + '.jpeg')
      except:
        pass
    get_twitch_data(streamers)
    for item in streamers:
      #print(item)
      streamer = item[1]
      if 'youtube' in streamer:
        get_youtube_data(streamer) 

    
    time.sleep(17)


my_demon = threading.Thread(target=GET_API_DATA, daemon=True)
# parse_streamers()
# get_twitch_data('https://www.twitch.tv/razedoto')
# get_youtube_data('https://www.youtube.com/c/Slidan')
# get_youtube_data('https://www.youtube.com/c/JomaOppa')
# print(streams)
