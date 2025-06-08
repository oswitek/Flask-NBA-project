import os
from nba_api.stats import endpoints
from nba_api.stats.static import teams, players
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_tables import Base, TodayGames, AllPlayers, AllTeams
import datetime
import time
import pandas as pd
import traceback
from dotenv import load_dotenv
from database_api_connection import *

import matplotlib.pyplot as plt
import seaborn as sns


# drop_tables()
# create_tables()

# scoreboard = endpoints.ScoreboardV2(game_date='2025-06-08')
# today_games = scoreboard.game_header.get_dict()['data']


# for game in today_games:
#     home_team_name = teams.find_team_name_by_id(game[6])['full_name']
#     away_team_name = teams.find_team_name_by_id(game[7])['full_name']
#     print(home_team_name + " VS " + away_team_name)
#
#     all_players, players_ids = get_all_players_from_db()
#
#     for player in all_players:
#         if player.is_active and player.current_team == home_team_name and player.current_team == away_team_name:
#             print(player.first_name + " " + player.last_name + " Team: " + player.current_team)
#
#         else:
#             print(f"{player.current_team} doesn't match {home_team_name} or {away_team_name}")


#fetch_all_players_to_db()

#today_date = datetime.today().strftime('%Y-%m-%d')
# today_date = '2025-06-08'

#get_all_players_from_db()

# fetch_today_games_to_db(today_date)
# today_games = get_today_games_from_db(today_date)
#
# for game in today_games:
#     print(game.to_dict())

# test = get_specific_player_from_db('LeBron James')
#
# print(test)


# player = "LeBron James"
#
# player_found = get_specific_player_from_db(player)
#
# print(player_found['country'])

# Test wykresu np rozkladu country wsród graczy przy uzyciu matpltlib i seaborn

# all_players_data, _ = get_all_players_from_db()
#
# players_countries_list = []
#
# for player in all_players_data:
#     if player.country != 'USA':
#         players_countries_list.append(player.country)
#
# players_countries = pd.Series(players_countries_list).sort_values(ascending=False).value_counts()
#
# #Jebać to zrobimy na PowerBi bo nie da sie interaktywnie tutaj
#
# plt.figure(figsize=(10,8))
# players_countries.plot(kind='bar')
# plt.title("NBA players not from USA distribution by country", fontsize=20)
# plt.xlabel("Country", fontsize=15)
# plt.ylabel("Players count", fontsize=15)
# plt.grid(axis='y',linestyle='--' , alpha=0.75)
# plt.tight_layout()


# year = '2020'
#
#
#
# teams_var = teams.get_teams()
# print(teams_var)



#create_tables()
#drop_tables(AllTeams)















