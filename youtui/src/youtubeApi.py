# from time import sleep
import errno
import ytmusicapi
import locale
import spotipy.util as util
from youtui.src.config import get_config
from reverseengineering import is_paused, is_playing # dummy data
from piped_api import PipedClient
import os
from mpv import MPV

class YoutubeAPI:
    client = None

    def __init__(self):

        # local variables used to update player state
        self.repeat_state = False
        self.shuffle_state =False
        self.current_track = {
            'item': {}
        }
        self.loaded_tracks = [] # tracks from playlist
        self.current_playlist = None
        self.loaded_tracks_ids = []
        self.search_results = None

        self.auth()
        self.client = ytmusicapi.YTMusic()
        self.piped = PipedClient()
        locale.setlocale(locale.LC_NUMERIC, "C")
        self.player = MPV()
        self.player._set_property('vid', False)


        # initialize m3u file used to store playlist cache
        __home_dir = os.path.expanduser("~")
        self.__filename = os.path.join(__home_dir, ".config", "youtui", ".temp", "cache.m3u")
        if not os.path.exists(os.path.dirname(self.__filename)):
            try:
                os.makedirs(os.path.dirname(self.__filename))
            except OSError as exc:  # prevent race condition
                if exc.errno != errno.EEXIST:
                    raise

    def auth(self):

        ...
        # config = get_config()
        # user_config_dir = os.path.expanduser("~")
        # cache_location = os.path.join(
        #     user_config_dir, '.config/spotui/SpoTUI_token.cache')
        # self.user_name = config.get("spotify_api", "user_name")
        # client_id = config.get("spotify_api", "client_id")
        # client_secret = config.get("spotify_api", "client_secret")
        # redirect_uri = config.get("spotify_api", "redirect_uri")
        # scopes = "user-read-playback-state streaming playlist-read-collaborative user-modify-playback-state playlist-modify-public user-library-modify user-top-read user-read-currently-playing playlist-read-private playlist-modify-private user-read-recently-played user-library-read"
        # self.token = util.prompt_for_user_token(
        #     self.user_name,
        #     scopes,
        #     client_id=client_id,
        #     client_secret=client_secret,
        #     redirect_uri=redirect_uri,
        #     cache_path=cache_location
        # )

        # if self.token:
        #     self.client = spotipy.Spotify(auth=self.token)
        # else:
        #     logging.warning("Can't get token for", self.user_name)

    def get_playing(self):
        try:
            status = is_playing
            
            status_dynamic = {
                'is_playing': not self.player._get_property('pause'), # opposite
                'progress_ms': int(self.player._get_property('time-pos')) * 1000,
                'shuffle_state': self.shuffle_state,
                'repeat_state': self.repeat_state,

                # repeat_state: False, # to be implemented
                'item': {
                    'id': self.current_track.get('id'),
                    'name': self.current_track.get('name'),
                    'artist': self.current_track.get('artist'),
                    'duration_ms': int(self.player._get_property('duration')) * 1000
                },

            }
            return status_dynamic
        except Exception as e:
            pass

    def get_audio_stream(self, videoid):
        video = self.piped.get_video(video_id=videoid)
        return video.get_streams('audio')[-1].url

    def search(self, query):
        try:

            search_results = self.client.search(query, filter='songs', limit= 50)

                #a list comprehension to extract the properties "title", artists,
                # "videoId" from only the dictionaries that contain "category": 'song' from search_results
            items = [{'name': item['title'], 'artist': item['artists'][0]['name'], 'id': item['videoId']} 
                        for item in search_results ]

            self.search_results=items
            return items
        except Exception as e:
            pass

    def __search_all(self, className, query):
        plural = className + 's'
        self.client.search()
        tracks = self.__extract_results(self.client.search(
            query, 50, 0, className), plural)
        return tracks
    
    def __extract_results(self, results, key):
        tracks = results[key]
        items = tracks['items']
        return items

    def start_playback(self, track):
        try:
            # this is called only when you manually play a track
            self.shuffle_state=False
            self.repeat_state=False

            cache=self.__filename

            self.loaded_tracks_ids = [loaded_track['id'] for loaded_track in self.loaded_tracks]
            if self.current_playlist and track['id'] in self.loaded_tracks_ids:
                # initialize track template
                self.current_track=track

                with open(cache, 'w') as f:

                    for id in self.loaded_tracks_ids:
                        if id is not None:
                            f.write('https://music.youtube.com/watch?v='+id+'\n')

                self.player.play(cache)
                self.player.wait_until_playing()
                
                self.update_current_track(track['id'])
                return
            
            self.player.play('https://music.youtube.com/watch?v='+track['id'])
            self.player.wait_until_playing()
            self.update_current_track()
        except Exception as e:
            pass

    # update current track state in self.get_playing()['item']
    def update_current_track(self, id=None):
        if id:
            current_track_id = id
        
        if not id: # its a nornam track, not a playlist
            current_track_id = self.player._get_property('filename').strip('watch?v=')
            self.current_track.setdefault('item', {})['id'] = current_track_id
            for track in self.search_results:
                if track['id'] == current_track_id:
                    self.current_track['name'] = track['name']
                    self.current_track['artist'] = track['artist']
                    # os.system('konsole')
                    return

        # it's a track in a playlist
        self.current_track.setdefault('item', {})['id'] = current_track_id
        for track in self.loaded_tracks:
            if track['id'] == current_track_id:
                self.current_track['name'] = track['name']
                self.current_track['artist'] = track['artist']
                # os.system('konsole')
                return

    def toggle_playback(self):
        try:
            self.player.cycle('pause')
        except Exception as e:
            pass

    def pause_playback(self, device_id):
        try:
            self.client.pause_playback(device_id)
        except Exception as e:
            pass

    def previous_track(self):
        try:

            self.player.playlist_prev()
            self.update_current_track()
            
            return
        except Exception as e:
            pass

    def next_track(self):
        try:
            self.player.playlist_next()
            self.update_current_track()
            
            return
        except Exception as e:
            pass

    def seek_track(self, position):
        try:
            self.player.seek(position)
        except Exception as e:
            pass
    
    def change_volume(self, audio_amount):
        try:
            volume = self.player._get_property('volume')
            if  0 < volume+audio_amount < 130:
                self.player._set_property('volume', volume+audio_amount)
        except Exception as e:
            pass
    def get_playlists(self):
        try:
            # this grabs playlists spotify is trying to get the user to listen to
            # playlists = self.client.user_playlists('spotify')

            playlists = []
            get_playlists = None
            for playlist in get_config()['playlists']:
                # time.sleep(1)
                # print(playlist)``
                get_playlists = self.client.get_playlist(f'{playlist}', limit=0,related=False,suggestions_limit=0)
                # print(get_playlists)
                playlists.append({key: get_playlists.get(key) for key in ['title', 'id']}) #seperate stuff


            out = list(map(self.__map_playlists, playlists))
            return out
        except Exception as e:
            return []
            pass

    def get_playlist_tracks(self, playlist_id):
        # try:
            self.current_playlist=playlist_id
            playlist = self.client.get_playlist(playlist_id,limit=None,related=False,suggestions_limit=0)
            tracks = [{key: track.get(key) for key in ['title', 'videoId', 'artists']} for track in playlist['tracks']]
            
            self.loaded_tracks = list(map(self.__map_tracks, tracks)) 
            return self.loaded_tracks
        
        # except Exception as e:
        #     pass

    def get_devices(self):
        try:
            devices = self.client.devices()
            return list(map(self.__map_devices, devices["devices"]))
        except Exception as e:
            pass

    def toggle_shuffle(self):
        # try:
            if not self.shuffle_state:
                self.player.playlist_shuffle()
                self.shuffle_state = True
            else:
                self.player.playlist_unshuffle()
                self.shuffle_state = False
        # except Exception as e:
            # pass

    def repeat(self):
        try:
            if self.repeat_state == False:
                # update local var
                self.repeat_state = True
                # enable looping in mpv
                self.player._set_property('loop-file', "inf")
            else:
                self.repeat_state = False
                self.player._set_property('loop-file', False)
        except Exception as e:
            pass

    def __map_tracks(self, track):

        out = {"name": track['title'],
        "artist": track["artists"][0]["name"],
        "id": track["videoId"]}
        return out

    def __map_playlists(self, playlist):
        return {
            "text": playlist["title"],
            "id": playlist["id"],
            # "uri": playlist[None]
        }

    def __map_devices(self, device):
        return {"text": device["name"], "id": device["id"]}

