# Setup environment
- [x] Create a new virtual environment
- [x] Install the required packages
- [x] Create project structure
- [x] Add project to Github
# Data preparation
- [x] Download data
- [ ] Clean data
- [ ] Create final data sets
- [ ] Store final data sets
- [ ] Document data preparation
# Setup database
- [ ] Create MongoDB database
- [ ] Create collections
- [ ] Store data in database
With the 2GB limit, we’ll need to make efficient use of storage. Here are some strategies to work within this limit:
1. Store only essential fields
2. Limit the number of records
   - Partial Data Load: Instead of loading the entire IMDb datasets, load a subset of the data (e.g., only movies released after the year 2000 or those with more than 50,000 votes).
   - Filter by Popular Titles: Load only the most popular titles using a condition on numVotes or averageRating.
Data has been successfully inserted into MongoDB with the correct filtering applied.
Movies Collection: 2000 records
People Collection: 83,967 records connected to those movies
3. Optimise the data structure

# Data exploration
Results Summary:

	1.	Number of Records:
	•	Movies: 5000
	•	People: 167,011
	•	These counts match our expectations and verify that the data loading was successful.
	2.	Sample Documents:
	•	The sample movies show a diverse set of data, with fields like tconst, primaryTitle, startYear, genres, etc.
	•	The sample people have fields like nconst, primaryName, primaryProfession, and knownForTitles.
	•	The sample data appears correctly structured.
	3.	Relationships Between Movies and People:
	•	For the sample movie "Tötet nicht mehr", we found two related people: "Ivar Petersen" and "Richard Timm".
	•	This suggests that relationships are being established, but let’s delve deeper into why some movies do not show related people.
	4.	Aggregated Data with Related People:
	•	The aggregation results reveal that:
	•	Some movies, like "Kate & Leopold" and "Final Curtain", have several related people listed.
	•	However, movies like "Tötet nicht mehr" and "La tierra de los toros" show zero related people even though related people were found during the sample relationship check.
	•	This discrepancy might indicate a problem in the way the data relationships are being matched during the aggregation.
	5.	Movies with Number of Related People:
	•	We see that some movies have zero related people even though their relationships are known.
	•	Example: "Tötet nicht mehr" has 0 related people in the aggregation result, while the earlier manual check found two related people.

Possible Reasons for Discrepancies:

	1.	Matching Inconsistency:
	•	It’s possible that the $lookup stage in the aggregation isn’t matching people correctly with the movies. This can happen if there are formatting differences between the tconst in the movies collection and the knownForTitles field in the people collection.
	2.	Incorrect Use of Regex:
	•	The manual relationship check uses a regex filter ("$regex": movie_id), which may not be as precise as directly matching the array elements in the knownForTitles field.
	•	Using regex can sometimes lead to false positives or missed matches if there are minor formatting variations.

Recommended Solutions:

To resolve these inconsistencies, let’s modify how relationships are established:
	1.	Improve the $lookup in Aggregation:
	•	Instead of using a simple lookup, we will enhance it with $unwind and $match to ensure better precision when matching movie IDs with knownForTitles.
	2.	Ensure Exact Matching for knownForTitles:
	•	Convert the knownForTitles field to an array if it isn’t already, so that $lookup can perform an exact match instead of relying on regex.


Updated Data Exploration Results Summary:

	1.	Number of Records:
	•	Movies: 5000
	•	People: 167,011
The data loading is still consistent, which is good.
	2.	Sample Movies and People:
	•	The sample movies and people look as expected, with fields like tconst, primaryTitle, nconst, primaryName, and knownForTitles.
	•	People, such as Cameron Diaz and Sandra Bullock, have accurate information regarding their professions and movies they are known for.
	3.	Relationships Between Movies and People:
	•	For the sample movie "The Silent Force", we see that 26 people are related to it, including actors, stunt crew, directors, and others.
	•	This looks consistent, and the number of related people appears to make sense for a feature-length film.
	4.	Improved Aggregated Data with Related People:
	•	In the improved aggregation output, movies like “The Silent Force” and “The Tango of the Widower and Its Distorting Mirror” now show related people correctly.
	•	Example: "The Silent Force" shows multiple crew members like "Loren Avedon" (actor/stunts), "David H. May" (director/writer), and "Alan Kapilow" (producer).
	•	This shows that relationships are more precisely established with the new method.
	5.	Movies with Number of Related People:
	•	Some movies still show zero related people, like "Loading Ludwig" and "Rondo".
	•	This may be due to these movies being lesser-known, with fewer prominent connections or lack of information on their contributors.

Observations and Analysis:

	1.	Improved Relationships:
	•	The improved aggregation appears to better match movies to their respective people, which is evident from the sample movie and aggregation results.
	•	Movies like "The Silent Force" are now correctly linked to a variety of contributors, showing a richer set of relationships.
	2.	Remaining Issues with Zero Relations:
	•	Some movies still have zero related people in the final aggregation. This could be due to:
	•	Incomplete Data: The information in the dataset itself may not be complete for these particular titles, leading to missing relationships.
	•	Genres or Runtime are NaN: Missing or incorrect data in fields like genres or runtimeMinutes might affect how these movies are connected to people.