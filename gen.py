import requests, os
from collections import defaultdict
import base64
import sys

TOKEN = os.getenv("OC_TOKEN")
try:
    assert TOKEN.count("-") == 4 and len(TOKEN) == 36
except:
    raise ValueError("Invalid token format")

PLAYER_URL = "https://training.olicyber.it/api/scoreboard/player"
SCOREBOARD_URL = "https://training.olicyber.it/api/scoreboard"

if TOKEN is None:
    raise ValueError("TOKEN environment variable not set")

headers = {
    "Authorization": f"Token {TOKEN}",
}

def resolve_fullname(player_data) -> str:
    return player_data["name"] + " " + player_data["surname"] + " (" + player_data["nickname"] + ")"

def find_scoreboard_position(player_data) -> int:
    display_name = resolve_fullname(player_data)
    scoreboard = requests.get(SCOREBOARD_URL, params={"noFreeze": False}, headers=headers).json()["scoreboard"]
    return next(i for i, player in enumerate(scoreboard) if player["displayedName"] == display_name) + 1

def find_best_category(player_data) -> str:
    categories = player_data["categories"]
    return max(categories, key=lambda category: categories[category]["solves"]).capitalize()

user_data = requests.get(PLAYER_URL, headers=headers).json()
useful_data = {
    "scoreboard_position": find_scoreboard_position(user_data),
    "username": user_data["nickname"],
    "solved_challenges": user_data["correctSubmissions"],
    "score": user_data["score"],
    "best_category": find_best_category(user_data),
}

def make_card(data, template="default"):
    try: 
        logo = open("data/logo.svg", 'r').read()
    except: 
        raise ValueError("data/logo.svg not found")
    
    data["logo"] = base64.b64encode(logo.encode()).decode()
    
    template_filename = f"data/template_{template}.svg"
    try: 
        return open(template_filename, 'r').read().format_map(defaultdict(lambda: "N/A", data))
    except Exception as e:
        raise ValueError(f"{template_filename} not found, or invalid: {str(e)}")


template_style = "default"

if len(sys.argv) > 1 and sys.argv[1] in ["default", "dark", "white","darkRed","darkBlue"]:
    template_style = sys.argv[1]


with open("card.svg", "w") as f:
    f.write(make_card(useful_data, template_style))