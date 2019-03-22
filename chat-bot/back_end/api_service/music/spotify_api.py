
import sys
import spotipy
import json

''' main function to call the spotify api

    last updated time :
    21/03/2019
'''

def  get_access_token(filename):
    file = open(filename)
    try:
        token = file.read()
    finally:
        file.close()
    return token

# get the basic jason file of the artist
def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        #print('+++++++sp.search(name)+++++++',items[0])
        return items[0]
    else:
        return None

# random  get one or several recommended songs name and url by search artist[id]
def show_recommendations_for_artist(name):
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
    data = json.dumps({'type': 'track', 'contents': content})
    print(data)
    return data

# show all the albums of the artist
def show_artist_albums(name):
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
    data = json.dumps({'type': 'album', 'contents': content})
    print(data)
    return data

def request_song(track):
    content = []
    results = sp.search(q='track:' + track, type='track')
    items = results['tracks']['items']
    data = items[0]['artists'][0]['external_urls']['spotify']
    print(items[0]['artists'][0]['name'])
    content.append({'name': items[0]['name'], 'url': items[0]['artists'][0]['external_urls']['spotify'],
                    'artist_name': items[0]['artists'][0]['name']})
    data = json.dumps({'type': 'track', 'contents': content})
    print(data)


if __name__ == '__main__':

    filename = './web-api-auth/authorization_code/auth_token.txt'
    token = get_access_token(filename)
    sp = spotipy.Spotify(auth = token)

    # test 1
    request_song('Dangerous')

    name = 'michael jackson'
    if name:
        # test2
        show_artist_albums(name)
        # test3
        show_recommendations_for_artist(name)
    else:
        print("Can't find that artist")
