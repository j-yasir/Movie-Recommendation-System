import streamlit as st
import pickle
import requests


# required data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

#function to fetch movie posters using api
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=07e5abefe42af0e786785f6ec1288649&append_to_response=videos'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']



# function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters





#page title
st.title("Movie Recommender System")

#showing list of movies
movies_list_to_show = movies['title'].values

selected_movie_name = st.selectbox(
    'Select your movie',
    movies_list_to_show)

st.write('You selected:', selected_movie_name)

#button for

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    import streamlit as st

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])


    with col3:
        st.text(names[2])
        st.image(posters[2])

    with (col4):
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


else:
    st.write("Movie not found!")