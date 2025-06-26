# FLASK NBA project

## Overview 
This project focuses on delivering enhanced, real-time NBA data by presenting live game updates, team season statistics, and player distributions through an interactive web interface. Designed for data analysts, it features custom data pipelines that retrieve information from the `NBA API`, then clean and normalize the data, and store it in a `PostgreSQL` database in the end. Users can search for specific players to view detailed information, while interactive charts built with `Plotly` allow user to select and manipulate which data ditribution they want to analyse.

## Main Features
- Retrieving information about NBA players, teams and games via `nba_api`
- Backend processing and analytics with `NumPy` and `pandas`
- Cloud-hosted `PostgreSQL` database for efficient data storage and management
- Integration between `nba_api` and `PostgreSQL` database
- Interactive visualizations of player distributions f.e. by height, weight or country with customizable plot types and career activity filters made with `Plotly`
- Search functionality to quickly find detailed information about specific players or teams

## ETL Data Pipeline
- **Live Data**: Real-time data retrieved from `nba_api`
- **Data Processing**: Cleaning and transformation with `pandas` and `NumPy`
- **Cloud Database**: PostgreSQL hosted on Render

## Live Demo
You can preview the app at:  
`https://flask-nba.onrender.com/`
