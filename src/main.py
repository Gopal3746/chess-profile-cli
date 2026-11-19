from ast import arg
import os
import requests
import sys
from dotenv import load_dotenv

from constants import TIMEOUT

BASE_URL = "https://api.chess.com/pub/"

def _get(path: str, email: str) -> dict | None:
    headers = {"User-Agent": f"MyChessApp/1.0 (contact: {email})"}
    try:
        response = requests.get(f"{BASE_URL}{path}", headers=headers, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

    if response.status_code == 404:
        print("Not found")
        return None
    if response.status_code != 200:
        print(f"Request failed. Status code: {response.status_code}")
        return None
    return response.json()


def get_profile(username: str, email: str) -> dict | None:
    return _get(f"player/{username}", email)


def get_stats(username: str, email: str) -> dict | None:
    return _get(f"player/{username}/stats", email)

def display_profile(profile: dict) -> None:
    country = profile.get("country", "")
    print(f"Name: {profile.get('name', 'N/A')}")
    print(f"Title: {profile.get('title', 'None')}")
    print(f"Followers: {profile.get('followers', 0)}")
    print(f"Country: {country.rsplit('/', 1)[-1] if country else 'N/A'}")
    print(f"Status: {profile.get('status', 'N/A')}")


def main() -> None:
    load_dotenv()
    email = os.getenv("CHESS_CONTACT_EMAIL", "")
    if not email:
        print("Set CHESS_CONTACT_EMAIL in your .env")
        return
    args = sys.argv
    if len(args) < 2:
        print("Enter username")
        return
    username = args[1]
    profile = get_profile(username, email)
    if profile:
        display_profile(profile)

if __name__ == "__main__":
    main()
