from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    director = Column(String)
    
    # Relationship with Actors table
    actors = relationship("Actors", back_populates="movie", cascade="all, delete-orphan")


class Actors(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    actor_name = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    
    # Relationship with Movies table
    movie = relationship("Movies", back_populates="actors")
