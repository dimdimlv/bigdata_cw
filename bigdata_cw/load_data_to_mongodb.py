import os
import pandas as pd
from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configurations
CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
DB_NAME = "imdb_project"
RAW_DATA_DIR = Path(__file__).resolve().parents[1] / 'data' / 'raw'

# Establish MongoDB connection
client = MongoClient(CONNECTION_STRING)
db = client[DB_NAME]
movies_collection = db["movies"]
people_collection = db["people"]


def load_filtered_movies(file_path, collection, subset_size=2000, essential_columns=None, filter_condition=None):
    """
    Load a filtered subset of movies into MongoDB.

    Args:
        file_path (str or Path): Path to the TSV file.
        collection (Collection): MongoDB collection to insert the data.
        subset_size (int): Number of rows to load from the dataset.
        essential_columns (list): List of columns to keep in the dataset.
        filter_condition (function, optional): Function to filter rows (applied to DataFrame).
    """
    # Load the data in chunks to manage memory usage
    records = []
    chunk_size = 10000
    for chunk in pd.read_csv(file_path, sep='\t', na_values='\\N', usecols=essential_columns, chunksize=chunk_size,
                             low_memory=False):
        if filter_condition:
            chunk = chunk[filter_condition(chunk)]
        records.extend(chunk.to_dict(orient='records'))
        if len(records) >= subset_size:
            records = records[:subset_size]
            break

    # Insert records into MongoDB if not empty
    if records:
        collection.insert_many(records)
        print(f"Inserted {len(records)} records from {file_path.name} into MongoDB collection: {collection.name}")
    else:
        print(f"No records to insert for {file_path.name}")

    # Return the list of tconst (movie IDs) for further filtering of people data
    return set([record["tconst"] for record in records])


def load_people_connected_to_movies(file_path, collection, movie_ids_to_keep, essential_columns=None):
    """
    Load people data that are connected to the filtered movies.

    Args:
        file_path (str or Path): Path to the TSV file.
        collection (Collection): MongoDB collection to insert the data.
        movie_ids_to_keep (set): Set of tconst IDs of movies to keep.
        essential_columns (list): List of columns to keep in the dataset.
    """
    # Load the people data into a pandas DataFrame with selected columns
    records = []
    chunk_size = 10000
    for chunk in pd.read_csv(file_path, sep='\t', na_values='\\N', usecols=essential_columns, chunksize=chunk_size,
                             low_memory=False):
        # Filter people whose knownForTitles intersect with selected movie IDs
        def filter_people(df):
            return df['knownForTitles'].apply(
                lambda titles: any(tconst in movie_ids_to_keep for tconst in str(titles).split(',')))

        filtered_chunk = chunk[filter_people(chunk)]
        records.extend(filtered_chunk.to_dict(orient='records'))

    # Insert records into MongoDB if not empty
    if records:
        collection.insert_many(records)
        print(f"Inserted {len(records)} records from {file_path.name} into MongoDB collection: {collection.name}")
    else:
        print(f"No records to insert for {file_path.name}")


if __name__ == "__main__":
    try:
        # Step 1: Load filtered movies data (2000 records)
        title_basics_path = RAW_DATA_DIR / "title.basics.tsv"
        essential_columns_movies = ["tconst", "primaryTitle", "startYear", "genres", "runtimeMinutes"]


        # Filter to include only movies released after 2000
        def filter_condition(df):
            return df['startYear'].fillna(0).astype(int) >= 2000


        movie_ids_to_keep = load_filtered_movies(title_basics_path, movies_collection, subset_size=2000,
                                                 essential_columns=essential_columns_movies,
                                                 filter_condition=filter_condition)

        # Step 2: Load people data connected to the filtered movies
        name_basics_path = RAW_DATA_DIR / "name.basics.tsv"
        essential_columns_people = ["nconst", "primaryName", "primaryProfession", "knownForTitles"]

        load_people_connected_to_movies(name_basics_path, people_collection, movie_ids_to_keep,
                                        essential_columns=essential_columns_people)

    except Exception as e:
        # Handle any exceptions that occur during the process and print the error message
        print(f"An error occurred: {e}")