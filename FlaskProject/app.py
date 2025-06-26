from flask import Flask, render_template, request, Response
from database_api_connection import *
from database_api_connection import search_players_by_name
from datetime import datetime
from plot_functions import *

app = Flask(__name__)
#create_tables()


@app.route('/')
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')
    today_games = []
    last_5_games = []

    try:
        fetch_today_games_to_db(today_date)
        today_games, last_5_games = get_today_games_from_db(today_date)
    except Exception as e:
        print("Wystąpił błąd przy fetch_today_games_to_db", e)

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)