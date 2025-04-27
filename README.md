# 🎶 Weather Mood App 🌦️

A fun, dynamic web app that matches your local weather to a mood, suggests a live Spotify playlist, and shows a beautiful Unsplash background image based on the vibe!

Built with Flask, Tailwind CSS, OpenWeatherMap API, Spotify API, and Unsplash API.

---

## 🌟 Features

- 🌦️ Live weather detection by city
- 🎶 Dynamic mood-matching Spotify playlists
- 🖼️ Mood-based Unsplash background images
- 🔀 Randomized moods based on weather type
- 📱 Mobile-responsive design with TailwindCSS
- 💬 Friendly error handling

---

## 🚀 How It Works

1. Enter your city.
2. App fetches live weather data using OpenWeatherMap.
3. Matches the weather to a randomized mood (e.g., "rainy" → "chill" or "lofi").
4. Searches Spotify for a playlist matching the mood.
5. Searches Unsplash for a background image matching the mood.
6. Displays the weather info, embedded Spotify playlist, and beautiful mood image!

---

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS
- **APIs**:
  - OpenWeatherMap API (Weather data)
  - Spotify API via Spotipy (Playlist search)
  - Unsplash API (Mood background images)
- **Environment Management**: `python-dotenv`
- **Deployment Ready**: Easily host on Render, Railway, or any Flask-compatible service

