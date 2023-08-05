# Import necessary modules and libraries
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# Load environment variables from .env file
load_dotenv()

# Import CLIENT_ID and CLIENT_SECRET from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Function to get Spotify API token using client credentials
def get_token():
    # Combine client_id and client_secret and encode in base64
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # API endpoint for token retrieval
    url = "https://accounts.spotify.com/api/token"

    # Headers for token request
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Data for token request
    data = {"grant_type": "client_credentials"}

    # Send a POST request to retrieve the token
    result = post(url, headers=headers, data=data)

    # Parse the JSON response to extract the access token
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Function to generate the authorization header with the provided token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Function to search for an artist by name
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    # Build the query URL and send a GET request to search for the artist
    query_url = url + query
    result = get(query_url, headers=headers)

    # Parse the JSON response to extract the artist information
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist found...")
        return None
    else:   
        return json_result[0]

# Function to get top tracks of an artist in a specific country
def get_songs_by_artist(token, artist_id, country):
    url =f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country}"
    headers =  get_auth_header(token)
    
    # Send a GET request to retrieve the artist's top tracks in the specified country
    result = get(url, headers=headers)
    
    # Parse the JSON response to extract the list of tracks
    json_result = json.loads(result.content)["tracks"]
    return json_result

# Get the API token
token = get_token()

# Search for an artist by name and get their ID
result = search_for_artist(token, "slowdive")
artist_id = result["id"]

# Get top tracks of the artist in different countries
songsTR = get_songs_by_artist(token, artist_id, "TR")
songsUS = get_songs_by_artist(token, artist_id, "US")

# Print the top tracks for each country
for idx, song in enumerate(songsTR):  
    print(f"{idx + 1}. {song['name']}")

print("\n")

for idx, song in enumerate(songsUS):  
    print(f"{idx + 1}. {song['name']}")