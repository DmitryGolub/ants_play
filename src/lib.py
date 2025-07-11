import json
import requests
from typing import Any, Optional
from env import *


def sender(path: str, payload: Optional[dict] = None) -> Optional[requests.Response]:
    url = f"{BASEURL}{path}"
    response = requests.post(url=url, headers=HEADERS, json=payload)
    return response if response.status_code == 200 else None


def write_json(data: Any) -> None:
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def getter(path: str) -> Optional[dict]:
    response = requests.get(url=path, headers=HEADERS)
    return response.json() if response.status_code == 200 else None
