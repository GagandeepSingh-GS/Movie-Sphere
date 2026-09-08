import requests
import streamlit as st


def get_movie_details(movie_name):
    api_key = st.secrets["OMDB_API_KEY"]

    url = "https://www.omdbapi.com/"

    params = {
        "apikey": api_key,
        "t": movie_name
    }

    response = requests.get(url, params=params)

    return response.json()