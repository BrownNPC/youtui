
#USING MPV TO PLAY YOUTUBE AUDIOS WITH PIPED API
# from piped_api import PipedClient
# import mpv


# import mpv
# player = mpv.MPV()

# # player.play('https://youtu.be/DOmdB7D-pUU')


# import os

# CLIENT = PipedClient()


# # Print out the first audio stream URL for a video:
# video = CLIENT.get_video('MRbRe5f9G3Q')
# audio_stream = video.get_streams('audio')[3]
# # print(audio_stream.url)
# player.play(audio_stream.url)
# player.wait_for_playback


# while True:
#     1+1
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

from ytmusicapi import YTMusic

ytmusic = YTMusic()

song = ytmusic.get_song('zWFQOIDBKBs')
values = {key: song['videoDetails'].get(key) for key in ['title', 'author', 'lengthSeconds', 'videoId']} #seperate stuff
print(values)