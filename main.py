import io
import json
import logging
import os
from typing import Dict
import openai
import requests
from models.openai_client import OpenAIClient
from models.spotify_client import SpotifyClient


PODCASTS = {
    "Lex Fridman": "2MAi0BvDc6GTFvKFPXnkCL"
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def transcribe(audio_file_location: str, podcast_name: str, podcast_id: str):
    """Transcribe the audio file content using OpenAI's Audio API."""
    logger.info("Transcribing podcast: %s", podcast_name)
    
    with open(audio_file_location, "rb") as f:
        audio_file_content = f.read()
    
    transcript = openai.Audio.transcribe("whisper-1", io.BytesIO(audio_file_content))
    
    transcript_location = os.path.join("transcripts", podcast_name, f"{podcast_id}.txt")
    os.makedirs(os.path.dirname(transcript_location), exist_ok=True)
        
    with open(transcript_location, "w") as f:
        f.write(transcript)


def process(podcast_name: str, sp: SpotifyClient):
    """Download the latest episode of the podcast and save it to a file."""
    logger.info("Processing podcast: %s", podcast_name)
    
    podcast_id = PODCASTS[podcast_name]
    
    # Get the latest episode of the podcast
    results = sp.show_episodes(podcast_id, limit=1, offset=0)
    latest_episode = results["items"][0]
        
    # Get the audio file for the latest episode
    audio_file_url = latest_episode["audio_preview_url"]
    audio_file_content = requests.get(audio_file_url).content
        
    audio_file_name = f"{podcast_id}.mp3"
    podcast_location = os.path.join("podcasts", podcast_name, audio_file_name)
    
    os.makedirs(os.path.dirname(podcast_location), exist_ok=True)
    
    # Download the audio file
    with open(podcast_location, "wb") as f:
        f.write(audio_file_content)
        
    transcribe(podcast_location, podcast_name, podcast_id)


def main():
    """Download the latest episodes of the podcasts."""
    with open('app.config.json') as f:
        config = json.load(f)
        sp = SpotifyClient(config).client
        oai_client = OpenAIClient(config)
        
    for podcast_name in PODCASTS:
        process(podcast_name, sp)
        
        
if __name__ == "__main__":
    main()