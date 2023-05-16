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
# save to csv
df.to_csv('pink_floyd_tracks.csv', index=False)