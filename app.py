import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.omdb_api import get_movie_details

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Movie Sphere",
    page_icon="🌍",
    layout="centered"
)

# 🌌 BACKGROUND
st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 50% 20%,
            rgba(20, 45, 120, 0.25),
            transparent 45%
        ),
        linear-gradient(
            180deg,
            #010207 0%,
            #030713 45%,
            #02040B 100%
        );
}

</style>
""", unsafe_allow_html=True)

# 🎬 MOVIE CARD STYLING
st.markdown("""
<style>

.movie-card {
    background: rgba(10, 20, 45, 0.75);
    border: 1px solid rgba(100, 150, 255, 0.25);
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
    text-align: center;
}

.movie-card-title {
    font-size: 16px;
    font-weight: 600;
    margin-top: 8px;
}

.movie-card-info {
    font-size: 13px;
    opacity: 0.8;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)

# LOAD DATASET
movies = pd.read_csv("data/movies.csv")

movies.columns = movies.columns.str.strip()

# DETECT GENRE COLUMN
if "genre" in movies.columns:

    genre_column = "genre"

elif "genres" in movies.columns:

    genre_column = "genres"

else:

    st.error(
        "❌ Genre column was not found in movies.csv."
    )

    st.write(
        "Available columns:",
        movies.columns.tolist()
    )

    st.stop()

# CLEAN DATA
movies["title"] = movies["title"].fillna("")

movies[genre_column] = (
    movies[genre_column]
    .fillna("")
)

# RECOMMENDATION ENGINE
vectorizer = CountVectorizer()

genre_matrix = vectorizer.fit_transform(
    movies[genre_column]
)


def recommend_movies(
    movie_title,
    number_of_recommendations=5
):

    movie_index = movies[
        movies["title"].str.lower()
        == movie_title.lower()
    ].index

    if len(movie_index) == 0:

        return pd.DataFrame()

    index = movie_index[0]

    similarity_scores = cosine_similarity(
        genre_matrix[index],
        genre_matrix
    ).flatten()

    similar_indices = (
        similarity_scores.argsort()[::-1]
        [1:number_of_recommendations + 1]
    )

    return movies.iloc[similar_indices]

#  MAIN PAGE
st.title("🌍 MOVIE SPHERE 🎥")

st.write(
    "Welcome to Movie Sphere! 👫🍿"
)

st.info(
    "Discover movies you may love."
)

#  MOVIE SEARCH
st.subheader("🔍 Search for a Movie")

search = st.text_input(
    "Enter a movie name:",
    placeholder="Example: Inception"
)


if search:

    movie_data = get_movie_details(search)

    if movie_data.get("Response") == "True":

        st.success(
            f"🎬 {movie_data['Title']} found!"
        )

        col1, col2 = st.columns([1, 2])

        with col1:

            poster = movie_data.get("Poster")

            if poster and poster != "N/A":

                st.image(
                    poster,
                    use_container_width=True
                )

            else:

                st.info(
                    "🖼️ Poster not available."
                )

        with col2:

            st.subheader(
                movie_data.get(
                    "Title",
                    "Unknown"
                )
            )

            st.write(
                f"📅 **Year:** "
                f"{movie_data.get('Year', 'N/A')}"
            )

            st.write(
                f"⭐ **IMDB Rating:** "
                f"{movie_data.get('imdbRating', 'N/A')}"
            )

            st.write(
                f"🎭 **Cast:** "
                f"{movie_data.get('Actors', 'N/A')}"
            )

            st.write(
                f"🎥 **Director:** "
                f"{movie_data.get('Director', 'N/A')}"
            )

            st.write(
                f"🎭 **Genre:** "
                f"{movie_data.get('Genre', 'N/A')}"
            )

        st.markdown("### 📝 Story")

        st.write(
            movie_data.get(
                "Plot",
                "No plot available."
            )
        )

    else:

        st.warning(
            "❌ Movie not found. Try another name."
        )

#  FAMOUS MOVIE FRANCHISES
st.subheader("🔥 Famous Movie Franchises")

