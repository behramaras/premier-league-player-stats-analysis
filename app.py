import streamlit as st
import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("clean_players.csv")

# App title
st.title("⚽ Premier League Player Stats Explorer (2024-2025)")

# --- PLAYER SEARCH SECTION ---
# Text input for searching a player by name (case insensitive)
search = st.text_input("Search for a player:")

# Filter the dataframe to show only players matching the search term
filtered = df[df['player_name'].str.contains(search, case=False, na=False)]

# Display a simple table with key player stats
st.dataframe(filtered[['player_name', 'team', 'position', 'goals', 'assists']])

# --- PLAYER DETAIL SECTION ---
# Dropdown (selectbox) to choose a player from the filtered list
player = st.selectbox("Select a player to view details", filtered['player_name'])

# Retrieve the full data row for the selected player
player_data = df[df['player_name'] == player]

# Display the detailed stats for the selected player
st.write("### Player Details")
st.write(player_data)

# --- PLAYER COMPARISON SECTION ---
# Allow the user to choose two players to compare
st.subheader("Player Comparison")

# Dropdown menus for selecting two players to compare
player1 = st.selectbox("Compare Player 1", df['player_name'])
player2 = st.selectbox("Compare Player 2", df['player_name'])

# If the same player is selected twice, show a warning message
if player1 == player2:
    st.warning("⚠️ Please select two different players to compare.")
else:
    # Filter the DataFrame to include only the two selected players
    compare = df[df['player_name'].isin([player1, player2])]
    
    # Ensure the bar chart displays players in the same order as selected
    compare['player_name'] = pd.Categorical(
        compare['player_name'], 
        categories=[player1, player2], 
        ordered=True
    )
    compare = compare.sort_values('player_name')

    # Display a bar chart comparing goals, assists, and expected goals
    st.bar_chart(compare.set_index('player_name')[['goals', 'assists', 'expected_goals']])
