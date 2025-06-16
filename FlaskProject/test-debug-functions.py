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


# drop_tables(AllTeams)
# create_tables()
#
# fetch_teams_to_db()

# all_teams_api = teams.get_teams()
#
# print(len(all_teams_api))
#
# for team in all_teams_api:
#     print(team['id'])


# all_players_data, _ = get_all_players_from_db()
# players_countries_list = [player.country for player in all_players_data]
# players_countries = pd.Series(players_countries_list).value_counts()
#
# usa_count = players_countries.get('USA', 0)
# rest_sum = players_countries.sum() - usa_count
# usa_vs_rest = pd.Series({'USA': usa_count, 'Reszta świata': rest_sum})
#
# other_countries = players_countries.drop('USA', errors='ignore')
# other_countries = other_countries[other_countries > 5]
#
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
#
# usa_vs_rest.plot.pie(
#     ax=ax1,
#     autopct='%1.1f%%',
#     startangle=90,
#     colors=['#1f77b4', '#ff7f0e'],
#     wedgeprops={'edgecolor': 'white'}
# )
# ax1.set_title('Dystrybucja wg. krajów USA vs Reszta', pad=20)
# ax1.set_ylabel('')
#
# other_countries.plot.pie(
#     ax=ax2,
#     autopct='%1.1f%%',
#     startangle=90,
#     colormap='tab20',
#     wedgeprops={'edgecolor': 'white'}
# )
# ax2.set_title('Rozkład pozostałych krajów', pad=20)
# ax2.set_ylabel('')
#
# plt.tight_layout()
# plt.show()

# all_players_data, _ = get_all_players_from_db()
#
# test_data = []
#
# for player in all_players_data:
#     test_data.append(player.is_active)
#
#
# test = pd.Series(test_data).value_counts().get(key=False)
#
# print(test)

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# all_players_data, _ = get_all_players_from_db()
# active_status = None
#
#
# players_heights_list = []
# for player in all_players_data:
#     if (active_status is True or active_status is False) and player.is_active == active_status and player.height is not None:
#         players_heights_list.append(int(round(player.height, 0)))
#     elif active_status is None and player.height is not None:
#         players_heights_list.append(int(round(player.height, 0)))
#
# players_heights = pd.Series(players_heights_list).value_counts().sort_values(ascending=False)
#
# print(players_heights)

# players_weights_list = []
# for player in all_players_data:
#     if (active_status is True or active_status is False) and player.weight is not None:
#         players_weights_list.append(int(round(player.weight, 0)))
#     elif active_status is None and player.weight is not None:
#         players_weights_list.append(int(round(player.weight, 0)))
#
# players_weights = pd.Series(players_weights_list).value_counts().sort_values(ascending=False)
# print(players_weights)


all_players_data, _ = get_all_players_from_db()

for player in all_players_data:
    print(player.current_team)














