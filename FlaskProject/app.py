from flask import Flask, render_template, request
from database_api_connection import *
from datetime import datetime

app = Flask(__name__)
#create_tables()


@app.route('/')
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')

    fetch_today_games_to_db(today_date)



    return render_template('index.html')#, games=today_games)

if __name__ == '__main__':
    app.run(debug=True, port=8000)