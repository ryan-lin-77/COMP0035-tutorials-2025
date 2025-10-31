""" Add data to the paralympics database.
This can only be used once you have completed activities 3.1 to 3.11
This is far more complex than you would be expected to create, or even need to use, for the coursework.
"""
import sqlite3
from importlib import resources

import pandas as pd

from activities.database_wk3 import data_solutions
from activities.database_wk3.solutions_db import create_db


def insert_data(db_path, df, table_name):
    """ Insert data into the tables that don't have primary keys """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table is empty
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    if row_count > 0:
        cursor.close()
        conn.close()
        print(f"Table {table_name} already has data. Skipping insert.")
        return

    # Get the column names from the tables, drop the 'id' column except for the team table
    cursor.execute(f"PRAGMA table_info({table_name});")
    cols_with_id = [row[1] for row in cursor.fetchall()]
    if table_name != "team":
        cols = cols_with_id[1:]
    else:
        cols = cols_with_id[0:-1]

    # Generate a placeholder for each col value in the parameterised query
    placeholders = ', '.join(['?'] * len(cols))

    # Generate the list of column names
    columns = ', '.join(cols)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    for _, row in df.iterrows():
        # Replace NaNs with None
        params = [
            None if pd.isna(row[col]) else row[col]
            for col in cols
        ]
        cursor.execute(sql, params)

    conn.commit()
    cursor.close()
    conn.close()


def insert_team_data(db_path, df):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    team_cols = get_column_names(db_path, "team")
    cols_to_use = team_cols[0:-1]  # drop the last column, country_id
    df.columns = cols_to_use  # reset the df columns to the revised names for the table
    insert_data(db_path, df, "team")
    replacement_names = {
        'Great Britain': 'UK',
        'United States of America': 'USA',
        'Republic of Korea': 'Korea',
        'Russian Federation': 'Russia',
        "People's Republic of China": 'China'
    }
    # For each row in the team table, if the value in team.name matches a value in country.country
    # then insert the country.id as team.country_id
    cursor.execute("SELECT * FROM team")
    rows = cursor.fetchall()
    for row in rows:
        # Find the country id where country.country matches team.name
        country_name = replacement_names.get(row[1], row[1])
        cursor.execute("SELECT id FROM country WHERE country = ?", (country_name,))
        result = cursor.fetchone()
        if result is not None:
            cursor.execute("UPDATE team SET country_id = ? WHERE code = ?", (result[0], row[0]))
    conn.commit()
    conn.close()


def insert_host_data(db_path, df):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the unique values for host
    host_values = pd.unique(df.host.dropna().str.split(',').explode().str.strip())

    # Iterate the rows in the games dataframe
    for host in host_values:
        # find the first row in the dataframe df where the host is contained in the string df['host']
        # df['host'] can have two values separated by a string
        row = df[df['host'].str.contains(rf'\b{host}\b', na=False)].iloc[0]
        country_names = [c.strip() for c in row.country.split(',')]
        for country_name in country_names:
            cursor.execute("SELECT id FROM country WHERE country = ?", (country_name,))
            result = cursor.fetchone()
            if result is not None:
                cursor.execute("INSERT INTO host (place_name, country_id) VALUES (?, ?)", (host, result[0]))
            else:
                print(f"Country '{country_name}' not found in country table. Skipping host '{host}'.")
    conn.commit()
    conn.close()


