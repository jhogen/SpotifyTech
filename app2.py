#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.graph_objects as pgo
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import spotipy
sp = spotipy.Spotify()

from spotipy.oauth2 import SpotifyClientCredentials 

import json
from pandas.io.json import json_normalize
import pandas as pd


# In[2]:


#Authenticatiie van de API zonder gebruiker.
client_credentials_manager = SpotifyClientCredentials(client_id='ee5d014280cf4dad8350e8a0b35608b0', client_secret="f3556b9ac996464a84e686586c3e9642")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# In[13]:


#De playlist die opgehaald wordt, de URI van de playlist en de URI van de nummers.
playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]


# In[4]:


#Het weergeven van de data en de kolommen, alle variabelen aanmaken 
data = {'track_uri': [],
        'track_name': [],
        'artist_uri': [],
        'artist_info': [],
        'artist_name': [],
        'artist_pop': [],
        'artist_genres': [],
        'album': [],
        'track_pop': [],
       }
for track in sp.playlist_tracks(playlist_URI)["items"]:
    #URI
    track_uri = track["track"]["uri"]
    
    #Track name
    track_name = track["track"]["name"]
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)
    
    #Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]
    
    #Album
    album = track["track"]["album"]["name"]
    
    #Popularity of the track
    track_pop = track["track"]["popularity"]
    
    data['track_uri'].append(track_uri)
    data['track_name'].append(track_name)
    data['artist_uri'].append(artist_uri)
    data['artist_info'].append(artist_info)
    data['artist_name'].append(artist_name)
    data['artist_pop'].append(artist_pop)
    data['artist_genres'].append(artist_genres)
    data['album'].append(album)
    data['track_pop'].append(track_pop)
    
    
df = pd.DataFrame.from_dict(data)


# In[5]:


#Titel van het tabblad aanmaken en de layout van het blog.
st.set_page_config(page_title="Dashboard Groep 23", page_icon="♫", layout = "wide", initial_sidebar_state="expanded")


# In[14]:


#Titel van elke pagina aanmaken.
st.title('Tech Report / Blog - Spotify API')


# In[7]:


#Het toevoegen van een sidebar.
st.sidebar.title('Navigatie')


# In[9]:


#In deze grafiek is te zien hoe populair een bepaald nummer is in de afspeellijst. Ook is te zien hoe populair de artiest van dat nummer is.
#Er kan geschakeld worden tussen een 'bar' en een 'scatter' plot.
#Bij de barplot komen sommige nummers op elkaar te staan. Dit komt hoofdzakelijk door dat deze nummers door dezelfde artiest zijn gemaakt. De artiest is namelijk net zo populair als zichzelf.


fig2 = px.scatter(x=df["track_pop"], y=df["artist_pop"], color=df["track_pop"], text=df["track_name"], title="Top 50 nummers van de wereld")

my_buttons = [  {'label': "Bar Plot", 'method': "update", 'args': [{"type": "bar"}]},
                {'label': "Scatter Plot", 'method': "update", 'args': [{"type": "scatter"}]}]

fig2.update_traces(textposition='top center')
fig2.update_layout(uniformtext_mode="hide", 
                  width=800, height=800)

fig2.update_layout({
    'updatemenus': [{
      'type': "buttons",'direction': 'down',
      'x': 1.4,'y': 0.5,
      'showactive': True,'active': 0,
      'buttons': my_buttons}]},
       xaxis_title = 'Populariteit van het nummer',
       yaxis_title = 'Populariteit van de artiest')


# In[44]:


#Het aanmaken van de tabel die alle nummers, albums en de populariteit van de nummers van een artiest laat zien.
table_df = df[["track_name", "album", "track_pop"]].copy()

fig3 = pgo.Figure(pgo.Table(header={"values": ["track_name", "album","track_pop"], "fill": dict(color='grey')}, cells={"values": [["track_name", "album", "track_pop"]], "fill": dict(color='black')}))


fig3.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "label": artist,
                    "method": "update",
                    "args": [
                        {
                            "cells": {
                                "fill": dict(color='black'), "values":  table_df.loc[df["artist_name"].eq(artist)].T.values
                            }
                        }
                    ],
                }
                for artist in df["artist_name"].unique().tolist()
            ]
        }
    ]
)


# In[11]:


#Weergeven data
df_describe = df.describe()


# In[21]:


#De gehele opbouw van de streamlit app!:
pages = st.sidebar.radio('paginas',options=['Home','API Dataset', 'Plot van Populariteit', 'Artiesten Info', 'Slider Artiest & Album'], label_visibility='hidden')

if pages == 'Home':
    st.subheader("SPOTIFY API - GROEP 22")
    st.markdown("Data Science 2022 - HvA - Osman, Thomas, Floris & Jakob")
