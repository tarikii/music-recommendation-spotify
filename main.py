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


def get_characteristics_track(token, track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)

    response = get(url, headers=headers)

    if response.status_code == 200:
        track_info = response.json()

        return track_info
    else:
        # Print the error response content
        print(f"Error: {response.status_code}")
        return None


def main():
    token = get_token()
    track_url = "https://open.spotify.com/track/4a2IfhPphh7KglUT8r4FTL?si=185818e201b44544"
    track_id = get_track_id(track_url)


    #characteristics_track = get_characteristics_track(token, "1e9XBW7dBqZeHVYMFI9oHN?si=c659d5b4c5314020")


if __name__ == "__main__":
    main()