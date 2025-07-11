import requests
from data_structures import *

BaseUrl = 'https://games-test.datsteam.dev/api'
RegisterUrl = BaseUrl + '/register'
ArenaUrl = BaseUrl + '/arena'
MoveUrl = BaseUrl + '/move'
LogsUrl = BaseUrl + '/logs'

def get_token() -> str:
    filename = 'token.txt'
    with open(filename, 'r') as file:
        line = file.readline()
        line = line[:-1]
    return line

Token = get_token()
Headers = { 'X-Auth-Token': Token }

def register_to_round() -> bool:
    response = requests.post(RegisterUrl, headers=Headers)
    if response.status_code != 200:
        print('API error when registering to round')
        print(response.text)
        return False
    else: 
        data = response.json()
        print('REGISTERED TO A ROUND:\n ', data)
        return True

def get_arena() -> dict:
    response = requests.get(ArenaUrl, headers=Headers)
    if response.status_code != 200:
        print('API error when fetching arena')
        print(response.text)
        return dict()
    else: 
        data = response.json()
        return data

def make_move(moves: list[Move]) -> dict:
    response = requests.post(MoveUrl, headers=Headers, json=moves)
    if response.status_code != 200:
        print('API error when making move')
        print(response.text)
        return dict()
    else:
        data = response.json()
        return data


def get_logs() -> list:
    response = requests.get(LogsUrl, headers=Headers)
    if response.status_code != 200:
        print('API error when fetching logs')
        print(response.text)
        return list()
    else: 
        data = response.json()
        return data

if __name__ == '__main__':
    register_to_round()
    arena = get_arena()
    hexes_in_response = arena['map']
    hexes = list()
    for h in hexes_in_response:
        hexes.append(Hex(h['q'], h['r'], HexType(h['type']), h['cost']))

    print(hexes)
    #print(arena['ants'])

