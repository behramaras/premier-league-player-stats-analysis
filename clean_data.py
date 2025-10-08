import pandas as pd 

# Load the raw CSV file
df = pd.read_csv("players.csv")

# Select only the relevant columns from the dataset
columns = [
    'Unnamed: 1_level_0 Player', 'Unnamed: 2_level_0 Nation',
    'Unnamed: 3_level_0 Pos', 'Unnamed: 4_level_0 Squad',
    'Unnamed: 5_level_0 Age', 'Playing Time MP',
    'Playing Time Min', 'Performance Gls', 'Performance Ast',
    'Performance G+A', 'Expected xG',
    'Expected xAG', 'Expected npxG+xAG'
]

df = df[columns]

# Rename columns to more readable and standardized names
df.rename(columns={
    'Unnamed: 1_level_0 Player': 'player_name',     # the player's full name
    'Unnamed: 2_level_0 Nation': 'nationality',     # the player's nationality (country code)
    'Unnamed: 3_level_0 Pos': 'position',           # the player's position (e.g., FW, MF, DF, GK)
    'Unnamed: 4_level_0 Squad': 'team',             # the club/team the player belongs to
    'Unnamed: 5_level_0 Age': 'age',                # the player's age
    'Playing Time MP': 'matches_played',            # number of matches the player has played
    'Playing Time Min': 'minutes_played',           # total minutes played in the season
    'Performance Gls': 'goals',                     # total goals scored
    'Performance Ast': 'assists',                   # total assists made
    'Performance G+A': 'goals_assists_total',       # total goals + assists combined
    'Expected xG': 'expected_goals',                # expected goals (xG)
    'Expected xAG': 'expected_assists',             # expected assists (xAG)
    'Expected npxG+xAG': 'expected_npxG_plus_xAG'   # non-penalty expected goals + expected assists
}, inplace=True)

# Define invalid values that represent repeated headers or unwanted text rows
invalid_values = [
    'player_name', 'nationality', 'position', 'team', 'age',
    'matches_played', 'minutes_played', 'goals', 'assists',
    'goals_assists_total', 'expected_goals', 'expected_assists',
    'expected_npxG_plus_xAG',
    'Player', 'Nation', 'Pos', 'Squad', 'Age',
    'MP', 'Min', 'Gls', 'Ast', 'G+A', 'xG', 'xAG', 'npxG+xAG',
]

# Remove any rows where *any* cell matches one of the invalid values above
# The tilde (~) negates the boolean mask, so only valid rows are kept
df = df[~df.apply(lambda row: any(val in str(cell) for cell in row for val in invalid_values), axis=1)]

# Convert numeric columns from strings to proper numeric (float/int) types
numeric_cols = [
    'age', 'matches_played', 'minutes_played',
    'goals', 'assists', 'goals_assists_total',
    'expected_goals', 'expected_assists', 'expected_npxG_plus_xAG'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # convert invalid entries to NaN

df['nationality'] = df['nationality'].apply(lambda x: x.split(' ')[-1] if isinstance(x, str) and ' ' in x else x)

# Save the cleaned dataset to a new CSV file
df.to_csv("clean_players.csv", index=False)
