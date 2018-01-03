#%%
from os.path import exists
import pandas as pd

from nba_py import team, constants, player

#%%
players_path = "players.csv"
if exists(players_path):
    players = pd.read_csv(players_path)
else:
    players = player.PlayerList().info()
    players.to_csv(players_path)

# id, name, years played, team, team_id, team_code 
players

#%%
# Game Logs, basic stats
player.PlayerGameLogs(players.loc[0,"PERSON_ID"]).info().iloc[0]

#%%
# Per ShotType/Game
player.PlayerShotTracking(players.loc[0,"PERSON_ID"]).general_shooting()

#%%
# Doesn't work
# player.PlayerShotLogTracking(players.loc[0,"PERSON_ID"])

#%%
# Needs two players
# player.PlayerVsPlayer(players.loc[0,"PERSON_ID"]).overall()

