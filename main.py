from dotenv import load_dotenv
import os
import base64
from requests import post, get, exceptions
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def show_menu():
    print("WELCOME TO SPOTIFY SEARCH MUSIC!")
    print()
    print()
    print("1. Search for an artist")
    print("2. Show top tracks of an artist")
    print("3. Get characteristics of a track")
    print("4. Search for the tracks of a playlist")
    print("0. Exit")
    print()
    return int(input("Choose your option: "))

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


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"

    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)

    try:
        result.raise_for_status()
        json_result = result.json()["artists"]["items"]

        if len(json_result) == 0:
            print()
            print(f"No artist found with the name: {artist_name}")
            print()
            return None

        return json_result[0]
    except exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return None
    except exceptions.RequestException as err:
        print(f"Error during the request: {err}")
        return None
    except ValueError as ve:
        print(f"Error parsing JSON response: {ve}")
        return None



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
    

def get_playlist_tracks_names(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    if "name" in json_result:
        playlist_name = json_result['name']
    else:
        print("Error: 'name' not found in the API response.")
        return None, None

    if "tracks" in json_result:
        tracks_info = json_result['tracks']['items']
        track_names = [track['track']['name'] for track in tracks_info]
        return playlist_name, track_names
    else:
        print("Error: 'tracks' not found in the API response.")
        return None, None


def main():
    token = get_token()
    track_url = "https://open.spotify.com/track/0Y2i84QWPFiFHQfEQDgHya?si=7918f849eee04290"
    track_id = get_track_id(track_url)
    desired_keys = ["danceability", "energy", "loudness", "tempo", "valence", "speechiness"]
    #artist = search_for_artist(token, "Leviathan")
    #artist_id = artist["id"]
    #songs = get_artist_songs(token, artist_id)

    while True:
        try:
            option = show_menu()

            if option == 1:
                try:
                    artist_name = input("Name of the artist: ")
                    artist = search_for_artist(token, artist_name)

                    if artist:
                        print(f"Artist found: {artist['name']} (Followers: {artist['followers']['total']})")
                except ValueError:
                    print()
                    print("Invalid Input!")
                    print()

            
            elif option == 2:
                try:

                    artist_name = input("Name of the artist: ")
                    artist = search_for_artist(token, artist_name)
                    artist_id = artist["id"]
                    top_songs = get_artist_songs(token, artist_id)

                    for idx, song in enumerate(top_songs):
                        print((idx + 1), song["name"])
                
                except TypeError:
                    pass
                
            
            elif option == 3:
                try:

                    track_url = input("Paste here the track URL of Spotify: ")
                    track_id = get_track_id(track_url)

                    track_info = get_characteristics_track(token, track_id, desired_keys)

                    for idx, info in track_info.items():
                        print((idx + 1), info)
                
                except IndexError:
                    print()
                    print("Not a valid URL!")
                    print()

                except ValueError:
                    print()
                    print("Not a valid URL!")
                    print()
            

            elif option == 4:
                try:

                    playlist_url = input("Paste here the URL of the Spotify playlist: ")
                    playlist_id = get_track_id(playlist_url)
                    playlist_name, track_names = get_playlist_tracks_names(token, playlist_id)

                    if track_names:
                        print(f"Tracks in the playlist '{playlist_name}':")
                        for idx, track_name in enumerate(track_names):
                            print(f"{idx + 1}. {track_name}")
                    else:
                        print("Failed to retrieve playlist track names.")
                except IndexError:
                    print()
                    print("Not a valid URL!")
                    print()
                
                except ValueError:
                    print()
                    print("Not a valid URL!")
                    print()
            
            elif option == 0:
                return False
            

            else:
                print()
                print("Invalid option! Pick between the numbers 0-4")
            
        except ValueError:
            print()
            print("Provide a number, not a string!")
            print()

if __name__ == "__main__":
    main()
