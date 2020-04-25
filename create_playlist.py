import json
import os 

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from exceptions import ResponseException
from secrets import spotify_token, spotify_user_id

class CreatePlaylist:
    
    def __init__(self):
        pass
    
    def get_youtube_client(self):
        pass
    
    def get_liked_videos(self):
        # Retrieve Liked Videos and create a dictionary of important song info
        
        request = self.youtube_client.videos.list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()
        
        
    
    
    def create_playlist(self):
        
        request_body = json.dumps({
            "name": "YouTube Music",
            "description": "All liked YouTube Videos",
            "public": True
        })
        
        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        
        # playlist id
        return response_json["id"]
        
    def get_spotify_uri(self, song_name, artist):
        # Search for the song 
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        uri = songs[0]["uri"]
        
        return uri        
    
    def add_song_to_playlist(self):
        # Add all liked songs on YouTube into a new playlist on Spotify
        
        # populate dictionaries with our liked songs 
        self.get_liked_videos()
        
        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]
        
        # create a new playlist
        playlist_id = self.create_playlist()
        
        # add all songs into new playlist
        request_data = json.dumps(uris)
        
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id
        )
        
        response = requests.post(
            query, 
            data=request_data, 
            headers={
                "Content-Type":"application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        
        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        
        response_json = response.json()
        return response_json
    
    if __name__ == '__main__':
        cp = CreatePlaylist()
        cp.add_song_to_playlist()
        