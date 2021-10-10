import requests
import json
from json.decoder import JSONDecodeError

stop = "0"

while stop == "0":
    # My client info
    CLIENT_ID = input("Type your client_id here: ")
    CLIENT_SECRET = input("Type your client_secret here: ")

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # The token request and validation
    try:
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']

        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        # base URL of all Spotify API endpoints
        BASE_URL = 'https://api.spotify.com/v1/search?'

        # Welcome message
        print()
        print("===SPOTIFY API===")
        print("===Welcome to the search an artist function of Yari Van Doninck!===")

        while True:
            
            print()
            print("To search for an artist - Press 1")
            print("To exit this program - Press 0")
            print()
            choice_of_user = input("What do you choose? -  ")

            # Code if choice was 0 - Stop the program
            if choice_of_user == "0":
                print("You ended the program...")
                break

            if choice_of_user != "0" and choice_of_user != "1":
                print("===You didn't type any of the available options try again.===")   

            # Code if choice was 1 - Search for an artist
            if choice_of_user == "1":
                print()
                artist= input("Which artist do you want to search? - ")
                print()
                
                # Error handling if artists can't be found
                try:

                    # actual GET request with proper header
                    r = requests.get(BASE_URL + 'q=' + artist + '&type=artist&market=US&limit=1', headers=headers)
                    r = r.json()

                    # get the genre, followers and popularity data of the artist
                    genre = r['artists']['items'][0]['genres']
                    genre_to_string = ", ".join(genre)
                    popularity = r['artists']['items'][0]['popularity']
                    followers = r['artists']['items'][0]['followers']['total']

                    # get the id to use in the next get request
                    artist_id = r['artists']['items'][0]['id']
                    url = 'https://api.spotify.com/v1/'

                    # pull all artists albums
                    r = requests.get(url + 'artists/' + artist_id + '/albums', headers=headers, params={'include_groups': 'album', 'limit': 50})
                    d = r.json()

                    # Get name of the artist
                    chosen_artist = d['items'][0]['artists'][0]['name']

                    # print name & genre of the artist
                    print(chosen_artist, " - Genres:", genre_to_string)
                    print("Popularity (rank): -", popularity)
                    print("Amount of followers: -", followers)
                    print()
                    print("All albums of", chosen_artist + ":")
                    print()

                    # Get and print all albums of the artist
                    albums = [] # to keep track of duplicates
                    an = 'album'
                    t = 'release datum'
                    print("{:40} {:20}".format(an, t))

                    # loop over albums
                    for album in d['items']:
                        album_name = album['name']
                        album_date = album['release_date']

                        # skip over albums we've already grabbed
                        trim_name = album_name.split('(')[0].strip()
                        if trim_name.upper() in albums:
                            continue
                        albums.append(trim_name.upper())
                        print("{:40} {:20}".format(trim_name.upper(), album_date))

                except:    
                    print("===Artist cannot be found, check for spelling errors or try another artist.===")

        # Help to stop the program
        stop = "1"

    except:
        print("authentication failed, check client_id & client_secret")   