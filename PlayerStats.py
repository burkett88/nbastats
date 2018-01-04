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

#%%
# id, name, years played, team, team_id, team_code 
person_id_list=players['PERSON_ID'].unique()[:10] #grab just 10 players

#%%
alllogs=pd.DataFrame()

#%%
df=player.PlayerGameLogs(i).info()

#%%
for i in person_id_list:
    df=player.PlayerGameLogs(i).info()
    df['GAME_DATE']=pd.to_datetime(df['GAME_DATE']) 
    df['30DAYS_DATE']=df['GAME_DATE']-pd.to_timedelta(30, unit='d')
    alllogs=alllogs.append(df)

#%%
# Per ShotType/Game
player.PlayerShotTracking(players.loc[0,"PERSON_ID"]).general_shooting()

#%%
# Doesn't work
# player.PlayerShotLogTracking(players.loc[0,"PERSON_ID"])

#%%
# Needs two players
# player.PlayerVsPlayer(players.loc[0,"PERSON_ID"]).overall()

