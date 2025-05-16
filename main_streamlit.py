import streamlit as st
import requests
import json

# API URLs
API_BASE_URL = "http://127.0.0.1:8000"
RANDOM_MOVIE_URL = f"{API_BASE_URL}/movies/random/"
SUMMARY_URL = f"{API_BASE_URL}/generate_summary/"

# App title
st.title("Movie Explorer")
st.write("Discover movies and get AI-generated summaries!")

# Initialize session state for storing movie data if not already initialized
if "movie" not in st.session_state:
    st.session_state.movie = None
if "summary" not in st.session_state:
    st.session_state.summary = None

# Function to fetch a random movie
def get_random_movie():
    try:
        response = requests.get(RANDOM_MOVIE_URL)
        
        if response.status_code == 200:
            # Store the movie data in session state
            st.session_state.movie = response.json()
            # Clear any existing summary when getting a new movie
            st.session_state.summary = None
            return True
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Failed to fetch random movie: {str(e)}")
        return False

# Function to generate a summary for the current movie
def generate_summary():
    if not st.session_state.movie:
        st.warning("Please load a movie first before generating a summary.")
        return
    
    try:
        # Get the movie_id from session state
        movie_id = st.session_state.movie["id"]
        
        # Make the API request to generate a summary
        response = requests.post(
            SUMMARY_URL,
            json={"movie_id": movie_id}
        )
        
        if response.status_code == 200:
            # Store the summary in session state
            st.session_state.summary = response.json()["summary_text"]
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Failed to generate summary: {str(e)}")

# Button to fetch a random movie
if st.button("Show Random Movie"):
    get_random_movie()

# Display movie details if a movie is loaded
if st.session_state.movie:
    movie = st.session_state.movie
    
    # Display movie info
    st.header(f"{movie['title']} ({movie['year']})")
    st.subheader(f"Directed by {movie['director']}")
    
    # Display actors
    st.write("#### Starring:")
    for actor in movie['actors']:
        st.write(f"- {actor['actor_name']}")
    
    # Button to generate summary (only enabled if a movie is loaded)
    if st.button("Get Summary"):
        generate_summary()
    
    # Display summary if available
    if st.session_state.summary:
        st.write("#### Movie Summary:")
        st.info(st.session_state.summary)
else:
    st.info("Click 'Show Random Movie' to get started!")

# Add a note at the bottom
st.markdown("---")
st.caption("Note: Make sure the FastAPI backend is running on http://127.0.0.1:8000")
