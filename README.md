# FLASK NBA project

## Overview 
This project focuses on delivering enhanced, real-time NBA data by presenting live game updates, team season statistics, and player distributions through an interactive web interface. Designed for data analysts, it features custom data pipelines that retrieve information from the NBA API, then clean and normalize the data, and store it in a PostgreSQL database in the end. Users can search for specific players to view detailed information, while interactive charts built with Plotly allow user to select and manipulate which data ditribution they want to analyse.

## Main features
- Retrieving information about NBA players, teams and games via nba_api
- Backend processing and analytics with NumPy and pandas
- Cloud-hosted PostgreSQL database for efficient data storage and management
- Integration between nba_api and PostgreSQL database
- Interactive visualizations of player distributions f.e. by height, weight or country with customizable plot types and career activity filters
- Search functionality to quickly find detailed information about specific players or teams

## Usage
To use this app follow these steps
1. Activate virtual enviroment and install all required dependencies by running commands in the project's terminal:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
2. Simply run the app by typing in the project's terminal:
```
flask run
```
3. Go to your web browser and enter:
```
http://127.0.0.1:8000/
```
4. Just explore and enjoy :)
