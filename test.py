
# USING MPV TO PLAY YOUTUBE AUDIOS WITH PIPED API
from piped_api import PipedClient
import mpv
import yt_dlp
from pprint import pprint
import mpv
player = mpv.MPV()

# player.play('https://youtu.be/DOmdB7D-pUU')


import os

CLIENT = PipedClient()

# def get_audio_stream(videoid):
#     # video = CLIENT.get_video(video_id=videoid)
#     # return video.get_streams('audio')[3].url

#     url = f'https://www.youtube.com/watch?v={videoid}'
#     ydl_opts = {}
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     # get all information about the youtube video
#       info = ydl.extract_info(url, download=False)

#       urls = []
#       for i in info['formats']:
#           for j in i['url']:
#               urls.append(j)
#     return urls[-1]

# # Print out the first audio stream URL for a video:
# # print(audio_stream.url)
player._set_property('vid', False)
# playlist="""https://www.youtube.com/watch?v=f0HOQGTfkcs
# https://www.youtube.com/watch?v=pb39n_bEHyA
# https://www.youtube.com/watch?v=gYPK088cPJI
# """
player.loadfile()
player.wait_until_playing()
player.playlist_play_index(-1)
# while len(player.playlist_filenames) < 2:
# player.playlist_play_index(-1)

# player.play()
# player.wait_for_playback()
# for song in playlist:
#     player.playlist_append(song)


# player.loadfile('https://www.youtube.com/watch?v=gYPK088cPJI', 'append-play')
print('done')

while True:
    command = input()
    if command == ' ':
        print(player.playlist_filenames)
    elif command == 'n':
        player.playlist_next()
    elif command == 'p':
        pprint(player._get_property('filename').strip('watch?v='))
        pprint(player._get_property('shuffle'))


# # player.audio_add(audio_stream.url)
# # os.system(f'mpv "{audio_stream.url}" --no-video')


#REVERSE ENGINEERING CURRENTLY PLAYING TRACKS
# import os, spotipy
# from spotipy import prompt_for_user_token
# from dotenv import load_dotenv
# load_dotenv()

# user_config_dir = os.path.expanduser("~")
# token =prompt_for_user_token(
#             username='Dead_Dawg',
#             scope = "user-read-playback-state streaming playlist-read-collaborative user-modify-playback-state playlist-modify-public user-library-modify user-top-read user-read-currently-playing playlist-read-private playlist-modify-private user-read-recently-played user-library-read",
#             client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
#             client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
#             redirect_uri=os.environ.get('SPOTIPY_REDIRECT_URI'),
#             # cache_path=cache_location
#         )
# cache_location = os.path.join(
#     user_config_dir, '.config/spotui/SpoTUI_token.cache')
# client = spotipy.Spotify(auth=token)
# print(client.current_playback())


#TRYING OUT YTMUSICAPI

# from ytmusicapi import YTMusic
# from spotui.src.config import get_config
# import time
# ytmusic = YTMusic()

# playlists = []

# for playlist in get_config()['playlists']:
#     # time.sleep(1)
#     # print(playlist)

#     get_playlists = ytmusic.get_playlist(f'{playlist}')
#     # print(get_playlists)
#     playlists.append({key: get_playlists.get(key) for key in ['title', 'id']}) #seperate stuff
#     # {key: song['videoDetails'].get(key) for key in ['title', 'author', 'lengthSeconds', 'videoId']}


# values = {key: song['videoDetails'].get(key) for key in ['title', 'author', 'lengthSeconds', 'videoId']} #seperate stuff
# print(playlists)


# TRYING TO MAKE MPV AUDIO PLAYER



# TESTING LIST COMPREHENSIONs
# from pprint import pprint
# from ytmusicapi import YTMusic
# from spotui.src.config import get_config
# import time
# ytmusic = YTMusic()

# search_results =  ytmusic.search('among us drip', filter='songs', limit=50)
# res =[{'title': item['title'], 'artists': item['artists'][0]['name'], 'videoId': item['videoId']} 
#       for item in search_results]


# pprint(res)