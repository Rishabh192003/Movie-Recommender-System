import streamlit as st 
import pickle
import pandas as pd
import requests
import os
import gdown

# Only download if not already downloaded
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=10FObpameldApISrc0qRmnyLJX2Bwi58O"
    gdown.download(url, "similarity.pkl", quiet=False)

# Function to fetch poster URL and TMDB link
def Fetch_poster_and_link(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=6a4b81aa5b5fb5929a57be811ac2d284'
    )
    data = response.json()
    poster_url = "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    movie_url = f"https://www.themoviedb.org/movie/{movie_id}"
    return poster_url, movie_url

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = [] 
    posters = []
    links = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        
        # Get poster and link
        poster_url, movie_url = Fetch_poster_and_link(movie_id)
        posters.append(poster_url)
        links.append(movie_url)
        
    return recommended_movies, posters, links   

# Load data
movies_dict = pickle.load(open('movie_dic.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System')

movie_selected = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters, links = recommend(movie_selected)
    
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.header(names[i])
            st.image(posters[i])
            # Create clickable link
            st.markdown(f"[🔗 Watch here]({links[i]})", unsafe_allow_html=True)
