from flask import Flask, render_template, request
from database_api_connection import *
from datetime import datetime

app = Flask(__name__)
create_tables()


@app.route('/')
def index():

    #fetch_all_players_to_db()
    #today_date = datetime.today().strftime('%Y-%m-%d')
    today_date = '2025-05-18'

    get_all_players_from_db()

    #fetch_today_games_to_db(today_date)
    today_games = get_today_games_from_db(today_date)
    for game in today_games:
        print(game.to_dict())

    return render_template('index.html', games=today_games)

if __name__ == '__main__':
    app.run(debug=True, port=8000)