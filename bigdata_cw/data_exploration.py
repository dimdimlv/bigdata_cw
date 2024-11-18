import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configurations
CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
DB_NAME = "imdb_project"

# Establish MongoDB connection
client = MongoClient(CONNECTION_STRING)
db = client[DB_NAME]
movies_collection = db["movies"]
people_collection = db["people"]


def count_documents():
    """ Count the number of documents in each collection. """
    num_movies = movies_collection.count_documents({})
    num_people = people_collection.count_documents({})

    print(f"Number of movies: {num_movies}")
    print(f"Number of people: {num_people}")


def get_sample_documents():
    """ Get and print sample documents from each collection. """
    # Sample movies
    print("\nSample Movies:")
    sample_movies = movies_collection.find().limit(5)
    for movie in sample_movies:
        print(movie)

    # Sample people
    print("\nSample People:")
    sample_people = people_collection.find().limit(5)
    for person in sample_people:
        print(person)


def verify_relationships():
    """ Verify relationships between movies and people. """
    # Find people connected to a sample movie
    sample_movie = movies_collection.find_one()
    if sample_movie:
        movie_id = sample_movie['tconst']
        print(f"\nSample Movie: {sample_movie['primaryTitle']}")

        related_people = people_collection.find({"knownForTitles": {"$regex": movie_id}})
        print("\nPeople related to the movie:")
        for person in related_people:
            print(f"Related Person: {person['primaryName']}, Professions: {person['primaryProfession']}")


def run_aggregation():
    """ Run aggregation to find relationships between movies and people. """
    pipeline = [
        {
            "$lookup": {
                "from": "people",
                "localField": "tconst",
                "foreignField": "knownForTitles",
                "as": "related_people"
            }
        },
        {
            "$project": {
                "primaryTitle": 1,
                "startYear": 1,
                "genres": 1,
                "related_people.primaryName": 1,
                "related_people.primaryProfession": 1
            }
        },
        {
            "$limit": 5
        }
    ]

    print("\nAggregated Movie Data with Related People:")
    enriched_movies = list(movies_collection.aggregate(pipeline))
    for movie in enriched_movies:
        print(movie)


def run_improved_aggregation():
    """ Run improved aggregation to find relationships between movies and people. """
    pipeline = [
        {
            "$lookup": {
                "from": "people",
                "let": {"movie_id": "$tconst"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {"$in": ["$$movie_id", {"$split": ["$knownForTitles", ","]}]}
                        }
                    }
                ],
                "as": "related_people"
            }
        },
        {
            "$project": {
                "primaryTitle": 1,
                "startYear": 1,
                "genres": 1,
                "related_people.primaryName": 1,
                "related_people.primaryProfession": 1
            }
        },
        {
            "$limit": 5
        }
    ]

    print("\nImproved Aggregated Movie Data with Related People:")
    enriched_movies = list(movies_collection.aggregate(pipeline))
    for movie in enriched_movies:
        print(movie)


def validate_relationship_counts():
    """ Validate the number of people related to each movie. """
    pipeline = [
        {
            "$lookup": {
                "from": "people",
                "localField": "tconst",
                "foreignField": "knownForTitles",
                "as": "related_people"
            }
        },
        {
            "$project": {
                "primaryTitle": 1,
                "related_people_count": {"$size": "$related_people"}
            }
        },
        {
            "$limit": 10
        }
    ]

    print("\nMovies with Number of Related People:")
    movies_people_count = list(movies_collection.aggregate(pipeline))
    for movie in movies_people_count:
        print(f"Movie: {movie['primaryTitle']}, Number of Related People: {movie['related_people_count']}")


if __name__ == "__main__":
    try:
        # Step 1: Count the number of documents in each collection
        count_documents()

        # Step 2: Get sample documents from each collection
        get_sample_documents()

        # Step 3: Verify relationships between movies and people
        verify_relationships()

        # Step 4: Run aggregation to explore relationships between movies and people
        #run_aggregation()
        run_improved_aggregation()

        # Step 5: Validate the number of people related to each movie
        validate_relationship_counts()

    except Exception as e:
        # Handle any exceptions that occur during the process and print the error message
        print(f"An error occurred: {e}")