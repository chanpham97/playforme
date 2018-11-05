import requests
import config

def get_playlist_duration(origin, dest, mode):
    modes = {"plane": 900, "car": 60}  # in kph
    stops = [origin, dest]
    stops_str = "|".join([x.replace(' ', '') for x in stops])
    res = requests.get('https://www.distance24.org/route.json', params={'stops':stops_str})
    time = 60*res.json()['distance']/modes[mode]
    return time

def get_songs_for(loc, count, token):
    payload={'q':'{} genre:{}'.format(loc, 'pop'), 'type':'track','limit':count}
    res = requests.get('https://api.spotify.com/v1/search', params=payload, headers={'Authorization':'Bearer {}'.format(token)})

    # song_names = [track['name'] for track in res.json()['tracks']['items']]
    song_ids = [track['id'] for track in res.json()['tracks']['items']]
    return song_ids


origin = 'New York'
dest = 'Los Angeles'
time = get_playlist_duration(origin, dest, 'plane')
res = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'client_credentials'}, auth=(config.spotify_client_id, config.spotify_client_secret))
token = res.json()['access_token']
count = time/3 if time/3 < 50 else 50
songs = get_songs_for(origin, count, token)
# get_songs_for('LA', count, token)
