import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Premier League Player Stats Explorer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS style injection
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
            color: #1C1C1E !important;
        }

        [data-testid="stHeader"] {
            background: #3F1052 !important;
        }

        [data-testid="stSidebar"] {
            background-color: #F2F2F7 !important;
        }

        h1, h2, h3 {
            color: #3F1052 !important;
        }

        .stDataFrame {
            background-color: #F2F2F7 !important;
            border-radius: 10px !important;
            padding: 8px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- TABLE INFORMATION SECTION ---
with st.expander("ℹ️ How to Use & Column Descriptions"):
    st.markdown("""
    **🔍 How to Use the Table:**
    - Click any **column header** to sort the table by that statistic.  
      For example, click **Goals** to sort players by goal count.  
    - Use the **search bar** to find a specific player by name.  
    - Scroll horizontally or vertically to explore all player stats.

    **📊 Column Descriptions:**
    | Column | Description |
    |:--|:--|
    | `player_name` | The player’s full name |
    | `team` | The club the player belongs to |
    | `position` | The player’s on-field position (DF, MF, FW, GK) |
    | `goals` | Total goals scored |
    | `assists` | Total assists made |
    | `expected_goals (xG)` | Expected goals metric |
    | `expected_assists (xAG)` | Expected assists metric |
    | `minutes_played` | Total minutes played in the season |
    | `matches_played` | Number of matches played |
    | `age` | The player’s age |
    """)

# Load the cleaned dataset
df = pd.read_csv("clean_players.csv")

# App title
st.title("⚽ Premier League Player Stats Explorer (2024-2025)")

# --- PLAYER SEARCH SECTION ---
# Text input for searching a player by name (case insensitive)
search = st.text_input("Search for a player:", placeholder="Enter here!")

# Filter the dataframe to show only players matching the search term
filtered = df[df['player_name'].str.contains(search, case=False, na=False)]

# Display a simple table with key player stats
st.dataframe(filtered[['player_name', 'team', 'position', 'goals', 'assists']], hide_index=True)

# --- PLAYER DETAIL SECTION ---
# Dropdown (selectbox) to choose a player from the filtered list
st.write("### Player Details")
player = st.selectbox("Select a player to view details", filtered['player_name'])

# Retrieve the full data row for the selected player
player_data = df[df['player_name'] == player]

# Display the detailed stats for the selected player
st.dataframe(player_data.reset_index(drop=True), hide_index=True)

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

st.caption("Created by Behram Aras")