franchises = {

    "Harry Potter": [
        "Harry Potter and the Sorcerer's Stone",
        "Harry Potter and the Chamber of Secrets",
        "Harry Potter and the Prisoner of Azkaban",
        "Harry Potter and the Goblet of Fire",
        "Harry Potter and the Order of the Phoenix",
        "Harry Potter and the Half-Blood Prince",
        "Harry Potter and the Deathly Hallows: Part 1",
        "Harry Potter and the Deathly Hallows: Part 2"
    ],

    "Fast & Furious": [
        "The Fast and the Furious",
        "2 Fast 2 Furious",
        "The Fast and the Furious: Tokyo Drift",
        "Fast & Furious",
        "Fast Five",
        "Fast & Furious 6",
        "Furious 7",
        "The Fate of the Furious"
    ],

    
    "Spider-Man": [
    "Spider-Man",
    "Spider-Man 2",
    "Spider-Man 3",
    "The Amazing Spider-Man",
    "The Amazing Spider-Man 2",
    "Spider-Man: Homecoming",
    "Spider-Man: Far From Home",
    "Spider-Man: No Way Home"
],

    "Marvel": [
        "Iron Man",
        "The Incredible Hulk",
        "Iron Man 2",
        "Thor",
        "Captain America: The First Avenger",
        "The Avengers",
        "Iron Man 3",
        "Thor: The Dark World"
    ],

    "DC": [
        "Man of Steel",
        "Batman v Superman: Dawn of Justice",
        "Suicide Squad",
        "Wonder Woman",
        "Justice League",
        "Aquaman",
        "Shazam!",
        "The Batman"
    ],

    "Transformers": [
        "Transformers",
        "Transformers: Revenge of the Fallen",
        "Transformers: Dark of the Moon",
        "Transformers: Age of Extinction",
        "Transformers: The Last Knight",
        "Bumblebee",
        "Transformers: Rise of the Beasts"
    ],

    "Star Wars": [
        "Star Wars",
        "The Empire Strikes Back",
        "Return of the Jedi",
        "The Phantom Menace",
        "Revenge of the Sith",
        "The Force Awakens",
        "The Last Jedi"
    ],

    "Mission: Impossible": [
        "Mission: Impossible",
        "Mission: Impossible II",
        "Mission: Impossible III",
        "Mission: Impossible - Ghost Protocol",
        "Mission: Impossible - Rogue Nation",
        "Mission: Impossible - Fallout"
    ],

    "Pirates of the Caribbean": [
        "Pirates of the Caribbean: The Curse of the Black Pearl",
        "Pirates of the Caribbean: Dead Man's Chest",
        "Pirates of the Caribbean: At World's End",
        "Pirates of the Caribbean: On Stranger Tides",
        "Pirates of the Caribbean: Dead Men Tell No Tales"
    ],

    "Jurassic Park": [
        "Jurassic Park",
        "The Lost World: Jurassic Park",
        "Jurassic Park III",
        "Jurassic World",
        "Jurassic World: Fallen Kingdom",
        "Jurassic World Dominion",
        "Jurassic World Rebirth"
    ],

    "MonsterVerse": [
        "Godzilla",
        "Kong: Skull Island",
        "Godzilla: King of the Monsters",
        "Godzilla vs. Kong",
        "Godzilla x Kong: The New Empire"
    ],

    "Baahubali": [
        "Baahubali: The Beginning",
        "Baahubali 2: The Conclusion"
    ],

    "Doraemon": [
        "Doraemon: Nobita's Dinosaur",
        "Doraemon: Nobita's Little Star Wars",
        "Doraemon: Nobita and the Steel Troops"
    ],

    "Shin-chan": [
        "Crayon Shin-chan: The Hidden Treasure of the Buri Buri Kingdom",
        "Crayon Shin-chan: Pursuit of the Balls of Darkness"
    ]
}

#  SELECT FRANCHISE
selected_franchise = st.selectbox(
    "Choose a franchise:",
    ["Select a Franchise"]
    + list(franchises.keys())
)

