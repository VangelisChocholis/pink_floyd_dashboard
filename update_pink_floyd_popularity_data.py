import pandas as pd
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Change the current working directory to the desired directory
os.chdir('/home/VangelisChocholis/pink_floyd_dashboard')

# read Pink Floyd data
# check get_pink_floyd_data_to_csv.py to see how we got them from a databse
df = pd.read_csv('pink_floyd_tracks.csv')

# acces spotipy
from spotify_config import config
client_id = config['client_id']
client_secret = config['client_secret']
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get current track popularity
pop_list = []
for track_id in df['track_id'].unique():
    try:
        track_pop = sp.track(track_id)['popularity']
        pop_list.append(track_pop)
    except Exception as e:
        print(f"Error retrievig track id '{track_id}': {e}")
        
'''df['track_popularity'] = [sp.track(track_id)['popularity'] for track_id in df['track_id']]'''
df['track_popularity'] = pd.Series(pop_list, name='track_popularity', dtype='int')

# get current album popularity in a dictionary
alb_pop = {}
for alb_id in df['album_id'].unique():
    try:
        album = sp.album(alb_id)
        alb_pop[alb_id] = album['popularity']
    except Exception as e:
        # Handle the exception
        print(f"Error retrieving album ID '{alb_id}': {e}")

# make a DataFrame with album_id and populariy
alb_pop_df = pd.DataFrame(data={'album_id': alb_pop.keys(),
                               'album_popularity': alb_pop.values()})

# merge to pass album popularity information
df = pd.merge(df, alb_pop_df, on='album_id')


# save to csv
df.to_csv('pink_floyd_tracks_updated.csv', index=False)


# check number of tracks and save to csv
'''tot_tracks = sum(album_num_tracks.values())
if tot_tracks == df.shape[0]:
    df.to_csv('pink_floyd_tracks_updated.csv', index=False)
else:
    raise Exception('Error! Unable to collect the correct number of tracks')'''



# get current Pink Floyd popularity
pink_floyd_popularity = sp.artist(df['artist_id'][0])['popularity']
# read popularity by date csv
pink_floyd_art_pop = pd.read_csv('pink_floyd_artist_popularity.csv')
current_date = date.today()
pop_dict = {'date': [current_date],
          'artist_popularity': [pink_floyd_popularity]}

# make new df
pink_floyd_art_pop_new = pd.DataFrame(pop_dict)
# concat old and new
p = pd.concat((pink_floyd_art_pop, pink_floyd_art_pop_new), axis=0)

# replace csv with new data
p.to_csv('pink_floyd_artist_popularity.csv', index=False)



# push csv files to GitHub repo
import subprocess

def add_and_push_csv_file(csv_file_path):

    # make sure this script is inside repo

    # Add the CSV file to the local repository
    subprocess.call(['git', 'add', csv_file_path])

    # Commit the changes
    subprocess.call(['git', 'commit', '-m', 'data update'])

    # Push the changes to the remote repository
    subprocess.call(['git', 'push', 'origin', 'main'])


add_and_push_csv_file("pink_floyd_tracks_updated.csv")
add_and_push_csv_file("pink_floyd_artist_popularity.csv")


