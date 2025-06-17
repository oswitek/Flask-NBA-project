from database_api_connection import get_all_players_from_db
import pandas as pd
import plotly.graph_objects as go

def draw_all_players_distribution(distribution_type, plot_type, active_status=None):
    all_players_data, _ = get_all_players_from_db()

    active_status_labels = {
        True: 'aktywnych',
        False: 'emerytowanych',
        None: 'wszystkich'
    }

    active_status_text = active_status_labels[active_status]

    match distribution_type:
        case 'country':
            players_countries_list = []

            for player in all_players_data:
                if (active_status is True or active_status is False) and player.is_active == active_status and player.country is not None:
                    players_countries_list.append(player.country)
                elif active_status is None and player.country is not None:
                    players_countries_list.append(player.country)

            players_countries = pd.Series(players_countries_list).value_counts().sort_values(ascending=False)

            if plot_type == 'pie':
                fig = go.Figure(
                    data=[go.Pie(
                    labels=players_countries.index,
                    values=players_countries.values,
                    hole=0.2,
                    textinfo='label',
                    textposition='inside',
                    hoverinfo='label+percent+value',
                    insidetextorientation='radial',
                    insidetextfont=dict(size=14),
                )]
                )
                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg kraju',
                    width=1200,
                    height=1200,
                    title_font_size=50,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html

            elif plot_type == 'bar':
                bar_legend = []
                for country, value in zip(players_countries.index, players_countries.values):
                    bar_legend.append(go.Bar(
                        name=country,
                        x=[country],
                        y=[value],
                    ))

                fig = go.Figure(
                    data=bar_legend,
                )

                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg kraju',
                    xaxis_title='Kraj',
                    yaxis_title='Liczba graczy',
                    width=1400,
                    height=1000,
                    title_font_size=25,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html

        case 'position':
            players_positions_list = []
            for player in all_players_data:
                if (active_status is True or active_status is False) and player.is_active == active_status and player.position is not None:
                    players_positions_list.append(player.position)
                elif active_status is None and player.position is not None:
                    players_positions_list.append(player.position)

            players_positions = pd.Series(players_positions_list).value_counts().sort_values(ascending=False)

            if plot_type == 'pie':
                fig = go.Figure(data=[go.Pie(
                    labels=players_positions.index,
                    values=players_positions.values,
                    hoverinfo='label+percent+value',
                    textinfo='label+percent',
                    textposition='inside',
                    hole=0.2,
                    insidetextorientation='radial',
                    insidetextfont=dict(size=14),
                    )]
                )

                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg pozycji',
                    width=1000,
                    height=1000,
                    title_font_size=25,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html

            elif plot_type == 'bar':
                bar_legend = []
                for position, value in zip(players_positions.index, players_positions.values):
                    bar_legend.append(go.Bar(
                        name=position,
                        x=[position],
                        y=[value],
                    ))

                fig = go.Figure(
                    data=bar_legend,
                )

                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg pozycji',
                    width=1000,
                    height=1000,
                    title_font_size=25,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html

        case 'height':
            players_heights_list = []
            for player in all_players_data:
                if (active_status is True or active_status is False) and player.is_active == active_status and player.height is not None:
                    players_heights_list.append(int(round(player.height, 0)))
                elif active_status is None and player.height is not None:
                    players_heights_list.append(int(round(player.height, 0)))

            players_heights = pd.Series(players_heights_list).value_counts().sort_values(ascending=False)

            if plot_type == 'pie':
                fig = go.Figure(data=[go.Pie(
                    labels=players_heights.index,
                    values=players_heights.values,
                    hoverinfo='label+percent+value',
                    textinfo='label+percent',
                    textposition='inside',
                    hole=0.2,
                )])

                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg wzrostu w centymetrach',
                    width=1000,
                    height=1000,
                    title_font_size=25,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html

            elif plot_type == 'bar':
                bar_legend = []
                for height, value in zip(players_heights.index, players_heights.values):
                    bar_legend.append(go.Bar(
                        name=f'{height} cm',
                        x=[height],
                        y=[value],
                    ))

                fig = go.Figure(
                    data=bar_legend,
                )

                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg wzrostu w centymetrach',
                    width=1000,
                    height=1000,
                    title_font_size=25,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html

        case 'weight':
            players_weights_list = []
            for player in all_players_data:
                if (active_status is True or active_status is False) and player.weight is not None:
                    players_weights_list.append(int(round(player.weight, 0)))
                elif active_status is None and player.weight is not None:
                    players_weights_list.append(int(round(player.weight, 0)))

            players_weights = pd.Series(players_weights_list).value_counts().sort_values(ascending=False)

            if plot_type == 'pie':
                fig = go.Figure(data=[go.Pie(
                    labels=players_weights.index,
                    values=players_weights.values,
                    hoverinfo='label+percent+value',
                    textinfo='label+percent',
                    textposition='inside',
                    hole=0.1,
                    )]
                )

                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg wagi w kilogramach',
                    width=1000,
                    height=1000,
                    title_font_size=25,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html

            if plot_type == 'bar':
                bar_legend = []
                for weight, value in zip(players_weights.index, players_weights.values):
                    bar_legend.append(go.Bar(
                        name=f'{weight} kg',
                        x=[weight],
                        y=[value],
                    ))

                fig = go.Figure(
                    data=bar_legend,
                )

                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg wagi w kilogramach',
                    width=1000,
                    height=1000,
                    title_font_size=25,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html

        case 'teams':
            players_teams_list = []
            for player in all_players_data:
                if (active_status is True or active_status is False) and player.current_team is not None:
                    players_teams_list.append(player.current_team)
                elif active_status is None and player.current_team is not None:
                    players_teams_list.append(player.current_team)

            players_teams = pd.Series(players_teams_list).value_counts().sort_values(ascending=False)

            if plot_type == 'pie':
                fig = go.Figure(data=[go.Pie(
                    labels=players_teams.index,
                    values=players_teams.values,
                    hoverinfo='label+percent+value',
                    textinfo='label+percent',
                    textposition='inside',
                    hole=0.1,
                )])

                fig.update_layout(
                    title=f'Dystrybucja {active_status_text} graczy wg drużyn',
                    width=1000,
                    height=1000,
                    title_font_size=25,
                )

                plot_html = fig.to_html(full_html=False)

                return plot_html



# def draw_player_stats(distribution_type, plot_type):