#  DISPLAY FRANCHISE MOVIES
if selected_franchise != "Select a Franchise":

    st.markdown(
        f"### 🎬 {selected_franchise} Collection"
    )

    movies_list = franchises[
        selected_franchise
    ]

    columns = st.columns(4)

    for index, movie_name in enumerate(
        movies_list
    ):

        movie_data = get_movie_details(
            movie_name
        )

        if movie_data.get("Response") == "True":

            with columns[index % 4]:

                poster = movie_data.get(
                    "Poster"
                )

                if poster and poster != "N/A":

                    st.image(
                        poster,
                        use_container_width=True
                    )

                st.markdown(
                    f"**{movie_data.get('Title', movie_name)}**"
                )

                st.caption(
                    f"📅 {movie_data.get('Year', 'N/A')}  "
                    f"⭐ {movie_data.get('imdbRating', 'N/A')}"
                )

#  MOVIE RECOMMENDATIONS
st.subheader("🎯 Get Movie Recommendations")

# STATE
if "show_genre" not in st.session_state:

    st.session_state.show_genre = False


if "show_recommendations" not in st.session_state:

    st.session_state.show_recommendations = False


if "last_recommended_movie" not in st.session_state:

    st.session_state.last_recommended_movie = None

#  MOVIE SELECTION
movie_options = sorted(
    movies["title"].dropna().unique()
)

selected_movie = st.selectbox(
    "Choose a movie you like:",
    movie_options
)

#  GENRE + RECOMMENDATION BUTTONS
genre_col, recommend_col = st.columns(2)

# 🎭 GENRE BUTTON
with genre_col:

    if st.button(
        "🎭 Explore by Genre",
        use_container_width=True
    ):

        st.session_state.show_genre = (
            not st.session_state.show_genre
        )

# ✨ RECOMMENDATION BUTTON
with recommend_col:

    if st.button(
        "✨ Recommend Movies",
        use_container_width=True
    ):

        st.session_state.show_recommendations = True

        st.session_state.last_recommended_movie = (
            selected_movie
        )

# 🎭 GENRE EXPLORER
if st.session_state.show_genre:

    st.subheader("🎞️ Explore by Genre")

    all_genres = sorted(
        set(
            genre.strip()
            for genres in movies[genre_column]
            for genre in genres.split("|")
            if genre.strip()
        )
    )

    selected_genre = st.selectbox(
        "Choose a genre:",
        ["Select a genre"] + all_genres
    )

    # DISPLAY GENRE RESULTS
    if selected_genre != "Select a genre":

        genre_movies = movies[
            movies[genre_column].str.contains(
                selected_genre,
                case=False,
                na=False
            )
        ]

        if not genre_movies.empty:

            st.success(
                f"Movies in {selected_genre} 🎬"
            )

            st.dataframe(
                genre_movies,
                use_container_width=True
            )

        else:

            st.warning(
                "No movies found for this genre."
            )

# DISPLAY RECOMMENDATIONS
if (
    st.session_state.show_recommendations
    and
    st.session_state.last_recommended_movie
    == selected_movie
):

    recommendations = recommend_movies(
        selected_movie,
        number_of_recommendations=10
    )

    if not recommendations.empty:

        st.markdown(
            "### 🎯 Top 10 Movie Recommendations 🍿"
        )

        st.caption(
            f"If you liked **{selected_movie}**, "
            "we hope you like these!"
        )

        st.dataframe(
            recommendations,
            use_container_width=True
        )

    else:

        st.warning(
            "Sorry, no recommendations found."
        )

#  MOVIE COLLECTION
if "show_collection" not in st.session_state:

    st.session_state.show_collection = False


if st.button(
    "🎥 Show / Hide Movie Collection",
    use_container_width=True
):

    st.session_state.show_collection = (
        not st.session_state.show_collection
    )


if st.session_state.show_collection:

    st.subheader("🎥 Movie Collection")

    st.dataframe(
        movies,
        use_container_width=True
    )

# FOOTER
st.markdown("---")

st.caption(
    "🎬 Movie Sphere · Discover. Explore. Enjoy. 💃"
)