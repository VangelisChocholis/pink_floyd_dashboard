import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('pink_floyd_tracks_updated.csv', parse_dates=[5])

# sort the name of the song (What is this?!):
# Several Species of Small Furry Animals Gathered Together in a Cave and Grooving with a Pict 
df.loc[df['track_id']=='63M8OHzd0lcVT517Pnon81', 'track_name'] = 'Several Speacies of Small Furry Animals...'

df = df.sort_values(by='track_popularity', ascending=True)


albums = (df
           .groupby(by=['release_date', 'album_name'])['album_popularity']
           .mean()
           .reset_index()
           .sort_values(by='release_date', ascending=True)
             )


#dropdown_cols = df.loc[:, [ 'track_popularity', 'valence', 'energy', 'danceability']].columns
dropdown_cols = [col.replace('_', ' ') for col in df.loc[:, ['track_popularity', 'valence', 'energy', 'danceability']].columns]




def plot_tracks():
    # make Pink Floyd tracks vs Popoularity

    # make x-axis dropdown menu
    column_selector = st.selectbox('Select x-axis', dropdown_cols, key=1, index=1) # set valence as default y-axis

    # df to plot
    if column_selector == 'track popularity':
        column_selector = 'track_popularity'
    df_chart = df.sort_values(by=column_selector, ascending=True)

    # make bar chart 
    fig = px.bar(df_chart, x=column_selector, y='track_name')

    # remove underscore again
    if column_selector == 'track_popularity':
        column_selector = 'track popularity'

    fig.update_layout(title=f'Pink Floyd tracks by {column_selector}')

    # update y-axis tick font size
    fig.update_layout(
        yaxis=dict(
            tickfont=dict(size=12)        
        )
    )
    fig.update_yaxes(title_text='')
    # set x-axis label
    fig.update_xaxes(title_text=column_selector)
    # set axis on top and adjust chart size
    fig.update_layout(xaxis_side='top')
    fig.update_layout(width=900, height=2200)

    return fig



def plot_tracks_album():
    
    # plot tracks for each album
    # make Album dropdown menu
    album_list = df.sort_values(by='release_date')['album_name'].unique() # display chronologically
    album_selector = st.selectbox('Select Album', album_list, key=2, index=10) # set The Wall as deafault Album

    # make y axis dropdown menu
    column_selector = st.selectbox('Select y-axis', dropdown_cols, index=1)  # set valence as default y-axis

    # we plot df_chart
    if column_selector == 'track popularity':
        column_selector = 'track_popularity'
    df_chart = df[df['album_name']==album_selector].sort_values(by=column_selector, ascending=False)
    
    # add description 
    st.write(descr_dict[column_selector])
         
    fig = px.bar(df_chart, x='track_name', y=column_selector)

    fig.update_layout(
        xaxis_title='Album',
        yaxis_title=column_selector,
        title='',
        height=600,
        width=900,
    )
    # adjust font size, use -45 degres label rotation
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_layout(xaxis_tickangle=-45)

    return fig


def plot_album_date():
    # making bar chart for album popularity vs releash date
    # perform groupby to get data
    
    # make chart
    fig = px.bar(albums, x='release_date', y='album_popularity',
                   color='album_name', color_discrete_sequence=px.colors.qualitative.Alphabet)
    # adjust chart
    fig.update_layout(
        xaxis_title='Release Date',
        yaxis_title='Album Popularity',
        title='Album Popularity by Release Date',
        height=600,
        width=900,
    )


    fig.update_xaxes(range=[albums['release_date'].min() - pd.DateOffset(years=2)
                            , albums['release_date'].max() + pd.DateOffset(years=2)]
                    )

    return fig


def plot_albums_popularity():
    # make albums by popularity
    albs = albums.sort_values(by='album_popularity', ascending=False)

    fig = px.bar(albs, x='album_name', y='album_popularity')

    fig.update_layout(
        xaxis_title='Album',
        yaxis_title='',
        title='Album Popularity (0 - 100)',
        height=600,
        width=900,
    )
    # adjust font size, use -45 degres label rotation
    fig.update_xaxes(tickfont=dict(size=15))
    fig.update_layout(xaxis_tickangle=-45)
    return fig
    


#st.write(plot_tracks())
#st.write(plot_tracks_album())
#st.write(plot_album_date())
#st.write(plot_albums_popularity())

#menu = ["Pink Floyd Tracks", "Tracks per Album", "Album Release Date", "Album Popularity"]  # List of graph names

# make a menu for the sidebar, each string maps to a plot function
menu = {
    'Tracks per Album': plot_tracks_album,
    'Album Popularity': plot_albums_popularity,
    'Pink Floyd Tracks': plot_tracks, #'Popularity by Release Date': plot_album_date,
    }

# sidebar to select graph
selection = st.sidebar.selectbox('Select a graph', menu.keys())

st.subheader(selection)
# write corresonding plot 
st.write(menu[selection]())
