from flask import Flask, render_template, request, Response
from database_api_connection import *
from database_api_connection import search_players_by_name
from datetime import datetime
from database_tables import AllGames, PlayerStats
from sqlalchemy.orm import aliased
from datetime import date
from plot_functions import *

app = Flask(__name__)
#create_tables()


@app.route('/')
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')
    today_games = None
    last_5_games = None

    try:
        today_games, last_5_games = get_today_games_from_db(today_date)
    except Exception as e:
        print("Wystąpił błąd przy get_today_games_from_db", e)

    return render_template('index.html', games=today_games, last_games=last_5_games)


@app.route('/players')
def players():
    return render_template('players-search.html')


@app.route('/players/search')
def players_search():
    player_name = request.args.get('player_name', '')
    players = None
    
    if player_name:
        try:
            players = search_players_by_name(player_name)
        except Exception as e:
            print(f"Błąd podczas wyszukiwania gracza: {e}")
    
    return render_template('players-search.html', players=players, player_name=player_name)


@app.route('/players/charts', methods=['GET', 'POST'])
def players_charts():

    distribution_type = request.args.get('distribution_type', 'teams') 
    
    plot_type = request.args.get('plot_type', 'pie')
    
    active_status_str = request.args.get('active_status', 'None')

    if active_status_str == 'true':
        active_status = True
    elif active_status_str == 'false':
        active_status = False
    else:
        active_status = None 

    plot_html, csv_file = draw_all_players_distribution(distribution_type, plot_type, active_status)

    if request.args.get('download_csv'):
        return Response(
            csv_file,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{distribution_type}-{active_status}.csv"'},
        )
    
    return render_template(
        'players-charts.html', 
        plot_html=plot_html,
        selected_distribution_type=distribution_type,
        selected_plot_type=plot_type,
        selected_active_status=active_status_str,
    )

@app.route('/teams')
def show_teams():
    teams = get_all_teams()
    return render_template('teams.html', teams=teams)

SEASONS = {
    "2019-20": (date(2019, 8, 1), date(2020, 8, 1)),
    "2020-21": (date(2020, 8, 1), date(2021, 8, 1)),
    "2021-22": (date(2021, 8, 1), date(2022, 8, 1)),
    "2022-23": (date(2022, 8, 1), date(2023, 8, 1)),
    "2023-24": (date(2023, 8, 1), date(2024, 8, 1)),
    "2024-25": (date(2024, 10, 1), date(2025, 6, 30)),
}


@app.route('/team/<int:team_id>')
def show_team_latest_games(team_id):
    TEAM_NAMES = {
    "ATL": "Atlanta Hawks",
    "BOS": "Boston Celtics",
    "BKN": "Brooklyn Nets",
    "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "Los Angeles Clippers",
    "LAL": "Los Angeles Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHX": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "WAS": "Washington Wizards"
}
    session = Session()

    season = request.args.get("season", "2024-25")
    start_date, end_date = SEASONS.get(season, SEASONS["2023-24"])

    try:
        current_page = int(request.args.get("page", 1))
        if current_page < 1:
            current_page = 1
    except ValueError:
        current_page = 1

    per_page = 10

    sort_option = request.args.get("sort", "date_desc")
    Opponent = aliased(AllGames)

    if sort_option == "date_asc":
        sort_column = AllGames.game_date.asc()
    elif sort_option == "pts_asc":
        sort_column = AllGames.pts.asc()
    elif sort_option == "pts_desc":
        sort_column = AllGames.pts.desc()
    elif sort_option == "opp_asc":
        sort_column = Opponent.pts.asc()
    elif sort_option == "opp_desc":
        sort_column = Opponent.pts.desc()
    else:
        sort_column = AllGames.game_date.desc()

    total_games = session.query(AllGames).filter(
        AllGames.team_id == team_id,
        AllGames.game_date >= start_date,
        AllGames.game_date < end_date
    ).count()

    total_pages = (total_games + per_page - 1) // per_page

    raw_games = (
        session.query(
            AllGames,
            Opponent.pts.label("opp_pts")
        )
        .join(
            Opponent,
            (AllGames.game_id == Opponent.game_id) &
            (AllGames.team_id != Opponent.team_id)
        )
        .filter(
            AllGames.team_id == team_id,
            AllGames.game_date >= start_date,
            AllGames.game_date < end_date
        )
        .order_by(sort_column)
        .offset((current_page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    games = []
    for game, opp_pts in raw_games:
        mvp = (
            session.query(PlayerStats)
            .filter(PlayerStats.game_id == game.game_id)
            .order_by(PlayerStats.pts.desc())
            .first()
        )
        games.append({
            "game": game,
            "opp_pts": opp_pts,
            "mvp": mvp
        })
    team_logos = get_team_logos()
    session.close()
    
    return render_template(
        "team_latest_games.html",
        games=games,
        team_id=team_id,
        team_logos=team_logos,
        selected_season=season,
        seasons=SEASONS.keys(),
        current_page=current_page,
        total_pages=total_pages,
        per_page=per_page,
        team_names=TEAM_NAMES  
    )

if __name__ == '__main__':
    app.run(debug=True, port=8000)