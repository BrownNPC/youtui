
# USING MPV TO PLAY YOUTUBE AUDIOS WITH PIPED API
# from piped_api import PipedClient
# import mpv


# import mpv
# player = mpv.MPV()

# # player.play('https://youtu.be/DOmdB7D-pUU')


# import os

# CLIENT = PipedClient()

# def get_audio_stream(videoid):
#     video = CLIENT.get_video(video_id=videoid)
#     return video.get_streams('audio')[3].url

# # Print out the first audio stream URL for a video:
# # print(audio_stream.url)
# player.play(get_audio_stream('MRbRe5f9G3Q'))
# player.wait_for_playback
# # player.property_add("pause", 1)
# print('done')

# while True:
#     command = input()
#     if command == 'q':
#         player.play(get_audio_stream('dQw4w9WgXcQ'))
#         player._set_property('loop-file', 'inf')
#     elif command == ' ':
#         # player.cycle('pause')
#         print(player._set_property('pause', True))
#     elif command == 'w':
#         progress_ms = int(player._get_property('time-pos')) * 1000
#         length = int(player._get_property('duration')) * 1000
#         print(length, progress_ms)
#         player._set_property('pause', False)
        
#         player.seek('10')
#         player._set_property('loop-file', False)





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
from pprint import pprint
from ytmusicapi import YTMusic
from spotui.src.config import get_config
import time
ytmusic = YTMusic()

search_results =  ytmusic.search('among us drip', filter='songs', limit=50)
res =[{'title': item['title'], 'artists': item['artists'][0]['name'], 'videoId': item['videoId']} 
      for item in search_results]


pprint(res)