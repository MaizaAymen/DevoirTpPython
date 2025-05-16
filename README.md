# Movie Explorer App

A full-stack application that allows users to explore movies, view details, and generate AI-powered summaries using FastAPI and Streamlit.
![alt text](img/image.png)
## Features

- Browse random movies from the database
- View movie details including actors
- Generate AI summaries using Groq LLM

## Project Structure

- **Backend**: FastAPI API with postgres
- **Frontend**: Streamlit web interface
- **AI Integration**: Groq LLM for generating movie summaries

## Setup and Installation

### Prerequisites

- Python 3.8+
- Groq API key (get one from [groq.com](https://console.groq.com/keys))

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Create or update the `.env` file in the project root:

```
# Database configuration - postgres used by default
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/movies_db


# Groq API Key
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual Groq API key.

### Step 3: Initialize the Database and Add Movies

Before using the frontend, you need to start the FastAPI server and add some sample movies:

1. Start the FastAPI server:
```bash
python -m uvicorn main:app --reload
```

2. Add sample movies using one of these methods:
   - Run the provided test script: `python test_api.py`
   - Use the Swagger UI at http://127.0.0.1:8000/docs to add movies through the `/movies/` endpoint
   - Use Postman to send POST requests to http://127.0.0.1:8000/movies/

### Step 4: Run the Streamlit Frontend

In a new terminal (while keeping the FastAPI server running), start the Streamlit app:

```bash
streamlit run main_streamlit.py
```

The web interface will open at http://localhost:8501

## API Endpoints

- `POST /movies/`: Create a new movie with actors
- `GET /movies/random/`: Get a random movie with its actors
- `POST /generate_summary/`: Generate an AI summary for a movie
- `GET /`: Welcome message

## Questions

### Why is it often necessary to commit the primary record (Movies) before creating the related records (Actors) that depend on its foreign key?

It's necessary to commit the primary record (Movies) before creating related records (Actors) because:

1. The primary record needs to be persisted to the database to generate its primary key (id).
2. The related records need this primary key value as their foreign key (movie_id).
3. Without committing first, the primary key might not be available, resulting in foreign key constraint violations.
4. The `db.refresh(db_movie)` call after commit ensures the SQLAlchemy object has the database-generated ID.

### What is the difference between lazy loading and eager loading (like joinedload) for relationships in SQLAlchemy?

**Lazy Loading:**
- Relationships are loaded only when explicitly accessed
- Results in N+1 query problem (one query for parent, then one for each child)
- Good for when you don't always need the related data
- Default behavior in SQLAlchemy

**Eager Loading (joinedload):**
- Relationships are loaded upfront in a single query using JOINs
- More efficient when you know you'll need the related data
- Prevents the N+1 query problem
- Must be explicitly specified using methods like `joinedload()`

### How would you format the list of actors fetched from the database into a simple string suitable for inclusion in the LLM prompt?

To format the list of actors as a comma-separated string:

```python
actor_names = [actor.actor_name for actor in movie.actors]
if len(actor_names) > 1:
    # Join all actors except the last one with commas, and add the last one with "and"
    actor_list = ", ".join(actor_names[:-1]) + " and " + actor_names[-1]
else:
    actor_list = actor_names[0] if actor_names else "unknown actors"
```

This approach formats the actors list with proper comma separation and adds "and" before the final actor, which is a natural way of presenting a list in English. For example: "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page and Tom Hardy".

In our `/movies/random/` endpoint, we use eager loading with `joinedload(models.Movies.actors)` to fetch both the movie and its actors in a single database query, which is more efficient than lazy loading would be.
