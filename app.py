import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle

# Loading the dataset
songs = pickle.load(open("songs.pkl", "rb"))

similarity = pickle.load(open('similar.pkl', 'rb'))

# Spotify API credentials
client_id = '3dd1535127924d8da84d89b0056086f4'
client_secret = '89099f694dec425c9908362715fb2576'

# Authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


def get_cover_url(song_title):
    results = sp.search(q=song_title, limit=1, type='track')
    if results['tracks']['items']:
        album = results['tracks']['items'][0]['album']
        return album['images'][0]['url']
    else:
        return None


def recommend(song):
    index = np.where(songs["song"] == song)[0][0]
    similar_songs = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_songs = []
    for i in similar_songs:
        song_title = songs["song"][i[0]]
        cover_url = get_cover_url(song_title)
        recommended_songs.append((song_title, cover_url))

    return recommended_songs


# Streamlit app
st.title("Song Recommender System")

# Dropdown list of song titles
song_list = songs['song'].tolist()
selected_song = st.selectbox("Select a song:", song_list)

if st.button("Recommend"):
    recommendations = recommend(selected_song)
    st.write("Recommended Songs:")

    cols = st.columns(len(recommendations))

    for col, (song_title, cover_url) in zip(cols, recommendations):
        with col:
            if cover_url:
                st.image(cover_url, caption=song_title)
            else:
                st.write(song_title)
