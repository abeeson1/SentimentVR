from google.cloud import bigquery
import bq_helper  # Helper functions for putting BigQuery results in Pandas DataFrames https://github.com/SohierDane/BigQuery_Helper
from pandas import DataFrame
import secret_data

#https://google-auth.readthedocs.io/en/latest/user-guide.html#service-account-private-key-files

client = bigquery.Client(project=secret_data.PROJECT_ID)

ncaa_basketball = bq_helper.BigQueryHelper(active_project="bigquery-public-data", dataset_name="ncaa_basketball")

# List of all the tables in the ncaa_basketball dataset
tables = ncaa_basketball.list_tables()


#TWO REQUIRED DATASETS
#mbb_historical_teams_seasons
#mbb_teams

# Query of All Data from Teams Games
old_query = """SELECT * 
            FROM `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr`"""

old_query2 = """
    SELECT 
        team_code,
        season,
        market, 
        name, 
        alias, 
        current_division, 
        wins, 
        losses,
        ties,
        (wins / losses) AS pct
    FROM 
        `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons`
    WHERE 
        2013 = season;
"""

old_query3 = """
    SELECT 
        season,
        round,
        win_seed,
        win_market,
        win_name,
        win_alias,
        win_school_ncaa,
        win_pts,
        lose_seed,
        lose_market,
        lose_name,
        lose_school_ncaa,
        lose_pts
    FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games` as teams_tournament
    WHERE 2013 = season;
"""

query = """
    SELECT 
        *
    FROM `bigquery-public-data.ncaa_basketball.mbb_games_sr` as teams_game
    WHERE teams_game.season = 2017
    AND teams_game.tournament = 'NCAA'
    AND teams_game.tournament_type IN ('South Regional', 'West Regional', 'National Championship','East Regional','First Four','Midwest Regional','Final Four');
"""

df = ncaa_basketball.query_to_pandas_safe(query, max_gb_scanned=1)

#Convert Columns to 10 pt Scale
'''
WinPts = df["win_pts"]
low = min(WinPts)
high = max(WinPts)
WinPts_inds = [float(10*(x-low)/(high-low)) for x in WinPts] #gives items a value from 0-10

print(WinPts_inds)
'''


df.to_csv(r'generated_data/'+'2017_season_detailed'+'.csv')