elif pages == 'API Dataset':
    st.subheader('Dataset Global Top 50 Songs')
    st.markdown("Onze data is opgehaald vanuit de Spotify API. Hiervoor hebben wij eerst het spotipy pakket geïnstalleerd en geïmporteerd. Om de data op te kunnen halen hebben wij een client ID en een client secret nodig, hiervoor hebben wij dus ook een account aan moeten maken bij de Spotify developer pagina. De authenticatie is na het aanmaken van een app bij Spotify compleet en nu kunnen wij een dataset kiezen: de globale top 50 top nummers. Uit deze dataset hebben wij alle info gehaald, zoals de track_uri, de track popularity en de artiestennamen, om er een paar te noemen. Hierna hebben wij de append tool gebruikt en is de data omgezet in een dataframe. De data is klaar om bewerkt te worden!")
    st.markdown("Hieronder wordt de door ons gekozen dataset weergegeven: https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f")
    st.dataframe(data=df, use_container_width=False)
    st.subheader('Mogelijke kwaliteitsissues')
    st.markdown("Wij zijn erg tevreden met de dataset, er staat veel informatie in, hij wordt automatisch dagelijks geupdated. Er is wel één mogelijk kwaliteitsprobleem in de vorm van missende waardes. Een paar nummers in de dataset hebben namelijk geen waarde binnen de genre kolom. Dus als je wilt selecteren op basis van de genres van de nummers, dan kunnen een aantal nummers buiten de selectie vallen.")
    st.subheader('Hier kan je de dataframe weergegeven zien met de describe() functie.')
    st.dataframe(data=df_describe, use_container_width=False)
    st.markdown("Bron: Spotify API")
elif pages == 'Plot van Populariteit':
        st.subheader('Bekijk de verhouding tussen de populariteit van het nummer van de artiest')
        st.markdown("In deze grafiek is te zien hoe populair een bepaald nummer is binnen de afspeellijst. Ook is te zien hoe populair de artiest van dat nummer op het moment is. Er kan geschakeld worden tussen een 'bar' en een 'scatter' plot. Bij de barplot komen sommige nummers op elkaar te staan. Dit komt hoofdzakelijk doordat deze nummers door dezelfde artiest zijn gemaakt. De artiest is namelijk net zo populair als zichzelf.")
        st.plotly_chart(fig2)
elif pages == 'Artiesten Info':
        st.subheader('Bekijk de populariteit van het top 50 nummer en het bijbehorende album van je favoriete artiest')
        st.markdown("Klik op één van de artiesten die een nummer hebben in de wereldwijde top 50 nummers! Hiermee kan je zien welk nummer van hen in de top 50 staat, uit welk album dit nummer komt en hoe populair het nummer is!")
        st.plotly_chart(fig3)
elif pages == 'Slider Artiest & Album':
        st.subheader('Bekijk je favoriete artiest en album')
        st.markdown("Speel met de slider en kies je favoriete artiest en je favoriete album!")
        artist = st.select_slider(
        'Selecteer een artiest',
        options= ['BLACKPINK','Bizarrap','Harry Styles','David Guetta','Manuel Turizo','Bad Bunny','OneRepublic','ROSALÍA','Chris Brown','Steve Lacy','Nicki Minaj','Joji','Rosa Linn','Glass Animals','Kate Bush','Tom Odell','The Neighbourhood','Central Cee','The Kid LAROI','Stephen Sanchez','KAROL G','Charlie Puth','The Weeknd','d4vd','Nicky Youre','Post Malone','Elton John','Imagine Dragons','Luar La L','Lizzo','Ghost','KAROL G','Rauw Alejandro','Rema','James Hype'])
        st.write('Mijn favoriete artiest is', artist)
        album = st.select_slider(
        'Selecteer een album',
        options= ['BORN PINK','Quevedo: Bzrp Music Sessions, Vol. 52','Harrys House','Im Good (Blue)','La Bachata','Un Verano Sin Ti','I Ain’t Worried','MOTOMAMI','Indigo','Gemini Rights','Queen Radio: Volume 1','Glimpse of Us','SNAP PACK','Dreamland','Hounds Of Love','Long Way Down','I Love You.','Doja','F*CK LOVE 3: OVER YOU','Easy On My Eyes','PROVENZA','Left and Right (Feat. Jung Kook of BTS)','Starboy','Romantic Homicide','Sunroof','Twelve Carat Toothache','The Lockdown Sessions','Mercury - Acts 1 & 2','L3tra','Special','MESSAGE FROM THE CLERGY]','GATÚBELA','LOKERA','Calm Down (with Selena Gomez)','Ferrari','The Lockdown Sessions'])
        st.write('Mijn favoriete album is', album)

