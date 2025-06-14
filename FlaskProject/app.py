from flask import Flask, render_template, request
from database_api_connection import *
from database_api_connection import search_players_by_name
from datetime import datetime

app = Flask(__name__)
#create_tables()


@app.route('/')
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')
    today_games = None

    try:
        today_games = fetch_today_games_to_db(today_date)
    except Exception as e:
        print("Wystąpił błąd przy fetch_today_games_to_db", e)

    return render_template('index.html', games=today_games)


@app.route('/players')
def players():
    return render_template('players.html')


@app.route('/players/search')
def players_search():
    player_name = request.args.get('player_name', '')
    players = None
    
    if player_name:
        try:
            players = search_players_by_name(player_name)
        except Exception as e:
            print(f"Błąd podczas wyszukiwania gracza: {e}")
    
    return render_template('players.html', players=players, player_name=player_name)


if __name__ == '__main__':
    app.run(debug=True, port=8000)