def insert_association_table_data(db_path, df):
    """ Insert data into the association tables: GamesTeam, GamesDisability and GamesHost """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for _, row in df.iterrows():
        # Find games.id where games.year + games.type matches the row['year'] + row['type']
        cursor.execute("SELECT id FROM games WHERE year = ? AND type = ?", (row['year'], row['type']))
        games_id_result = cursor.fetchone()
        if not games_id_result:
            continue
        games_id = games_id_result[0]

        # GamesHost: handle multiple hosts
        hosts = [h.strip() for h in str(row['host']).split(',') if h.strip()]
        for host in hosts:
            cursor.execute("SELECT id FROM host WHERE place_name = ?", (host,))
            host_id_result = cursor.fetchone()
            if host_id_result:
                host_id = host_id_result[0]
                cursor.execute("INSERT INTO gameshost (games_id, host_id) VALUES (?, ?)", (games_id, host_id))

        # GamesDisability: handle multiple disabilities
        disabilities = [d.strip() for d in str(row['disabilities_included']).split(',') if d.strip()]
        for disability in disabilities:
            cursor.execute("SELECT id FROM disability WHERE description = ?", (disability,))
            disability_id_result = cursor.fetchone()
            if disability_id_result:
                disability_id = disability_id_result[0]
                cursor.execute("INSERT INTO gamesdisability (games_id, disability_id) VALUES (?, ?)",
                               (games_id, disability_id))
    conn.commit()
    conn.close()


def delete_rows(db_path, table_names=None):
    """ Delete all rows from a table if specified, or all tables if not.

    Args:
        db_path: Path to the database
        table_names: List of table names to delete
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if not table_names:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        table_names = [row[0] for row in cur.fetchall()]
    for table_name in table_names:
        cur.execute(f"DELETE FROM {table_name}")  # Delete every row
    conn.commit()
    conn.close()


def get_column_names(db_path, table_name):
    """Return a list of column names for the specified table."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    cols = [row[1] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return cols


def create_dataframes(data_path):
    """ Reads the data from Excel into two dataframes and returns these

    Args:
        data_path (str): Path to the raw data file

    Returns:
        df_games, df_country_codes (tuple [pd.DataFrame, pd.DataFrame]): tuple of dataframes
    """
    # Games sheet
    dict_event_dtypes = {
        'type': 'string',
        'year': 'Int64',
        'country': 'string',
        'host': 'string',
        'start': 'string',
        'end': 'string',
        'disabilities_included': 'string',
        'countries': 'Int64',
        'events': 'Int64',
        'sports': 'Int64',
        'participants_m': 'Int64',
        'participants_f': 'Int64',
        'participants': 'Int64',
        'highlights': 'string',
        'URL': 'string'
    }
    df_games = pd.read_excel(data_path, sheet_name="games", dtype=dict_event_dtypes)
    # Clean the 'type' column
    df_games['type'] = df_games['type'].str.strip().str.lower()
    df_games = df_games[df_games['type'].isin(['winter', 'summer'])]
    # Country code sheet
    dict_code_dtypes = {
        'Code': 'string',
        'Name': 'string',
        'Region': 'string',
        'SubRegion': 'string',
        'MemberType': 'string',
        'Notes': 'string'
    }
    df_country_codes = pd.read_excel(data_path, sheet_name="team_codes", dtype=dict_code_dtypes)
    return df_games, df_country_codes


def main():
    db_path = resources.files(data_solutions).joinpath("paralympics.db")
    data_path = resources.files(data_solutions).joinpath("paralympics_all_raw.xlsx")
    schema_path = resources.files(data_solutions).joinpath("paralympics_schema.sql")
    create_db(schema_path=schema_path, db_path=db_path)
    df_games, df_codes = create_dataframes(data_path)
    # games data
    insert_data(db_path, df_games, "games")
    # disability data using the unique values from the disabilities_included column
    disability_values = pd.unique(df_games.disabilities_included.dropna().str.split(',').explode().str.strip())
    df_disabilities = pd.DataFrame({'description': disability_values})
    insert_data(db_path, df_disabilities, "disability")
    # country data, needs to be unique and split the values in the row that has both UK and USA in
    country_values = pd.unique(df_games.country.dropna().str.split(',').explode().str.strip())
    df_country = pd.DataFrame({'country': country_values})
    insert_data(db_path, df_country, "country")
    # team
    insert_team_data(db_path, df=df_codes)
    # Host
    delete_rows(db_path, ["host", ])
    insert_host_data(db_path, df_games)
    # gameshost, gamesdisability
    insert_association_table_data(db_path, df_games)


if __name__ == "__main__":
    main()
