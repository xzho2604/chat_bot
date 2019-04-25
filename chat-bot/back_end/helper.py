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
    try:
        result = show_recommendations_for_artist(artist)
    except:
        result = "500" # 500 indicate expetion for token expire
    return result 

def artist_album(param):
    artist = param["music-artist"]
    try:
        result = show_artist_albums(artist)
    except:
        result = "500"

    return result  

def play_song(param):
    song = param["song"]
    print("the song is :",song)
    try:
        result = request_song(song)
    except:
        result = "500"
    return result  

def play_album(param):
    album = param["music-album"]

    try:
        result = request_album(album)
    except:
        result = "500"
    return result  


