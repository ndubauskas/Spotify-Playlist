from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
CLIENT_ID = "CLIENT ID"
CLIENT_SECRET = "SECRET"
USERNAME = "USERNAME"
website_date = input("Type in a date YYYY-MM-DD: ")
#website_date = "1995-04-26"
playlist_name = f"{website_date}Playlist"
playlist_description = f"Top hits from {website_date}"
year = website_date.split("-")[0]
website = "https://www.billboard.com/charts/hot-100/" + website_date

response = requests.get(website)
website_text = response.text
soup = BeautifulSoup(website_text, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth
                        (client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri="http://example.com",
                        scope="playlist-modify-private",
                        show_dialog=True,
                         cache_path=".cache",
                         username= "USERNAME")
                     )
playlist = sp.user_playlist_create(sp.me()["id"], playlist_name, public=False, description=playlist_description)
playlist_id = playlist["id"]

user_id = sp.current_user()["id"]
for i in range(0,len(song_names)):
    results = sp.search(q=f"track:{song_names[i]} year:{year}", type="track")
    if results["tracks"]["items"]:

        track_url = results["tracks"]["items"][0]["uri"]
        sp.playlist_add_items(playlist_id, [track_url])
        print(f"Spotify URL for '{song_names[i]} {track_url}")
    else:
        print(f"No Spotify track found for '{song_names[i]}' ")



