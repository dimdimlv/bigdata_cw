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