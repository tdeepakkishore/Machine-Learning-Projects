import streamlit as st
import pandas as pd
import pickle
import requests

st.set_page_config(
    page_title="Movie Recommendation App",
    page_icon='🧊',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title('Movie Recommender System')

# mov_load = pickle.load(open('movies.pkl', 'rb'))
dict_load = pickle.load(open('movies_dict.pkl', 'rb'))
sim_load = pickle.load(open('similarity.pkl', 'rb'))

# Converting to Dataframe
movies_df = pd.DataFrame(dict_load)


# Fetching Images
def fetch_poster(movie):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=324243d9892aeb5663c5c'
                            '6fc38760262&language=en-US'.format(movie))
    data = response.json()
    return 'https://image.tmdb.org/t/p/original'+data['poster_path']


def recommend(movie):
    ind = movies_df[movies_df['title'] == movie].index[0]
    corr = sim_load[ind]
    mov = sorted(list(enumerate(corr)), reverse=True, key=lambda x: x[1])[1:6]

    vals = [i[0] for i in mov]

    movie_names = []
    movie_poster = []

    for index in vals:
        m, n = movies_df.iloc[index, :2].values
        movie_names.append(n)
        movie_poster.append(fetch_poster(m))

    return movie_names, movie_poster


# List of Movies
selected_movie = st.selectbox('Select Movies',  movies_df['title'])

# Button of Recommendation
if st.button('Recommend'):
    movies_lst, poster_lst = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    details = list(zip(movies_lst, poster_lst))

    with col1:
        st.text(details[0][0])
        st.image(details[0][1])
    with col2:
        st.text(details[1][0])
        st.image(details[1][1])
    with col3:
        st.text(details[2][0])
        st.image(details[2][1])
    with col4:
        st.text(details[3][0])
        st.image(details[3][1])
    with col5:
        st.text(details[4][0])
        st.image(details[4][1])