import argparse
import os
import sys

from dotenv import load_dotenv

from chesscli.api import ChessAPIError, NotFoundError, get_profile


# ---------- display ----------

def display_profile(profile: dict) -> None:
    country = profile.get("country", "")
    print(f"Username: {profile.get('username', 'N/A')}")
    print(f"Name: {profile.get('name', 'N/A')}")
    print(f"Title: {profile.get('title', 'None')}")
    print(f"Followers: {profile.get('followers', 0)}")
    print(f"Country: {country.rsplit('/', 1)[-1] if country else 'N/A'}")
    print(f"Status: {profile.get('status', 'N/A')}")


# ---------- command handlers ----------

def cmd_profile(args: argparse.Namespace) -> None:
    profile = get_profile(args.username, args.email)
    display_profile(profile)


# ---------- parser ----------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chesscli",
        description="Explore Chess.com players from your terminal.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_profile = sub.add_parser("profile", help="Show a player's profile")
    p_profile.add_argument("username", help="Chess.com username")
    p_profile.set_defaults(func=cmd_profile)

    return parser


# ---------- entry point ----------

def main() -> None:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()

    args.email = os.getenv("CHESS_CONTACT_EMAIL", "")
    if not args.email:
        print("Warning: set CHESS_CONTACT_EMAIL in .env", file=sys.stderr)

    try:
        args.func(args)
    except NotFoundError:
        print(f"Not found: {getattr(args, 'username', '')}", file=sys.stderr)
        sys.exit(1)
    except ChessAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
