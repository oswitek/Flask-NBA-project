from nba_api.stats import endpoints
from nba_api.stats.static import teams, players
from nba_api.live.nba.endpoints import odds as team_odds
from flask import Flask, render_template, request
from datetime import datetime
import time
from pytz import timezone

app = Flask(__name__)


@app.route('/')
def index():

    today_date = datetime.today().strftime('%Y-%m-%d')
    #today_date = "2025-05-18" #Testowo jak chcecie sobie sprawdzić jakiś dzień to zakomentujcie linijkę wyżej i wpiszcie datę tutaj i odkomentujcie to -> ctr-s i reload stronki
    scoreboard = endpoints.ScoreboardV2(game_date=today_date) #W game[4] pamietajcie ze jest zwracany format STRING a nie datetime
    today_games = scoreboard.game_header.get_dict()['data']
    #print(today_games)

    odds = team_odds.Odds()
    odds_games = odds.get_games().get_dict()

    today_games_list = []

    all_players = endpoints.LeagueDashPlayerStats().get_data_frames()[0]
    #print(all_players)

    #Dla każdej gry w grach rozgrywanych danego dnia pobieramy ID meczu, id drużyn, loga drużyn oraz typujemy najlepszych graczy i oddsy bukmacherów na daną drużynę.
    for game in today_games:
        game_status_id = game[3]  # gdzie jest status 1 = scheduled 2 = trwa 3 = end
        home_team_id = game[6]
        home_team_logo = "https://cdn.nba.com/logos/nba/{}/global/L/logo.svg".format(home_team_id) #loga z osobnej stronki (W pelni sie zgadzają z ID druzyn nba_api) bo w api nie bylo log
        away_team_id = game[7]
        away_team_logo = "https://cdn.nba.com/logos/nba/{}/global/L/logo.svg".format(away_team_id)
        game_place = game[15]

        #Do obliczenia czy gra sie jeszcze nie zaczela / trwa / koniec
        if game_status_id == 1:
            game_time = "Planned: {}".format(game[4])  #zaplanowany
        elif game_status_id == 2: #trwa
            us_eastern_timezone = timezone('US/Eastern')
            current_time = datetime.now(us_eastern_timezone)
            game_time_string = game[4].replace("ET", "").strip()
            game_time_datetime = datetime.strptime(game_time_string, "%I:%M %p")

            game_start_date = datetime(
                current_time.year, current_time.month, current_time.day,
                game_time_datetime.hour, game_time_datetime.minute
            )

            game_start_time = us_eastern_timezone.localize(game_start_date)
            game_time_elapsed = current_time - game_start_time
            game_time = "Ongoing: {}".format(game_time_elapsed)
        else:
            game_time = "End of the match"

        #print(game_time)

        home_team_name = teams.find_team_name_by_id(home_team_id)['full_name']
        away_team_name = teams.find_team_name_by_id(away_team_id)['full_name']

        #Trzeba bylo dodać żeby tylko 8 najlepszych przeliczalo bo za duzo zapytan przy zawodnikach z całej drużyny i wysypuje (bierzemy se pod uwage tylko 8 zawodników z najwiekszym czasem gry w minutach - taki core zespołu)
        top_home_players = all_players[all_players['TEAM_ID'] == home_team_id].sort_values(by=['MIN'], ascending=False).head(8)
        top_away_players = all_players[all_players['TEAM_ID'] == away_team_id].sort_values(by=['MIN'], ascending=False).head(8)

        best_home_player = None
        best_away_player = None
        most_home_points = 0
        most_away_points = 0

        for player_id in top_home_players['PLAYER_ID']:
            player_last_10_games = endpoints.playergamelog.PlayerGameLog(player_id=player_id, season=game[8]).get_data_frames()[0].head(10)
            current_points = player_last_10_games['PTS'].sum()
            if current_points > most_home_points:
                most_home_points = current_points
                points_per_game = most_home_points / len(player_last_10_games)
                player_name = top_home_players.loc[top_home_players['PLAYER_ID'] == player_id]['PLAYER_NAME'].iloc[0]
                player_photo = "https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(player_id)
                best_home_player = {
                    'player_name' : player_name,
                    'player_photo': player_photo,
                    'points_per_game' : points_per_game,
                }
            time.sleep(0.4)

        for player_id in top_away_players['PLAYER_ID']:
            player_last_10_games = endpoints.playergamelog.PlayerGameLog(player_id=player_id, season=game[8]).get_data_frames()[0].head(10)
            current_points = player_last_10_games['PTS'].sum()
            if current_points > most_away_points:
                most_away_points = current_points
                points_per_game = most_away_points / len(player_last_10_games)
                player_name = top_away_players.loc[top_away_players['PLAYER_ID'] == player_id]['PLAYER_NAME'].iloc[0]
                player_photo = "https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(player_id)
                best_away_player = {
                    'player_name': player_name,
                    'player_photo': player_photo,
                    'points_per_game': points_per_game,
                }
            time.sleep(0.4)

        #print(best_home_player)
        #print(best_away_player)

        #Każdy 1 mecz ma taką postać
        game_data = {
            'home_team_logo': home_team_logo,
            'home_team': home_team_name,
            'best_home_player': best_home_player,
            'away_team_logo': away_team_logo,
            'away_team': away_team_name,
            'best_away_player': best_away_player,
            'game_time': game_time,
            'game_place': game_place,
            'odds': None
        }

        #Match oddsy dla każdej drużyny
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
        time.sleep(0.4)


    return render_template('index.html', today_games_html=today_games_list)

@app.route('/players', methods=['GET'])
def players_search():
    player_name = request.args.get('player_name', '')
    #player_name = "Jordan"

    found_players_by_name = []
    players_list = []

    if player_name:
        found_players_by_name = players.find_players_by_full_name(player_name)

        for searched_player in found_players_by_name:
            player_id = searched_player['id']
            player_full_name = searched_player['full_name']
            stats = endpoints.PlayerCareerStats(player_id=player_id)
            career_df = stats.get_data_frames()[0]

            if not career_df.empty:
                latest_known_season = career_df.iloc[-1]
                players_list.append({
                    'name': player_full_name,
                    'player_id': player_id,
                    'team': latest_known_season['TEAM_ABBREVIATION'],
                    'season': latest_known_season['SEASON_ID'],
                    'games': latest_known_season['GP'],
                    'points': latest_known_season['PTS'],
                    'rebounds': latest_known_season['REB'],
                    'assists': latest_known_season['AST'],
                    'photo': "https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(player_id)
                })
            time.sleep(0.4)

    return render_template('players.html', players=players_list, player_name=player_name)


if __name__ == '__main__':
    app.run(debug=True, port=8000)