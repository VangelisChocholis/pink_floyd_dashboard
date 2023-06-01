import pandas as pd
import sqlite3

# SQL query to get Pink Floyd data
query = '''
SELECT art.id AS artist_id, art.name AS artist_name,
tr.name AS track_name, alb.name AS album_name, alb.id AS album_id, 
alb.release_date AS release_date, tr.duration AS track_duration,
aud_feat.*
FROM
artists art
JOIN r_track_artist tr_art ON art.id = tr_art.artist_id
JOIN r_artist_genre art_gen ON art_gen.artist_id = art.id
JOIN tracks tr ON tr.id = tr_art.track_id
JOIN audio_features aud_feat ON aud_feat.track_id = tr.id
JOIN r_albums_tracks alb_tr ON alb_tr.track_id = tr.id
JOIN albums alb ON alb.id = alb_tr.album_id
WHERE art.name = 'Pink Floyd'
'''
conn = sqlite3.connect('spotify_db.sqlite')
df = pd.read_sql(query, conn)
conn.close()

# remove duplicates
df = df[~df['track_id'].duplicated()]

# remove columns (we already have duration)
df = df.drop(['track_duration', 'analysis_url'], axis=1)

# convert duration to minutes
df['duration'] = df['duration']/60000

# convert to datetime, release_date is in Unix format (in ms)
df['release_date'] = pd.to_datetime(df['release_date'], unit='ms')

# main Pink Floyd albums
album_num_tracks = {
    'The Piper at the Gates of Dawn': 11,
    'A Saucerful of Secrets': 7,
    'More': 13,
    'Ummagumma': 12,
    'Atom Heart Mother': 5,
    'Meddle': 6,
    'Obscured by Clouds': 10,
    'The Dark Side of the Moon': 10,
    'Wish You Were Here': 5,
    'Animals': 5,
    'The Wall': 26,
    'The Final Cut': 13,
    'A Momentary Lapse of Reason': 11,
    'The Division Bell': 11
}

# filter df to inlude tracks from main albums
df = df[df['album_name'].isin(album_num_tracks.keys())]

# remove remastered versions
df = df[~df['track_name'].str.contains('remaster', case=False)]

# remove live versions
df = df[~df['track_name'].str.contains('- live', case=False)]

# save to csv
df.to_csv('pink_floyd_tracks.csv', index=False)
