# 02 Project: Data Modeling with Apache Cassandra

## Assignment
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring you on the project. Your role is to create a database for this analysis. You'll be able to test your database by running queries given to you by the analytics team from Sparkify to create the results.

## Assignment objectives
In this project, skills learnt regarding data modeling for Apache Cassandra will be applied to complete an ETL pipeline using python. 

## Dataset
Only one dataset ```event_data``` will be used. The directory of CSV files partitioned by date. Here are examples of filepaths to two files in the dataset:

```
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
```

## Packages used
* pandas
* cassandra
* re
* os
* glob
* numpy
* json
* csv

## Project Overview
1) ```event_datafile_new.csv``` will be processed to create a denormalized dataset
2) Data tables will be created and modeled in accordance to the query needed
    
    2.1) Since queries are provided, the modeling would revolve around this query

3) The data will be loaded into a Apache Cassandra to run queries

## Queries submitted by data analysts for Cassandra Modeling
1. Give me the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession  = 4

2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
    
3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'

## ETL overview

The data are stored as a collection of csv files partitioned by date. 

The ETL pipeline and data modeling are written in a single jupyter notebook, **Project_1B_ Project_Submission.ipynb**.

Denormalization is performed in order for queries to be done.

1. **`songinfo_session_level`** includes artist, song title and song length information for a given `sessionId` and `itemInSessionId`.

2. **`songinfo_user_session_level`** includes artist, song and user for a given `userId` and `sessionId`.

3. **`user_song_level`** includes user names for a given song.

A pandas DataFrame is returned so that it is easier to read the data

## Running Cassandra Locally

1) Proceed to your terminal and run ```brew install cassandra```
2) Start cassandra by running ```cassandra -f``` in your terminal. It would take some time for the cassandra to start up so do wait for a moment. When it is done your terminal would print ``` INFO  [OptionalTasks:1] <YYYY-MM-DD HH:MM:SS,xxx> CassandraRoleManager.java:338 - Created default superuser role 'cassandra'  ```
3) Open a new terminal and run ```cqlsh```

As a quick orientation:

- use ```DESCRIBE KEYSPACES;``` to see the available keyspace. This lets your delete the keyspace should anything goes wrong in your modeling process and you would like to delete them

- Or you can run ```SELECT * FROM system_schema.keyspaces;``` 
    
    - If you need to drop a keyspace run ```DROP name_of_your_keyspace;```

- To view the tables in a specific keyspace: https://stackoverflow.com/questions/38696316/how-to-list-all-cassandra-tables 

4) Since we are running locally in a Jupyter notebook, you should run ```pip install cassandra-driver```

