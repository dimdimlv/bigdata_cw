import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configurations
CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
DB_NAME = "imdb_project"

# Establish MongoDB connection
client = MongoClient(CONNECTION_STRING)
db = client[DB_NAME]
reviews_collection = db["reviews"]
movies_collection = db["movies"]

OMDB_API_URL = "http://www.omdbapi.com/"


def fetch_movie_data(tconst):
    """ Fetch movie data from OMDB API using tconst (IMDb ID). """
    params = {
        'apikey': OMDB_API_KEY,
        'i': tconst
    }
    response = requests.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {tconst}: {response.status_code}")
        return None


def add_omdb_reviews():
    """ Add reviews and metadata fetched from OMDB API to MongoDB incrementally. """
    # Query movies without omdb_loaded flag or where it's set to False
    movies_to_process = movies_collection.find(
        {"$or": [{"omdb_loaded": {"$exists": False}}, {"omdb_loaded": False}]},
        {"tconst": 1}
    ).limit(900)

    movie_ids = [movie["tconst"] for movie in movies_to_process]

    for tconst in movie_ids:
        movie_data = fetch_movie_data(tconst)

        if movie_data and movie_data.get('Response') == 'True':
            # Extract necessary data from OMDB response
            review_data = {
                "tconst": tconst,
                "title": movie_data.get("Title"),
                "year": movie_data.get("Year"),
                "plot": movie_data.get("Plot"),
                "ratings": movie_data.get("Ratings"),
                "imdbRating": movie_data.get("imdbRating"),
                "source": "OMDB"
            }

            # Insert the review into MongoDB
            reviews_collection.insert_one(review_data)
            print(f"Inserted OMDB review for movie ID: {tconst}")

            # Mark the movie as processed in the movies collection
            movies_collection.update_one({"tconst": tconst}, {"$set": {"omdb_loaded": True}})
        else:
            # Mark as failed to avoid retrying too soon
            movies_collection.update_one({"tconst": tconst}, {"$set": {"omdb_loaded": False}})


if __name__ == "__main__":
    try:
        add_omdb_reviews()
        print("OMDB reviews added successfully for up to 1000 movies.")
    except Exception as e:
        print(f"An error occurred: {e}")