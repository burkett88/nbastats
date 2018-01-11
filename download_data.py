#%%
from os.path import exists
import pandas as pd
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
players.head()

#%%
gamelog_path = "gamelogs.csv"
if exists(gamelog_path):
    gamelogs = pd.read_csv(gamelog_path,index_col=[0,1,2,3])
else:
    person_id_list=players['PERSON_ID'].unique()
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
gamelogs.head()