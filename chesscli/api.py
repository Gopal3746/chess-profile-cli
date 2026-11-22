import requests
from chesscli.constants import TIMEOUT

BASE_URL = "https://api.chess.com/pub/"


class ChessAPIError(Exception):
    pass


class NotFoundError(ChessAPIError):
    pass


def _get(path: str, email: str) -> dict:
    headers = {"User-Agent": f"chesscli/0.1 (contact: {email or 'unknown'})"}
    try:
        response = requests.get(f"{BASE_URL}{path}", headers=headers, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        raise ChessAPIError(f"Network error: {e}") from e

    if response.status_code == 404:
        raise NotFoundError(path)
    if response.status_code != 200:
        raise ChessAPIError(f"Request failed with status {response.status_code}")
    return response.json()


def get_profile(username: str, email: str) -> dict:
    return _get(f"player/{username}", email)
