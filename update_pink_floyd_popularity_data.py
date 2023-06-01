import pandas as pd
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

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
df['track_popularity'] = [sp.track(track_id)['popularity'] for track_id in df['track_id']]

# get current album popularity in a dictionary
alb_pop = {alb_id: sp.album(alb_id)['popularity'] for alb_id in df['album_id'].unique()}

# make a DataFrame with album_id and populariy
alb_pop_df = pd.DataFrame(data={'album_id': alb_pop.keys(),
                               'album_popularity': alb_pop.values()})   

# merge to pass album popularity information
df = pd.merge(df, alb_pop_df, on='album_id')

# check number of tracks and save to csv
tot_tracks = sum(album_num_tracks.values())
if tot_tracks == df.shape[0]:
    df.to_csv('pink_floyd_tracks_updated.csv', index=False)
else:
    raise Exception('Error! Unable to collect the correct number of tracks')


# get current Pink Floyd popularity
pink_floyd_popularity = sp.artist(df['artist_id'][0])['popularity']
# read popularity by date csv
pink_floyd_art_pop = pd.read_csv('pink_floyd_artist_popularity.csv')
current_date = date.today()
pop_dict = {'date': [current_date],
          'artist_popularity': [pink_floyd_popularity]}+
# make new df
pink_floyd_art_pop_new = pd.DataFrame(pop_dict)
# concat old and new 
p = pd.concat((pink_floyd_art_pop, pink_floyd_art_pop_new), axis=0)
# replace csv with new data
p.to_csv('pink_floyd_artist_popularity.csv', index=False)


