from nba_api.stats import endpoints
from nba_api.stats.static import teams
from nba_api.live.nba.endpoints import odds as team_odds
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')
    scoreboard = endpoints.ScoreboardV2(game_date=today_date)
    today_games = scoreboard.game_header.get_dict()['data']

    odds = team_odds.Odds()
    odds_games = odds.get_games().get_dict()

    today_games_list = []

    for game in today_games:
        game_status_id = game[3]  # gdzie jest status 1 = scheduled 2 = trwa 3 = end
        home_team_id = game[6]
        home_team_logo = "https://cdn.nba.com/logos/nba/{}/global/L/logo.svg".format(home_team_id) #loga z osobnej stronki (W pelni sie zgadzają z ID druzyn nba_api) bo w api nie bylo log
        away_team_id = game[7]
        away_team_logo = "https://cdn.nba.com/logos/nba/{}/global/L/logo.svg".format(away_team_id)
        game_time = game[4] if game_status_id != 2 else None  # gra trwa to nie wliczać
        game_place = game[15]

        home_team_name = teams.find_team_name_by_id(home_team_id)['full_name']
        away_team_name = teams.find_team_name_by_id(away_team_id)['full_name']

        #Każdy 1 mecz ma taką postać
        game_data = {
            'home_team_logo': home_team_logo,
            'home_team': home_team_name,
            'away_team_logo': away_team_logo,
            'away_team': away_team_name,
            'game_time': game_time,
            'game_place': game_place,
            'odds': None
        }

        match_odds = next((g for g in odds_games if g['homeTeamId'] == str(home_team_id) and g['awayTeamId'] == str(away_team_id)), None)

        if match_odds:
            two_way_market = next((m for m in match_odds['markets'] if m['name'] == '2way'), None)

            if two_way_market and two_way_market['books']:
                booker = two_way_market['books'][0]
                outcomes_info = []
                for outcome in booker['outcomes']:
                    team_type = outcome['type']
                    team_name = home_team_name if team_type == 'home' else away_team_name
                    outcomes_info.append({
                        'team': team_name,
                        'odds': outcome['odds'],
                        'trend': outcome['odds_trend']
                    })

                game_data['odds'] = {
                    'booker_name': booker['name'],
                    'outcomes': outcomes_info
                }

        today_games_list.append(game_data)

        #Dodać jeszcze najlepszy gracz z najlepszym graczem porównanie z endpointa playervsplayer i trzeba też najlepszego gracza danego teamu wyszukać i porównywać między sobą np pod kątem kto ma więcej punktów zdobytych itp.

    return render_template('index.html', today_games_html=today_games_list)

#@app.route('/players')
#def players():
#
#    return render_template('players.html', )


if __name__ == '__main__':
    app.run(debug=True, port=8000)