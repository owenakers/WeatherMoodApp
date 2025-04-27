from flask import Flask, render_template, request
import requests
import spotipy
import random
import os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# API keys loaded from .env
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Set up Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Function to match weather condition to a mood keyword
def get_mood_keyword(condition):
    condition = condition.lower()
    if "rain" in condition or "drizzle" in condition or "thunderstorm" in condition:
        return random.choice(["chill", "lofi", "sad", "calm", "cozy"])
    elif "clear" in condition:
        return random.choice(["happy", "energetic", "upbeat", "sunshine"])
    elif "cloud" in condition:
        return random.choice(["dreamy", "indie", "calm", "chill"])
    elif "snow" in condition:
        return random.choice(["cozy", "winter", "holiday", "calm"])
    else:
        return random.choice(["epic", "cinematic", "adventure"])



@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result', methods=['POST'])
def result():
    weather_data = None
    mood = None
    playlist_id = None
    mood_image_url = None
    error = None

    city = request.form['city']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=imperial"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        condition = data['weather'][0]['main']
        mood = get_mood_keyword(condition)

        # --- Spotify Playlist Search ---
        results = sp.search(q=mood, type='playlist', limit=10)
        playlists = results['playlists']['items']

        if playlists:
            # Filter playlists that definitely have external links
            valid_playlists = [p for p in playlists if p and 'external_urls' in p and 'spotify' in p['external_urls']]

            if valid_playlists:
                random_playlist = random.choice(valid_playlists)
                playlist_url = random_playlist['external_urls']['spotify']
                playlist_id = playlist_url.split("/")[-1]
            else:
                # Fallback playlist ID (Lofi Beats playlist)
                playlist_id = "37i9dQZF1DXdPec7aLTmlC"
        else:
            # Fallback playlist ID (Lofi Beats playlist)
            playlist_id = "37i9dQZF1DXdPec7aLTmlC"

        # --- Unsplash Mood Image Search ---
        unsplash_url = "https://api.unsplash.com/photos/random"
        params = {
            'query': mood,
            'client_id': UNSPLASH_ACCESS_KEY,
            'orientation': 'landscape'
        }
        image_response = requests.get(unsplash_url, params=params)

        if image_response.status_code == 200:
            image_data = image_response.json()
            mood_image_url = image_data['urls']['regular']
        else:
            mood_image_url = None

        # --- Weather Data ---
        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'].capitalize()
        }
    else:
        error = f"Could not find weather for '{city}'. Please try again."

    return render_template(
        'result.html',
        weather_data=weather_data,
        mood=mood,
        playlist_id=playlist_id,
        mood_image_url=mood_image_url,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
