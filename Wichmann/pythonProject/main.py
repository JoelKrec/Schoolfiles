import requests as r
from rich.console import Console
from rich.table import Table
from curtsies import Input
import base64
import json
import time
import os

console = Console()
clientId = "9ccea7a811194571b834ec6571f4c51f"
clientSecret = "eece1e728d8e48109c870f10751c48cd"
keyUp = 'KEY_UP'
keyDown = 'KEY_DOWN'


def base64_encode_str(unencoded_string):
    unencoded_string_bytes = unencoded_string.encode('ascii')
    base64_encoded_bytes = base64.b64encode(unencoded_string_bytes)
    return base64_encoded_bytes.decode('ascii')


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


# ggf. hinterlegtes Token holen, Gültigkeit überprüfen, sonst neues generieren
def get_token():
    # Prüfen, ob Datei mit Access-Token existiert, wenn nicht, lege sie an
    if os.path.isfile("access_token.json") is False:
        f = open("access_token.json", "x")

    f = open("access_token.json", "r")
    f_content = f.read()
    f.close()

    if len(f_content) == 0:
        return generate_token()
    else:
        # JSON-Validitätscheck
        if not is_json(f_content):
            return generate_token()

        f_content = json.loads(f_content)
        token = f_content['token']

        # Token-Validitätscheck
        if f_content['expires'] > int(time.time()):
            return token
        else:
            return generate_token()


def generate_token():
    # Autorisierungsparameter setzen
    client_id = '9ccea7a811194571b834ec6571f4c51f'
    client_secret = 'eece1e728d8e48109c870f10751c48cd'
    auth_string = base64_encode_str(f'{client_id}:{client_secret}')
    headers = {'Authorization': f'Basic {auth_string}'}
    body = {'grant_type': 'client_credentials'}

    # Token generieren
    token = r.post(f'https://accounts.spotify.com/api/token', headers=headers, data=body).json()

    # Token speichern
    f = open("access_token.json", "w")
    json_string = json.dumps({
        "token": token['access_token'],
        "expires": token['expires_in'] + int(time.time())
    })
    f.write(json_string)
    f.close()

    return token['access_token']

def getAuthHeader():
    return {'Authorization': f'Bearer {get_token()}'}


def createArtistUrl(search):
    return "https://api.spotify.com/v1/search?type=artist&q=" + str(search)


def createAlbumUrl(artistId):
    return "https://api.spotify.com/v1/artists/" + str(artistId) + "/albums"


def createGetAlbumTracksUrl(albumId):
    return "https://api.spotify.com/v1/albums/" + str(albumId)


def createGetTrackInfoUrl(trackId):
    return "https://api.spotify.com/v1/tracks/" + str(trackId)


def spotifyGet(url):
    return r.get(url, headers=getAuthHeader())


def clearStyleTags(inputs):
    result = []
    for i in inputs:
        i = i.replace('[red]', '')
        i = i.replace('[/]', '')
        result.append(i)
    return result


def getUserInput(header, options):
    y = 0
    maxY = len(options)

    while True:
        console.clear()
        table = Table(show_header=True, header_style="bold magenta")
        for head in header:
            table.add_column(head)

        results = []
        i = 0
        for option in options:
            if len(header) != len(options[0]):
                continue
            # option = clearStyleTags(option)
            if y == i:
                style = "red"
            else:
                style = "white"

            convertedOption = []
            for element in option:
                if type(element) == list:
                    temp = ""
                    for subElement in element:
                        temp = subElement + ", " + temp
                    element = temp
                else:
                    element = str(element)
                convertedOption.append(element)

            results.append(convertedOption)
            table.add_row(*convertedOption, style=style)

            i = i + 1
        console.print(table)

        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                if e == keyUp:
                    y = y - 1
                    if y < 0:
                        y = maxY - 1
                    break
                elif e == keyDown:
                    y = y + 1
                    if y >= maxY:
                        y = 0
                    break
                elif e == '\n':
                    return results[y].copy()
                elif e == "":
                    return ["Back"]


console.clear()
while True:
    console.print("Please enter an artist to search for: ")
    artistSearch = input()

    getResults = []

    artistsResult = spotifyGet(createArtistUrl(artistSearch))
    artists = []
    for artist in artistsResult.json()['artists']['items']:
        artists.append([artist['name'], artist['genres'], artist['id']])

    getResults.append([['Name', 'Genres', 'ID'], artists])

    albumInput = getUserInput(*getResults[0])

    albumResult = spotifyGet(createAlbumUrl(albumInput[2]))

    albums = []
    for album in albumResult.json()['items']:
        albums.append([album['name'], album['id']])

    getResults = [['Name', 'ID'], albums]

    songInput = getUserInput(*getResults)

    songResult = spotifyGet(createGetAlbumTracksUrl(songInput[1]))

    songs = []
    for song in songResult.json()['tracks']['items']:
        songs.append([song['name'], song['explicit'], song['id']])

    getResults = [['Name', 'Explicit', 'ID'], songs]

    getUserInput(*getResults)

    # Todo: Track Info display und zurück gehen. Vielleicht switch case mit einer Stufenvariable, die hoch gezählt wird
