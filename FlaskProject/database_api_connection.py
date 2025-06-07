import os
from nba_api.stats import endpoints
from nba_api.stats.static import teams, players
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_tables import Base, TodayGames, AllPlayers
import datetime
import time
import pandas as pd
import traceback
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, connect_args={'client_encoding': 'utf8'})

Session = sessionmaker(bind=engine)


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Udało się utworzyć tabele")
    except Exception as e:
        print("Błąd przy tworzeniu tabel:\n", e)

def drop_tables():
    try:
        Base.metadata.drop_all(bind=engine)
        print("Udało się usunąć tabele")
    except Exception as e:
        print("Błąd przy usuwaniu tabel:\n", e)

def get_today_games_from_db(today_date_var):
    session = Session()

    try:
        today_games = session.query(TodayGames).filter(TodayGames.game_date_est == today_date_var).all()

        return today_games

    except Exception as e:
        print("There are no games scheduled for today:\n", e)

        return []

    finally:
        session.close()

def fetch_today_games_to_db(today_date_var):
    session = Session()
    today_games_in_db = get_today_games_from_db(today_date_var)

    if not today_games_in_db:
        try:
            scoreboard = endpoints.ScoreboardV2(game_date=today_date_var)
            today_games = scoreboard.game_header.get_dict()['data']
            #print("1 pass")

            for game in today_games:

                home_team_name = teams.find_team_name_by_id(game[6])['full_name']
                away_team_name = teams.find_team_name_by_id(game[7])['full_name']
                #print("2 pass")

                all_players, players_ids = get_all_players_from_db()

                top_home_player_fullname = None
                top_home_player_country = None
                top_home_player_position = None
                top_home_player_points_per_game = 0.0
                top_home_player_photo_URL = None

                top_away_player_fullname = None
                top_away_player_country = None
                top_away_player_position = None
                top_away_player_points_per_game = 0.0
                top_away_player_photo_URL = None

                home_player_most_points = 0
                away_player_most_points = 0

                for player in all_players:

                    if player.is_active == True and player.last_10_games_minutes is not None:

                        if player.current_team == home_team_name:
                            home_player_points = player.last_10_games_points

                            if home_player_points > home_player_most_points:
                                home_player_most_points = home_player_points
                                player_last_10_games_count = player.last_10_games_count

                                top_home_player_points_per_game = home_player_points / player_last_10_games_count
                                top_home_player_fullname = f"{player.first_name} {player.last_name}"
                                top_home_player_country = player.country
                                top_home_player_position = player.position
                                top_home_player_photo_URL = "https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(player.player_id)


                        elif player.current_team == away_team_name:
                            away_player_points = player.last_10_games_points

                            if away_player_points > away_player_most_points:
                                away_player_most_points = away_player_points
                                player_last_10_games_count = player.last_10_games_count

                                top_away_player_points_per_game = away_player_points / player_last_10_games_count
                                top_away_player_fullname = f"{player.first_name} {player.last_name}"
                                top_away_player_country = player.country
                                top_away_player_position = player.position
                                top_away_player_photo_URL = "https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(player.player_id)

                # print("3 pass")
                db_game = TodayGames(
                    game_id = game[2],
                    game_date_est = game[0],
                    game_season = game[8],
                    home_team_id = game[6],
                    home_team_name = home_team_name,
                    home_team_logo_URL = "https://cdn.nba.com/logos/nba/{}/global/L/logo.svg".format(game[6]),
                    away_team_id = game[7],
                    away_team_name = away_team_name,
                    away_team_logo_URL = "https://cdn.nba.com/logos/nba/{}/global/L/logo.svg".format(game[7]),
                    game_status_id = game[3],
                    game_status_text = game[4],
                    arena_name = game[15],

                    top_home_player_fullname = top_home_player_fullname,
                    top_home_player_country = str(top_home_player_country),
                    top_home_player_position = str(top_home_player_position),
                    top_home_player_points_per_game = float(top_home_player_points_per_game),
                    top_home_player_photo_URL = top_home_player_photo_URL,

                    top_away_player_fullname = top_away_player_fullname,
                    top_away_player_country = str(top_away_player_country),
                    top_away_player_position = str(top_away_player_position),
                    top_away_player_points_per_game = float(top_away_player_points_per_game),
                    top_away_player_photo_URL = top_away_player_photo_URL
                )

                session.add(db_game)
                #print("4 pass")

            session.commit()

        except Exception as e:
            print("Save to db Exception:\n", e)
            session.rollback()

        finally:
            session.close()

    else:
        print("Today games already exist")

