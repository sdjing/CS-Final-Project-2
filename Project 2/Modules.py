from nba_api.stats.endpoints._base import Endpoint
from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.library.parameters import Season, SeasonTypeAllStar, LeagueIDNullable
from nba_api.stats.endpoints import playergamelog
import math 
import pandas as pd
import json
from nba_api.stats.static import players
    
def lambda_handler(event, context):
    name = event["queryStringParameters"]["name"]
    nba_players = players.get_players()
    nba_players[:5]
    matchedNames = []
    for player in nba_players:
        if player["full_name"].lower() == name.lower():
            return ["found", player["id"]]
        elif player["full_name"].split() == name.split():
            return ["found", player["id"]]
        elif player["first_name"].lower() == name.strip().lower() or player["last_name"].lower() == name.strip().lower():
            matchedNames.append(player["full_name"])

    if matchedNames:
        return matchedNames
    else:
        errorMessage = ["Didn't find ID", matchedNames]
        return errorMessage