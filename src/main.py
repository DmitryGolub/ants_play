import requests


print("start")

with requests.Session() as session:
    headers = {
        'accept': 'application/json',
        'X-Auth-Token': 'e71c6ce6-f297-40fb-9a44-16b650933bec'
    }

    register = session.post(
        url="https://games-test.datsteam.dev/api/register",
        headers=headers
    )

    if register.status_code == 200:
        print("Success authenticate")
    else:
        print("Unsuccess authenticate")
        print(register)
        raise TimeoutError("Register was finished, wait new game")
