#%%
from os.path import exists
import pandas as pd

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
person_id_list=players['PERSON_ID'].unique()[:15] #grab just 10 players for now
stats=['MIN', 'FGM',
       'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
       'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
       'PLUS_MINUS']

#%%
alllogs = []
for i in person_id_list:
    df=player.PlayerGameLogs(i).info()
    df['GAME_DATE']=pd.to_datetime(df['GAME_DATE']) 
    df=df.set_index('GAME_DATE')
    df['OpposingTeam']=df['Game_ID'].apply(lambda x: game.BoxscoreSummary(x).game_summary()['VISITOR_TEAM_ID'])
    df_cols = [df]
    keys = [1]
    for rollingPeriod in (7,):
        dfr = df[stats].apply(lambda col: col.rolling(rollingPeriod).mean())
        df_cols.append(dfr)
        keys.append(rollingPeriod)
    df = pd.concat(df_cols,keys=keys,names=["RollingPeriod","Stat"],axis=1)
    alllogs.append(df)
#%%
alllogs = pd.concat(alllogs)
alllogs
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

