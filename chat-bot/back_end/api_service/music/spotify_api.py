
import sys
import spotipy
import json
import random
from spotipy import oauth2

# new version of getting token
# need to install spotipy with command: "pip3 install git+https://github.com/plamere/spotipy.git --upgrade"
# to get the latest version, otherwise some function will be missing.
CLIENTID = 'e7aa73aec5d24f48a00f6a4428e8cf94'
CLIENT_SECRET = '1a350fe2add24438b737dcf51c3a4a7c'

sp_oauth = oauth2.SpotifyClientCredentials(
    CLIENTID,
    CLIENT_SECRET)
token = sp_oauth.get_access_token()
sp = spotipy.Spotify(auth=token)


def refresh_sp():
    global sp
    new_token = sp_oauth.get_access_token()
    if new_token != token:
        sp = spotipy.Spotify(auth=newToken)


# get the basic jason file of the artist
def get_artist(name):
    refresh_sp()
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        #print('+++++++sp.search(name)+++++++',items[0])
        return items[0]
    else:
        return None


# random  get one or several recommended songs name and url by search artist[id]
#take in a request from the dialogflow and parse to take out the artist name parame and return a jason with recommened song
def show_recommendations_for_artist(name):
    refresh_sp()
    artist = get_artist(name)
    content = []
    results = sp.recommendations(seed_artists = [artist['id']])
    #print(results)
    for track in results['tracks']:
        # check if search the specific name of the artist by id
        if(artist['id'] == track['artists'][0]['id']):
            external_url = track['external_urls']['spotify'].replace('com', 'com/embed')
            #print(track['name'], '-', track['artists'][0]['name'])
            content.append({'name': track['name'], 'url': external_url, 'artist_name': track['artists'][0]['name']})
    #data = json.dumps({'type': 'track', 'contents': content})

    #select random song from content
    data = {'type': 'track', 'contents': random.choice(content)}

    #print(data)
    return data

# show all the albums of the artist
def show_artist_albums(name):
    refresh_sp()
    artist = get_artist(name)
    content = []
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    #print('+++++++results+++++++++',results)
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set()  # to avoid dups
    albums.sort(key=lambda album: album['name'].lower())
    #print('+++++albums+++++', albums)
    for album in albums:
        external_url = album['external_urls']['spotify'].replace('com', 'com/embed')
        content.append({'name': album['name'], 'url': external_url, 'artist_name': album['artists'][0]['name']})
        name = album['name']
        if name not in seen:
            #print((' ' + name))
            seen.add(name)
    #random choose one of the album in conent
    data = {'type': 'album', 'contents': random.choice(content)}
    #print(data)
    return data

def get_artist_albums(artist_name, album_name):
    refresh_sp()
    if artist_name == None:
        request_album(album_name)
    else:
        artist = get_artist(artist_name)
        content = []
        albums = []
        results = sp.artist_albums(artist['id'], album_type='album')
        #print('+++++++results+++++++++',results)
        albums.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])
        seen = set()  # to avoid dups
        albums.sort(key=lambda album: album['name'].lower())
        #print('+++++albums+++++', albums)
        for album in albums:
            if album['name'] == album_name:
                external_url = album['external_urls']['spotify'].replace('com', 'com/embed')
                content.append({'name': album['name'], 'url': external_url, 'artist_name': album['artists'][0]['name']})
                name = album['name']
            if name not in seen:
                #print((' ' + name))
                seen.add(name)
            data = {'type': 'album', 'contents': content}
            #print(data)
            return data

#given song name return artist name,url,album
def request_song(track):
    refresh_sp()
    content = []
    results = sp.search(q='track:' + track, type='track')
    items = results['tracks']['items']
    # data = items[0]['artists'][0]['external_urls']['spotify']
    # print(items[1]['external_urls']['spotify'])
    # 'url': items[0]['artists'][0]['external_urls']['spotify']
    content.append({'name': items[1]['name'], 'url': items[1]['external_urls']['spotify'].replace('com', 'com/embed'),
                    'artist_name': items[1]['artists'][0]['name']})
    data = {'type': 'track', 'contents': content[0]}
    return data

def request_album(album):
    refresh_sp()
    content = []
    results = sp.search(q='album:' + album, type='track')
    items = results['tracks']['items']
    # print(items[0])
    data = items[0]['artists'][0]['external_urls']['spotify']
    external_url = items[0]["album"]['external_urls']['spotify'].replace('com', 'com/embed')
    content.append({'name': items[0]['album']['name'], 'url': external_url,
                    'artist_name': items[0]['artists'][0]['name']})
    data = {'type': 'album', 'contents': random.choice(content)}
    return data

if __name__ == '__main__':
    # test 1
    #request_song('Dangerous')
    name = 'michael jackson'
    print(request_song("let it go"))
    #print(request_album("Eat a Peach"))
    

    #print(show_recommendations_for_artist(name))
    #if name:
        # test2
    #print(show_artist_albums(name))
        # test3
    #print(show_recommendations_for_artist(name))
    #else:
    #    print("Can't find that artist")
