"""
Given the following inputs:
- <game_data> is a list of dictionaries, with each dictionary representing a player's shot attempts in a game. The list can be empty, but any dictionary in the list will include the following keys: gameID, playerID, gameDate, fieldGoal2Attempted, fieldGoal2Made, fieldGoal3Attempted, fieldGoal3Made, freeThrowAttempted, freeThrowMade. All values in this dictionary are ints, except for gameDate which is of type str in the format 'MM/DD/YYYY'
- <true_shooting_cutoff> is the minimum True Shooting percentage value for a player to qualify in a game. It will be an int value >= 0.
- <player_count> is the number of players that need to meet the <true_shooting_cutoff> in order for a gameID to qualify. It will be an int value >= 0.

Implement find_qualified_games to return a list of unique qualified gameIDs in which at least <player_count> players have a True Shooting percentage >= <true_shooting_cutoff>, ordered from most to least recent game.
"""
from typing import List, Dict 
from collections import defaultdict
from datetime import datetime

def find_qualified_games(game_data: List[Dict], true_shooting_cutoff: int, player_count: int) -> List[int]:
    
    # Function to calculate the True Shooting Percentage 
    def calculate_true_shooting_percentage(fga, fgm, fta, ftm):
        if (fga + fta) == 0: # In case aything equals 0/ Didn't Play
            return 0
        return (fgm + ftm) / (fga + fta) * 100  #Calculating the true shooting percentage 
    
    # Store qualified player counts per game
    game_player_count = defaultdict(int)
    game_dates = {}
    
    for entry in game_data:
        game_id = entry['gameID']
        player_id = entry['playerID']
        fga = entry['fieldGoal2Attempted'] + entry['fieldGoal3Attempted']
        fgm = entry['fieldGoal2Made'] + entry['fieldGoal3Made']
        fta = entry['freeThrowAttempted']
        ftm = entry['freeThrowMade']
        
        ts_percentage = calculate_true_shooting_percentage(fga, fgm, fta, ftm)
        
        if ts_percentage >= true_shooting_cutoff:
            game_player_count[game_id] += 1
        
        if game_id not in game_dates:
            game_dates[game_id] = datetime.strptime(entry['gameDate'], '%m/%d/%Y')
    
    # Find The qualified game IDs
    qualified_games = [
        game_id for game_id, count in game_player_count.items()
        if count >= player_count
    ]
    
    # Sort by the date of the game, with the most recent being first
    qualified_games.sort(key=lambda game_id: game_dates[game_id], reverse=True)
    
    return qualified_games