def fetch_all_players_to_db():
    session = Session()
    all_players_api = players.get_players()
    _, all_players_ids = get_all_players_from_db()

    insert_counter = 0

    try:
        for player in all_players_api:
            player_id = player['id']

            if player_id in all_players_ids:
                continue

            #Domyślne wartości statystyk (None) jakby któryś gracz nmie miał danych
            whole_season = None
            last_10_games_shots_acc = None
            last_10_games_points = None
            last_10_games_minutes = None
            last_10_games_losses = None
            last_10_games_wins = None
            last_10_games_assists = None
            last_season_games_played = None
            player_last_10_games_count = None
            team_name = None
            height_cm = None
            weight_kg = None

            try:

                try:
                    player_stats = endpoints.playergamelog.PlayerGameLog(player_id=player_id).get_data_frames()[0]

                    if not player_stats.empty and 'SEASON_ID' in player_stats:
                        last_season_id = max(player_stats['SEASON_ID'].unique())
                        season_start_year = int(str(last_season_id)[1:])
                        season_end_year = season_start_year + 1
                        whole_season = f"{season_start_year}-{season_end_year}"

                        player_last_10_games = player_stats.head(10)
                        player_last_10_games_count = len(player_last_10_games)
                        fga = player_last_10_games['FGA'].sum()
                        last_10_games_shots_acc = round(player_last_10_games['FGM'].sum() / fga, 2) if fga else 0.0
                        last_10_games_points = player_last_10_games['PTS'].sum()
                        last_10_games_minutes = player_last_10_games['MIN'].sum()
                        last_10_games_losses = player_last_10_games['WL'].value_counts().get('L', 0)
                        last_10_games_wins = player_last_10_games['WL'].value_counts().get('W', 0)
                        last_10_games_assists = player_last_10_games['AST'].sum()
                        last_season_games_played = player_stats[player_stats['SEASON_ID'] == last_season_id].shape[0]
                except Exception:
                    pass

                #Dane osobowe
                player_info_df = endpoints.commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]

                birthdate = pd.to_datetime(player_info_df['BIRTHDATE'].iloc[0]).date()
                age_years = (datetime.date.today() - birthdate).days // 365
                try:
                    height = player_info_df['HEIGHT'].iloc[0]
                    feet, inches = map(int, height.split('-'))
                    height_cm = round(feet * 30.48 + inches * 2.54, 2)

                except Exception:
                    pass

                try:
                    weight_kg = round(float(player_info_df['WEIGHT'].iloc[0]) * 0.45359237, 2)

                except Exception:
                    pass

                jersey = player_info_df['JERSEY'].iloc[0]
                jersey_nr = int(jersey) if jersey and jersey.isdigit() else None

                position = player_info_df['POSITION'].iloc[0]
                country = player_info_df['COUNTRY'].iloc[0]

                try:
                    if 'TEAM_ID' in player_info_df.columns:
                        team_id = player_info_df['TEAM_ID'].iloc[0]
                        if pd.notna(team_id):
                            team_info = teams.find_team_name_by_id(team_id)
                            if team_info and 'full_name' in team_info:
                                team_name = team_info['full_name']
                                #print("Team: " + team_name)
                except Exception as e:
                    team_name = None
                    print("Nie udało się pobrać pełnej nazwy drużyny:\n", e)

                player_record = AllPlayers(
                    player_id = int(player_id),
                    first_name = player['first_name'],
                    last_name = player['last_name'],
                    age = int(age_years) if age_years is not None else None,
                    height = float(height_cm) if height_cm is not None else None,
                    weight = float(weight_kg) if weight_kg is not None else None,
                    jersey_nr = int(jersey_nr) if jersey_nr is not None else None,
                    current_team = team_name,
                    position = position,
                    country = country,
                    last_season = whole_season,
                    ls_games_played = int(last_season_games_played) if last_season_games_played is not None else None,
                    last_10_games_count = int(player_last_10_games_count) if player_last_10_games_count is not None else None,
                    last_10_games_wins = int(last_10_games_wins) if last_10_games_wins is not None else None,
                    last_10_games_losses = int(last_10_games_losses) if last_10_games_losses is not None else None,
                    last_10_games_points = int(last_10_games_points) if last_10_games_points is not None else None,
                    last_10_games_assists = int(last_10_games_assists) if last_10_games_assists is not None else None,
                    last_10_games_minutes = float(last_10_games_minutes) if last_10_games_minutes is not None else None,
                    last_10_games_shots_acc = float(last_10_games_shots_acc) if last_10_games_shots_acc is not None else None,
                    is_active = bool(player['is_active']),
                )

                session.add(player_record)
                session.commit()
                insert_counter += 1
                print(f"{insert_counter}. Dodano gracza: {player['first_name']} {player['last_name']}")
                if insert_counter == 301:
                    print(f"Zrestartuj aplikacje bo to było {insert_counter} zapytanie i api się wywalilo")
                time.sleep(0.5)

            except Exception as player_error:
                print(f"Błąd przy przetwarzaniu gracza {player['first_name']} {player['last_name']}: {player_error}")
                traceback.print_exc()
                session.rollback()

    except Exception as e:
        print("Błąd główny w fetch_all_players_to_db():\n", e)
        traceback.print_exc()

    finally:
        session.close()


def get_all_players_from_db():
    session = Session()
    all_players_db = None
    all_players_ids = None

    try:
        all_players_db = session.query(AllPlayers).all()
        all_players_ids = {player_id for (player_id,) in session.query(AllPlayers.player_id).all()}
    except Exception as e:
        print("Nie udalo sie pobrac graczy z bazy:\n", e)

    finally:
        session.close()

    return all_players_db, all_players_ids













