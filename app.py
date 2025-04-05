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


def Fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6a4b81aa5b5fb5929a57be811ac2d284'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+ data["poster_path"]

def recommend(movie):
    movie_index=movies[movies['title'] == movie].index[0]
    distances= similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)) , reverse=True , key=lambda x:x[1])[1:6]
    recommended_movies=[] 
    poster=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching the movies poster using API
        poster.append(Fetch_poster(movie_id))
        
    return recommended_movies , poster   

movies_dict= pickle.load(open('movie_dic.pkl' , 'rb'))

movies=pd.DataFrame(movies_dict)

similarity= pickle.load(open('similarity.pkl' , 'rb'))

st.title('Movies Recommender System')
movie_selected=st.selectbox(
    'Select the movie to get more relevant movies of your interset ',
    movies['title'].values
)

if st.button('Recommend'):
    names,poster=recommend(movie_selected)
    

    col1, col2, col3, col4,col5 = st.columns(5)

    with col1:
       st.header(names[0])
       st.image(poster[0])
    with col2:
       st.header(names[1])
       st.image(poster[1])
    with col3:
       st.header(names[2])
       st.image(poster[2])
    with col4:
       st.header(names[3])
       st.image(poster[3])
    with col5:
       st.header(names[4])
       st.image(poster[4])


