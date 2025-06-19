from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TodayGames(Base):
    __tablename__ = 'today_games_info'
    game_id = Column(Integer, primary_key=True)
    game_date_est = Column(DateTime)
    game_season = Column(Integer)

    home_team_id = Column(Integer)
    home_team_name = Column(String)
    home_team_logo_URL = Column(String)

    away_team_id = Column(Integer)
    away_team_name = Column(String)
    away_team_logo_URL = Column(String)

    game_status_id = Column(Integer)
    game_status_text = Column(String)
    arena_name = Column(String)

    top_home_player_fullname = Column(String)
    top_home_player_country = Column(String)
    top_home_player_position = Column(String)
    top_home_player_photo_URL = Column(String)
    top_home_player_points_per_game = Column(Float)

    top_away_player_fullname = Column(String)
    top_away_player_country = Column(String)
    top_away_player_position = Column(String)
    top_away_player_photo_URL = Column(String)
    top_away_player_points_per_game = Column(Float)

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'game_date_est': self.game_date_est,
            'game_season': self.game_season,
            'home_team_id': self.home_team_id,
            'home_team_name': self.home_team_name,
            'home_team_logo_URL': self.home_team_logo_URL,
            'away_team_id': self.away_team_id,
            'away_team_name': self.away_team_name,
            'away_team_logo_URL': self.away_team_logo_URL,
            'game_status_id': self.game_status_id,
            'game_status_text': self.game_status_text,
            'arena_name': self.arena_name,

            'top_home_player_fullname': self.top_home_player_fullname,
            'top_home_player_country': self.top_home_player_country,
            'top_home_player_position': self.top_home_player_position,
            'top_home_player_points_per_game': self.top_home_player_points_per_game,
            'top_home_player_photo_URL': self.top_home_player_photo_URL,

            'top_away_player_fullname': self.top_away_player_fullname,
            'top_away_player_country': self.top_away_player_country,
            'top_away_player_position': self.top_away_player_position,
            'top_away_player_points_per_game': self.top_away_player_points_per_game,
            'top_away_player_photo_URL': self.top_away_player_photo_URL
        }

    def __repr__(self):
        return "<Game {}>".format(self.game_id)



class AllPlayers(Base):
    __tablename__ = 'all_players_info'

    player_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    current_team = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    jersey_nr = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    country = Column(String, nullable=True)

    last_season = Column(String, nullable=True)
    ls_games_played = Column(Integer, nullable=True)

    last_10_games_count = Column(Integer, nullable=True)
    last_10_games_wins = Column(Integer, nullable=True)
    last_10_games_losses = Column(Integer, nullable=True)
    last_10_games_points = Column(Integer, nullable=True)
    last_10_games_assists = Column(Integer, nullable=True)
    last_10_games_minutes = Column(Float, nullable=True)
    last_10_games_shots_acc = Column(Float, nullable=True)

    is_active = Column(Boolean, nullable=False)

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'current_team': self.current_team,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'jersey_nr': self.jersey_nr,
            'position': self.position,
            'country': self.country,
            'last_season': self.last_season,
            'ls_games_played': self.ls_games_played,
            'last_10_games_count': self.last_10_games_count,
            'last_10_games_wins': self.last_10_games_wins,
            'last_10_games_losses': self.last_10_games_losses,
            'last_10_games_points': self.last_10_games_points,
            'last_10_games_assists': self.last_10_games_assists,
            'last_10_games_minutes': self.last_10_games_minutes,
            'last_10_games_shots_acc': self.last_10_games_shots_acc,
            'is_active': self.is_active
        }

    def __repr__(self):
        return "<Player {}>".format(self.player_id)


class AllTeams(Base):
    __tablename__ = 'teams_info'
    team_id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    year_founded = Column(Integer, nullable=True)

    def to_dict(self):
        return {
            'team_id': self.team_id,
            'full_name': self.full_name,
            'abbreviation': self.abbreviation,
            'nickname': self.nickname,
            'city': self.city,
            'state': self.state,
            'year_founded': self.year_founded,
        }

    def __repr__(self):
        return "<Team {}>".format(self.full_name)
