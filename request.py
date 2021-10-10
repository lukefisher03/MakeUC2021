import json
from json.decoder import JSONDecodeError
from typing import final
import requests
import sys 
import pandas as pd
import csv

CLIENT_ID = "83ae548c8bdb40a9a65a4b6e2a174bd6"
CLIENT_SECRET = "9961fe6a1fe94d11a256d13a65b44efb"


AUTH_URL = 'https://accounts.spotify.com/api/token'
base_url = "https://api.spotify.com/v1/"

playlists = [
    "59ZbFPES4DQwEjBpWHzrtC"
]
final_playlist = []
songs_count = 0
playlists_count = 0

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
auth_response_data = auth_response.json()
access_token = auth_response_data["access_token"]

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

if auth_response.status_code == 200:
    print("Request went through")
else:
    print("Request did not go through")

final_attributes = []

for playlist in playlists:
    try: 
        playlist = requests.get(base_url+"playlists/"+playlist, headers=headers)
        spotify_playlist_output = playlist.json()

        items = spotify_playlist_output["tracks"]["items"]
        items_array = []
        for item in items:
            id = (item["track"]["id"])
            items_array.append(id)
        #print(items_array)

        song_attr = []

        for array_item in items_array:
            try:
                song_attributes = requests.get(base_url+"audio-features/"+array_item, headers=headers)
                json_attr = song_attributes.json()
                is_retro = False
                if(retro_setting == str(1)):
                    is_retro = True
                else: 
                    is_retro = False
                
                song = [
                    json_attr["danceability"],
                    json_attr["energy"],
                    json_attr["key"],
                    json_attr["loudness"],
                    json_attr["speechiness"],
                    json_attr["acousticness"],
                    json_attr["instrumentalness"],
                    json_attr["liveness"],
                    json_attr["valence"],
                    json_attr["tempo"],
                    json_attr["time_signature"],
                    # is_retro
                ]

                final_attributes.append(song)
                songs_count += 1
                print("finished song #" + str(songs_count) + " | " +str(song))
            except KeyError:
                print("ERROR on song #" + str(songs_count))
        playlists_count += 1
        print('Finished processing playlist #' + str(playlists_count))
    except KeyError and TypeError:
        print("ERROR on Playlist #" + str(playlists_count))
with open("songs.csv", 'w') as csvfile: 
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["danceability","energy","key","loudness","speechiness","acousticness","instrumentalness","liveness","valence","tempo","time_signature","retro"])
    for song in final_attributes:
        csvwriter.writerow(song) 
    csvfile.close() 



    # csvfile=open("songs_count.csv","w", newline="")
    # obj = csv.writer(csvfile)
    # for song in final_attributes:
    #     obj.writerow(song)
    # csvfile.close()




    # with open('./songs_count.csv') as csv_file:
    #     csv_writer = csv.writer(csv_file, delimiter=' ')
    #     for song in final_attributes:
    #         csv_writer.writerow(pd.read_json(json.dumps(song)).to_csv())

#print(json.dumps(final_attributes))

# df = pd.read_json(json.dumps(final_attributes))
# print(df.to_csv())
