import requests

def get_profile_information(username: str):
    url = "https://api.chess.com/pub/player/"
    payload = f"{url}{username}"
    response = requests.get(payload)
    if (response.status_code == 200):
        profile = response.json()
        print(f"Name: {profile.get('name')}")
        print(f"Title: {profile.get('title')}")
        print(f"Followers: {profile.get('followers')}")
        print(f"Country URL: {profile.get('country')}")
        print(f"Status: {profile.get('status')}")
    else:
        print(f"Failed to fetch profile. Status code: {response.status_code}")


def main():
    username = "hikaru"
    get_profile_information(username)

if __name__ == "__main__":
    main()
