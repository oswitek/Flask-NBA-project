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

    top_home_player_name = Column(String)
    top_home_player_photo_URL = Column(String)
    top_away_player_name = Column(String)
    top_away_player_photo_URL = Column(String)

    def to_dict(self):
        return {
            'id': self.game_id,
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
            'top_home_player_name': self.top_home_player_name,
            'top_home_player_photo_URL': self.top_home_player_photo_URL,
            'top_away_player_name': self.top_away_player_name,
            'top_away_player_photo_URL': self.top_away_player_photo_URL
        }

    def __repr__(self):
        return f"<Game {self.game_id}>"



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
    last_10_games_wins = Column(Integer, nullable=True)
    last_10_games_losses = Column(Integer, nullable=True)
    last_10_games_points = Column(Integer, nullable=True)
    last_10_games_assists = Column(Integer, nullable=True)
    last_10_games_minutes = Column(Float, nullable=True)
    last_10_games_shots_acc = Column(Float, nullable=True)

    is_active = Column(Boolean, nullable=False)





