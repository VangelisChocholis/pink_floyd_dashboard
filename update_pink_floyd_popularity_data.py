import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# read Pink Floyd data 
# check get_pink_floyd_data_to_csv.py to see how we got them from a databse
df = pd.read_csv('pink_floyd_tracks.csv')

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

# make sure to drop duplicates
df = df[~df['track_id'].duplicated()]

# remove remastered versions
df = df[~df['track_name'].str.contains('remaster', case=False)]

# remove live versions
df = df[~df['track_name'].str.contains('- live', case=False)]

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

# get current Pink Floyd popularity
pink_floyd_popularity = sp.artist(df['artist_id'][0])['popularity']
#print(f'Current Pink Floyd popularity: {pink_floyd_popularity}')

# check number of tracks and save to csv
tot_tracks = sum(album_num_tracks.values())
if tot_tracks == df.shape[0]:
    print('Great! We have collected all the tracks')
    df.to_csv('pink_floyd_tracks_updated.csv', index=False)
else:
    print('Error! Unable to collect the correct number of tracks')

    

