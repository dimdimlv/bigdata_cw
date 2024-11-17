# Data Dictionary for IMDb Datasets

This data dictionary provides detailed descriptions for each column in the IMDb datasets that are being used for the Big Data project. The datasets include `name.basics.tsv.gz`, `title.basics.tsv.gz`, and `title.ratings.tsv.gz`. These files contain information about people, movies, and ratings from IMDb.

## 1. `name.basics.tsv.gz`

This dataset contains information about people involved in the entertainment industry.
- nconst (string): Alphanumeric unique identifier of the person (e.g., nm0000001). 
- primaryName (string): The name by which the person is most often credited. 
- birthYear (YYYY format): The year the person was born. If unknown, represented as `\N`. 
- deathYear (YYYY format): The year the person died, if applicable. If the person is still alive or if the information is unknown, represented as `\N`.
- primaryProfession (array of strings): The top-3 professions of the person (e.g., actor, director, writer). 
- knownForTitles (array of tconsts): List of titles the person is known for, represented by their unique identifiers (e.g., tt0000001).

## 2. `title.basics.tsv.gz`

This dataset contains basic information about movies, TV shows, and other types of titles.
- tconst (string): Alphanumeric unique identifier of the title (e.g., tt0000001). 
- titleType (string): The type/format of the title (e.g., movie, short, tvseries, tvepisode, video). 
- primaryTitle (string): The more popular or common title used by the filmmakers on promotional materials at the point of release. 
- originalTitle (string): The original title, in the original language. 
- isAdult (boolean): Indicates if the title is intended for adults. `0` represents non-adult content, `1` represents adult content. 
- startYear (YYYY format): The release year of the title. For TV series, this is the series start year. 
- endYear (YYYY format): The end year of a TV series. If not applicable, represented as `\N`. 
- runtimeMinutes (integer): Primary runtime of the title, in minutes. If unknown, represented as `\N`. 
- genres (string array): Up to three genres associated with the title (e.g., Drama, Comedy, Action).

## 3. `title.ratings.tsv.gz`

This dataset contains ratings data for the titles.
- tconst (string): Alphanumeric unique identifier of the title (e.g., tt0000001). 
- averageRating (float): The weighted average of all individual user ratings for the title (on a scale of 1 to 10). 
- numVotes (integer): The number of votes the title has received.

## Usage Notes

- **Identifiers**: The `tconst` and `nconst` identifiers are used to link data across different files. 
- **Missing Values**: Missing values are represented by `\N` in the datasets. Be sure to handle these appropriately during data processing.

This data dictionary will serve as a reference throughout the project to help understand and interpret the contents of each dataset.
