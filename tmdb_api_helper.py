from tmdbv3api import TMDb, Movie, Person
import os

# Try Streamlit secrets first (for cloud)
api_key = None
try:
    import streamlit as st
    api_key = st.secrets["tmdb"]["TMDB_API_KEY"]
except Exception:
    # Local dev: load from .env
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY not set.")

tmdb = TMDb()    
tmdb.api_key = api_key
tmdb.language = "en"

# API objects
movie_api = Movie()
person_api = Person()

def get_movie_info(movie_name: str):
    """Fetch movie details from TMDb."""
    if not movie_name:
        return None

    results = movie_api.search(movie_name)
    if not results:
        return None

    movie_id = results[0].id
    details = movie_api.details(movie_id)

    return {
        "title": details.title,
        "release_date": details.release_date,
        "overview": details.overview,
        "genres": [g['name'] for g in details.genres],
        "runtime": details.runtime,
    }

def get_person_info(name: str):
    """Fetch actor/person details from TMDb."""
    if not name or not isinstance(name, str):
        return None

    query = name.strip()
    if not query:
        return None

    try:
        results = person_api.search(query)
    except Exception as e:
        print(f"API error for '{query}': {e}")
        return None

    if not results:
        return None

    person = results[0]
    details = person_api.details(person.id)

    return {
        "name": details.name,
        "birthday": details.birthday,
        "place_of_birth": details.place_of_birth,
        "biography": details.biography,
    }
