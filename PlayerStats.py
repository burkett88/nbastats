#%%
from pathlib import Path
import pandas as pd

from nba_py import team, constants, player

import os
print(os.getcwd())
#%%
players_path = "players.pkl"
if Path(players_path).exists():
    players = pd.read_pickle(players_path)
else:
    players = player.PlayerList().info()
    players.to_pickle(players_path)

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

