#%%
from os.path import exists
import pandas as pd
from tqdm import tqdm
import sys
from time import sleep
from random import random

from nba_py import team, constants, player, game

#%%
players_path = "players.csv"
if exists(players_path):
    players = pd.read_csv(players_path)
else:
    players = player.PlayerList().info()
    players.to_csv(players_path)

#%%
# id, name, years played, team, team_id, team_code 
person_id_list=players['PERSON_ID'].unique()
stats=['MIN', 'FGM',
       'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
       'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
       'PLUS_MINUS']

#%%
gamelog_path = "gamelogs.csv"
if exists(gamelog_path):
    gamelogs = pd.read_csv(gamelog_path,index_col=[0,1,2,3])
else:
    n = len(person_id_list)
    dfs = []
    for i,pid in enumerate(person_id_list):
        sleep(random())
        if i > 0 and i % 5 == 0:
            sys.stderr.write("{} of {} Done\r".format(i,n))
        df=player.PlayerGameLogs(pid).info()
        df['GAME_DATE']=pd.to_datetime(df['GAME_DATE']) 
        # Make all the ID's indexes
        df=df.set_index(['GAME_DATE','SEASON_ID','Game_ID','Player_ID'])
        dfs.append(df)
    sys.stderr.write("{} of {} Done\n".format(n,n))
    gamelogs = pd.concat(dfs)
    gamelogs.to_csv(gamelog_path)
gamelogs
#%%

dfs = []
for player_id,df in gamelogs.groupby("Player_ID"):
    # Only bring along the stats we are using for averaging for now
    df = df[stats]
    # This was slow, so commented out. Instead should do a single call to get a list of all the game scores and use pandas to find team id
    # df['OpposingTeam']=df['Game_ID'].apply(lambda x: game.BoxscoreSummary(x).game_summary()['VISITOR_TEAM_ID'])
    df_cols = [df]
    keys = [1]
    for rollingPeriod in (7,14):
        dfr = df.apply(lambda col: col.rolling(rollingPeriod).mean())
        df_cols.append(dfr)
        keys.append(rollingPeriod)
    df = pd.concat(df_cols,keys=keys,names=["RollingPeriod","Stat"],axis=1)
    dfs.append(df)
gamelogs_rolling = pd.concat(dfs)
gamelogs_rolling

#%%
# Flattened column names
gamelogs_rolling_flat = gamelogs_rolling.copy()
gamelogs_rolling_flat.columns = ["{}_{}".format(b,a) for a,b in gamelogs_rolling_flat.columns.values]
gamelogs_rolling_flat

#%%
visitingTeamid = game.BoxscoreSummary("0021601230").game_summary()['VISITOR_TEAM_ID']
print(game.BoxscoreSummary("0021601230").game_summary())

#%%
PreviousGame = game.BoxscoreSummary("0021601230").last_meeting()
TotPointsPrevGame=PreviousGame['LAST_GAME_HOME_TEAM_POINTS']+PreviousGame['LAST_GAME_VISITOR_TEAM_POINTS']

#%%
# Per ShotType/Game
player.PlayerShotTracking(players.loc[0,"PERSON_ID"]).general_shooting()

#%%
# Doesn't work
# player.PlayerShotLogTracking(players.loc[0,"PERSON_ID"])

#%%
# Needs two players
# player.PlayerVsPlayer(players.loc[0,"PERSON_ID"]).overall()

