from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data =  {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_track_id(track):
    track_id = track.split("/")
    return track_id[4]


def get_characteristics_track(token, track_id, keys):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)

    response = get(url, headers=headers)

    

    if response.status_code == 200:
        track_info = response.json()
        important_keys = {}

        for key in keys:
            if key in track_info:
                important_keys[key] = track_info[key]
        
        return important_keys
    else:
        # Print the error response content
        print(f"Error: {response.status_code}")
        return None


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"

    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("There is not an artist with this name on Spotify :(")
        return None
    
    return json_result[0]


def get_artist_songs(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    if "tracks" in json_result:
        return json_result["tracks"]
    else:
        print("Error: 'tracks' not found in the API response.")
        return None



def main():
    token = get_token()
    track_url = "https://open.spotify.com/track/0Y2i84QWPFiFHQfEQDgHya?si=7918f849eee04290"
    track_id = get_track_id(track_url)
    desired_keys = ["danceability", "energy", "loudness", "tempo", "valence", "speechiness"]
    artist = search_for_artist(token, "Leviathan")
    artist_id = artist["id"]
    songs = get_artist_songs(token, artist_id)

    #for idx, song in enumerate(songs):
        #print((idx + 1), song["name"])

    track_info = get_characteristics_track(token, track_id, desired_keys)

if __name__ == "__main__":
    main()
