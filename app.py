import pickle
import streamlit as st
import requests
from requests.exceptions import ConnectTimeout

def fetch_poster(id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=db46e50e7da3221d8cd8c032e75b042b'.format(id)
    try:
        data = requests.get(url, timeout=10)  # Set timeout to 10 seconds
        data.raise_for_status()  # Raise an exception for 4xx or 5xx errors
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = 'https://image.tmdb.org/t/p/w185/' + poster_path
            return full_path
        else:
            return None  # No poster path found
    except ConnectTimeout:
        st.error("Connection to the movie database timed out. Please try again later.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster for movie with ID {id}: {e}")
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        id = movies.iloc[i[0]].id
        poster_url = fetch_poster(id)
        if poster_url:
            recommended_movies_poster.append(poster_url)
            recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

st.header("Movie Recommendation System using Machine Learning")
movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))
movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendation',
    movie_list
)
if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    for name, poster in zip(recommended_movies_name, recommended_movies_poster):
        with col1:
            st.text(name)
            st.image(poster)