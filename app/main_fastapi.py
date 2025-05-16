from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List
import os

# Import for Langchain and Groq integration
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain

from app import models, schemas
from app.database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Movies API")

# Initialize the Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama3-70b-8192"  # Using llama3-70b model, can be changed as needed
)

# Create a prompt template for movie summaries
movie_summary_template = PromptTemplate(
    input_variables=["title", "year", "director", "actor_list"],
    template="Generate a short, engaging summary for the movie '{title}' ({year}), " + 
             "directed by {director} and starring {actor_list}."
)

# Create a Langchain chain
summary_chain = LLMChain(llm=llm, prompt=movie_summary_template)


@app.post("/movies/", response_model=schemas.MoviePublic)
def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_db)):
    """
    Create a new movie with its actors.
    
    First create and commit the movie record, then create the actor records
    that depend on the movie's primary key.
    """
    # Create movie first
    db_movie = models.Movies(
        title=movie.title,
        year=movie.year,
        director=movie.director
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)  # Refresh to get the generated id
    
    # Now create actors with the movie_id FK
    for actor in movie.actors:
        db_actor = models.Actors(
            actor_name=actor.actor_name,
            movie_id=db_movie.id
        )
        db.add(db_actor)
    
    db.commit()
    db.refresh(db_movie)  # Refresh again to get the actors
    
    return db_movie


@app.get("/movies/random/", response_model=schemas.MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    """
    Get a random movie from the database along with its actors.
    
    Uses eager loading to fetch the actors along with the movie in a single query.
    """
    # Query for a random movie with its actors
    movie = db.query(models.Movies).options(
        joinedload(models.Movies.actors)
    ).order_by(func.random()).first()
    
    # Handle case where no movies exist
    if not movie:
        raise HTTPException(status_code=404, detail="No movies found in the database")
    
    return movie


@app.post("/generate_summary/", response_model=schemas.SummaryResponse)
def generate_summary(req: schemas.SummaryRequest, db: Session = Depends(get_db)):
    """
    Generate a summary for a movie using the Groq LLM.
    
    Takes a movie_id, retrieves the movie details from the database,
    and uses the Groq LLM to generate a summary.
    """
    # Get the movie with its actors
    movie = db.query(models.Movies).options(
        joinedload(models.Movies.actors)
    ).filter(models.Movies.id == req.movie_id).first()
    
    # Handle case where movie doesn't exist
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with ID {req.movie_id} not found")
    
    # Format the actor list into a comma-separated string
    actor_names = [actor.actor_name for actor in movie.actors]
    if len(actor_names) > 1:
        # Join all actors except the last one with commas, and add the last one with "and"
        actor_list = ", ".join(actor_names[:-1]) + " and " + actor_names[-1]
    else:
        actor_list = actor_names[0] if actor_names else "unknown actors"
    
    # Generate the summary
    summary = summary_chain.invoke({
        "title": movie.title,
        "year": movie.year,
        "director": movie.director,
        "actor_list": actor_list
    })
    
    return {"summary_text": summary["text"]}


@app.get("/")
def read_root():
    return {"message": "Welcome to Movies API. Go to /docs for the API documentation."}
