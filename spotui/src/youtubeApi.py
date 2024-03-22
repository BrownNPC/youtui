# from time import sleep
import ytmusicapi
import locale

import spotipy.util as util
from spotui.src.config import get_config
from spotui.src.Logging import logging
from client import showStatusMsg
from reverseengineering import is_paused, is_playing # dummy data
from piped_api import PipedClient
import os
from mpv import MPV

class YoutubeAPI:
    client = None

    def __init__(self):

        # local variables used to update player state
        self.repeat_state = False
        self.current_track = '' # track id (video id)

        self.auth()
        self.client = ytmusicapi.YTMusic()
        self.piped = PipedClient()
        locale.setlocale(locale.LC_NUMERIC, "C")
        self.player = MPV()
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
                'shuffle_state': False, # to be implemented
                'repeat_state': self.repeat_state,

                # repeat_state: False, # to be implemented
                'item': {
                    'id': self.current_track,
                    'name': self.current_track['name'],
                    'artist': self.current_track['artist'],
                    'duration_ms': int(self.player._get_property('duration')) * 1000
                },

                
                
        

            }
            return status_dynamic
        except Exception as e:
            pass

    def get_audio_stream(self, videoid):
        video = self.piped.get_video(video_id=videoid)
        return video.get_streams('audio')[3].url

    def search(self, query):
        try:
            classes = ['track', 'show', 'playlist']
            items = [self.__search_all(c, query) for c in classes]
            flat_items = [item for sublist in items for item in sublist]
            return list(map(self.__map_tracks, flat_items))
        except Exception as e:
            pass

    def start_playback(self, track):
        showStatusMsg(f'THIS IS TRACK --- {track}')
        self.current_track = track
        # dc = {}
        self.current_track.setdefault('item', {})['id'] = track['id']
        stream_url = self.get_audio_stream(track['id'])
        self.player.play(stream_url)
        return
            # self.player.wait_until_playing()
        # except Exception as e:
            # pass

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

    def previous_track(self, device_id):
        try:
            self.client.previous_track(device_id)
        except Exception as e:
            pass

    def next_track(self, device_id):
        try:
            self.client.next_track(device_id)
        except Exception as e:
            pass

    def seek_track(self, position):
        # try:
            self.player.seek(position)
        # except Exception as e:
            # pass

    def get_top_tracks(self):
        try:
            tracks = self.client.current_user_top_tracks()
            items = tracks["items"]
            while tracks["next"]:
                tracks = self.client.next(tracks)
                items += tracks["items"]
            return list(map(self.__map_tracks, items))
        except Exception as e:
            pass

    def get_recently_played(self):
        try:
           # set used to identify unique tracks, prevent duplication of results
            track_uris = set()
            while tracks["next"]:
                tracks = self.client.next(tracks)
                items += tracks["items"]
                # remove all non-unique track-items from recently played list
                items = [item for item in items if item["track"]["uri"] not in track_uris \
                and (track_uris.add(item["track"]["uri"]) or True)]
            return list(map(self.__map_tracks, items))
        except Exception as e:
            pass

    def show_episodes(self, id):
        try:
            tracks = self.client.show_episodes(id)
            items = tracks["items"]
            return list(map(self.__map_tracks, items))
        except Exception as e:
            pass

    def get_liked_tracks(self):
        try:
            tracks = self.client.current_user_saved_tracks()
            items = tracks["items"]
            while tracks["next"]:
                tracks = self.client.next(tracks)
                items += tracks["items"]
            return list(map(self.__map_tracks, items))
        except Exception as e:
            pass

    def get_playlists(self):
        try:
            # this grabs playlists spotify is trying to get the user to listen to
            # playlists = self.client.user_playlists('spotify')

            playlists = []
            for playlist in get_config()['playlists']:
                # time.sleep(1)
                # print(playlist)

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
            playlist = self.client.get_playlist(playlist_id,limit=None,related=False,suggestions_limit=0)
            # showStatusMsg(f"TRACKS IN PLAYLIST  ---\n\n\--- {playlist['tracks']}")
            tracks = [{key: track.get(key) for key in ['title', 'videoId', 'artists']} for track in playlist['tracks']]
            
            return list(map(self.__map_tracks, tracks)) 
        
        # except Exception as e:
        #     pass

    def get_devices(self):
        try:
            devices = self.client.devices()
            return list(map(self.__map_devices, devices["devices"]))
        except Exception as e:
            pass

    def shuffle(self, state):
        try:
            devices = self.client.shuffle(state)
        except Exception as e:
            pass

    def repeat(self, state):
        try:
            if state:
                # update local var
                self.repeat_state = True
                # enable looping in mpv
                self.player._set_property('loop-file', "inf")
            else:
                self.repeat_state = False
                self.player._set_property('loop-file', False)
        except Exception as e:
            pass

    def __search_all(self, className, query):
        plural = className + 's'
        tracks = self.__extract_results(self.client.search(
            query, 50, 0, className), plural)
        return tracks

    def __extract_results(self, results, key):
        tracks = results[key]
        items = tracks['items']
        return items

    def __map_tracks(self, track):

        # showStatusMsg(f'TRACK: ----  \n\n\  {track}')
        out = {"name": track['title'],
        "artist": track["artists"][0]["name"],
        "id": track["videoId"]}
        self.current_track = out
        return out

    def __map_playlists(self, playlist):
        return {
            "text": playlist["title"],
            "id": playlist["id"],
            # "uri": playlist[None]
        }

    def __map_devices(self, device):
        return {"text": device["name"], "id": device["id"]}

