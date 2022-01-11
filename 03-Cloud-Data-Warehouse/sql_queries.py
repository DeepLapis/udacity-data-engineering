import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# Getting Variables
LOG_DATA = config.get("S3","LOG_DATA")
SONG_DATA = config.get("S3","SONG_DATA")
LOG_JSONPATH = config.get("S3","LOG_JSONPATH")


# Credentials
ARN = config.get("IAM_ROLE","ARN")


# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events" 
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events(
        artist          TEXT, 
        auth            TEXT, 
        firstName       TEXT, 
        gender          TEXT, 
        itemInSession   INTEGER, 
        lastName        TEXT,
        length          FLOAT, 
        level           TEXT, 
        location        TEXT, 
        method          TEXT, 
        page            TEXT, 
        registration    TEXT,
        sessionId       INTEGER, 
        song            TEXT, 
        status          INTEGER, 
        ts              BIGINT, 
        userAgent       TEXT,
        userId          INTEGER
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        artist_id          TEXT, 
        artist_latitude    NUMERIC, 
        artist_location    TEXT, 
        artist_longitude   NUMERIC,
        artist_name        TEXT,      
        duration           FLOAT, 
        num_songs          INTEGER, 
        song_id            TEXT, 
        title              TEXT, 
        year               INTEGER
    )
        
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id    INTEGER IDENTITY(0,1) NOT NULL sortkey,
        start_time     TIMESTAMP NOT NULL,
        user_id        INTEGER NOT NULL, 
        level          TEXT NOT NULL, 
        song_id        TEXT NOT NULL,
        artist_id      TEXT NOT NULL,
        session_id     INTEGER NOT NULL, 
        location       TEXT NOT NULL,
        user_agent     TEXT NOT NULL
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id      INTEGER NOT NULL PRIMARY KEY sortkey,
        first_name   TEXT NOT NULL,
        last_name    TEXT NOT NULL,
        gender       TEXT NOT NULL,
        level        TEXT NOT NULL
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id     TEXT NOT NULL PRIMARY KEY sortkey, 
        title       TEXT NOT NULL,
        artist_id   TEXT NOT NULL,
        year        INTEGER NOT NULL,
        duration    FLOAT NOT NULL
    )
        
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id  TEXT NOT NULL PRIMARY KEY sortkey,
        name       TEXT NOT NULL,
        location   TEXT,
        latitude   NUMERIC,
        longitude  NUMERIC
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time  TIMESTAMP NOT NULL sortkey,
        hour        INTEGER NOT NULL,
        day         INTEGER NOT NULL,
        week        INTEGER NOT NULL,
        month       INTEGER NOT NULL,
        year        INTEGER NOT NULL,
        weekday     INTEGER NOT NULL
    )
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events
    FROM {}
    iam_role {}
    json {};
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    COPY staging_songs
    FROM {}
    iam_role {}
    json 'auto';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (
        start_time,
        user_id, 
        level, 
        song_id,
        artist_id,
        session_id, 
        location,
        user_agent
    )
    
    SELECT
        DISTINCT TIMESTAMP WITH TIME ZONE 'epoch' + staging_events.ts/1000 * interval '1 second' AS start_time,
        staging_events.userId AS user_id,
        staging_events.level AS level,
        staging_songs.song_id AS song_id,
        staging_songs.artist_id AS artist_id,
        staging_events.sessionId AS session_id,
        staging_songs.artist_location AS location,
        staging_events.userAgent AS user_agent
    FROM staging_events
    JOIN staging_songs
      ON staging_events.song = staging_songs.title 
     AND staging_events.artist = staging_songs.artist_name 
     AND staging_events.length = staging_songs.duration
     AND staging_events.page='NextSong'
     AND staging_events.ts IS NOT NULL
""")

user_table_insert = ("""
    INSERT INTO users (
        user_id,
        first_name,
        last_name,
        gender,
        level
    )
    
    SELECT
        DISTINCT userId AS userId,
        firstName,
        lastName,
        gender,
        level
    FROM staging_events
    WHERE staging_events.page='NextSong'
      AND userId IS NOT NULL
""")

song_table_insert = ("""
    INSERT INTO songs (
        song_id,
        title,   
        artist_id,  
        year,
        duration
    )
    
    SELECT
        DISTINCT song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
    WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
    INSERT INTO artists (
        artist_id,
        name,
        location,
        latitude,
        longitude
    )
    
    SELECT
        DISTINCT artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL
  
""")

time_table_insert = ("""
    INSERT INTO time (
        start_time,
        hour,      
        day,       
        week,      
        month,     
        year,     
        weekday
    )
        
    SELECT 
        start_time, 
        EXTRACT(hour FROM start_time), 
        EXTRACT(day FROM start_time), 
        EXTRACT(week FROM start_time), 
        EXTRACT(month FROM start_time), 
        EXTRACT(year FROM start_time), 
        EXTRACT(weekday FROM start_time)
    FROM songplays
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, 
                        staging_songs_table_create, 
                        songplay_table_create, 
                        user_table_create, 
                        song_table_create, 
                        artist_table_create, 
                        time_table_create]


drop_table_queries = [staging_events_table_drop, 
                      staging_songs_table_drop, 
                      songplay_table_drop, 
                      user_table_drop, 
                      song_table_drop, 
                      artist_table_drop, 
                      time_table_drop]


copy_table_queries = [staging_events_copy, 
                      staging_songs_copy]


insert_table_queries = [songplay_table_insert, 
                        user_table_insert, 
                        song_table_insert, 
                        artist_table_insert, 
                        time_table_insert]
