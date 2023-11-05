import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient():
    def __init__(self, config):
        self.client = self.authenticate(config)

    def authenticate(self, config):
        client_id = config["spotify"]["client_id"]
        client_secret = config["spotify"]["client_secret"]
        auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:8080/callback/", scope="user-library-read")
        return spotipy.Spotify(auth_manager=auth_manager)
