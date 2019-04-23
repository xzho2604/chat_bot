from api_service.weather.weather_api import *
from api_service.music.spotify_api import *


#
#---------------------------------------------
#weather
# return {time,city,title,weather}
def process_weather(param):
    city = param["address"]["city"]
    when = param["date-time"] #string of:"2019-04-24T12:00:00+10:00"
    when = when[:10]
    weather = get_forecast(city,when)

    return {"city":city,"weather":weather,"time":when,"temp":20} 

#---------------------------------------------
#music
def artist_song(param):
    artist = param["music-artist"][0]
    return show_recommendations_for_artist(artist)

def artist_album(param):
    artist = param["music-artist"]
    return show_artist_albums(artist)

def play_song(param):
    song = param["song"]
    return request_song(song)

def play_album(param):
    album = param["music-album"]
    return request_album(album)


