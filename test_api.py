import requests
import json

# Define the API endpoint
api_url = "http://127.0.0.1:8000/movies/"
summary_url = "http://127.0.0.1:8000/generate_summary/"

print("Starting test script...")
print(f"API URL: {api_url}")

# Movie 1: Inception
inception = {
  "title": "Inception",
  "year": 2010,
  "director": "Christopher Nolan",
  "actors": [
    {
      "actor_name": "Leonardo DiCaprio"
    },
    {
      "actor_name": "Joseph Gordon-Levitt"
    },
    {
      "actor_name": "Elliot Page"
    },
    {
      "actor_name": "Tom Hardy"
    }
  ]
}

# Movie 2: Pulp Fiction
pulp_fiction = {
  "title": "Pulp Fiction",
  "year": 1994,
  "director": "Quentin Tarantino",
  "actors": [
    {
      "actor_name": "John Travolta"
    },
    {
      "actor_name": "Samuel L. Jackson"
    },
    {
      "actor_name": "Uma Thurman"
    },
    {
      "actor_name": "Bruce Willis"
    }
  ]
}

# Movie 3: The Message
the_message = {
  "title": "Al-Risalah (The Message)",
  "year": 1976,
  "director": "Moustapha Akkad",
  "actors": [
    {
      "actor_name": "Abdullah Gaith (عبد الله غيث)"
    },
    {
      "actor_name": "Muna Wassef (منى واصف)"
    },
    {
      "actor_name": "Hamdi Ghaith (حمدي غيث)"
    },
    {
      "actor_name": "Ahmad Marey (أحمد مرعي)"
    }
  ]
}

# Function to create a movie
def create_movie(movie_data):
    response = requests.post(api_url, json=movie_data)
    if response.status_code == 200:
        print(f"Successfully created movie: {movie_data['title']}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"Failed to create movie: {movie_data['title']}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Create the movies
print("Creating Inception...")
inception_response = create_movie(inception)

print("\nCreating Pulp Fiction...")
pulp_fiction_response = create_movie(pulp_fiction)

print("\nCreating The Message...")
the_message_response = create_movie(the_message)

# Test the random movie endpoint
print("\nTesting the random movie endpoint...")
for i in range(3):
    response = requests.get("http://127.0.0.1:8000/movies/random/")
    if response.status_code == 200:
        movie = response.json()
        print(f"Random movie {i+1}: {movie['title']} ({movie['year']}) directed by {movie['director']}")
        print(f"Actors: {', '.join([actor['actor_name'] for actor in movie['actors']])}")
    else:
        print(f"Failed to get random movie. Status code: {response.status_code}")

# Test the summary generation endpoint
if inception_response:
    print("\nTesting summary generation for Inception...")
    summary_response = requests.post(
        summary_url,
        json={"movie_id": inception_response["id"]}
    )
    
    if summary_response.status_code == 200:
        summary = summary_response.json()
        print("Summary generated successfully!")
        print(f"Summary: {summary['summary_text']}")
    else:
        print(f"Failed to generate summary. Status code: {summary_response.status_code}")
        print(f"Response: {summary_response.text}")
