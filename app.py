import streamlit as st
import pandas as pd
import altair as alt

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
filtered = df[df['player_name'].str.contains(search, case=False, na=False,regex=False)]

# Display a simple table with key player stats
st.dataframe(filtered.sort_values('player_name')[['player_name', 'team', 'position', 'goals', 'assists']], hide_index=True)

# --- TOP 10 GOAL CONTRIBUTORS SECTION ---
# Group data first (to merge players with multiple team entries)
df_grouped = (df.groupby("player_name", as_index=False)
            .agg({
        "goals": "sum",
        "assists": "sum",
        "goals_assists_total": "sum",
})
)

st.write("### 🏆 Top 10 Goal Contributors")

# Show top 10 players by total goal contributions
st.dataframe(df_grouped.nlargest(10, "goals_assists_total"), hide_index=True)

# --- PLAYER DETAIL SECTION ---
# Dropdown (selectbox) to choose a player from the filtered list
st.write("### Player Details")
player = st.selectbox("Select a player to view details", sorted(df['player_name']))

# Retrieve the full data row for the selected player
player_data = df[df['player_name'] == player]

# Display the detailed stats for the selected player
st.dataframe(player_data.reset_index(drop=True), hide_index=True)

# --- PLAYER COMPARISON SECTION ---
st.subheader("Player Comparison")

# Group players by both name and team to handle mid-season transfers
df_grouped2 = (
    df.groupby(["player_name", "team"], as_index=False)
    .agg({
        "goals": "sum",
        "assists": "sum",
        "expected_goals": "sum"
    })
)

# Identify players who have played for more than one team
duplicate_players = df_grouped2[df_grouped2.duplicated("player_name", keep=False)]["player_name"].unique()

# Create a TOTAL row that sums up all stats for each duplicate player
totals = (
    df_grouped2[df_grouped2["player_name"].isin(duplicate_players)]
    .groupby("player_name", as_index=False)
    .agg({
        "goals": "sum",
        "assists": "sum",
        "expected_goals": "sum"
    })
)
totals["team"] = "TOTAL"

# Combine team-level stats and total-level stats
df_grouped2 = pd.concat([df_grouped2, totals], ignore_index=True)

# Create a combined label for dropdowns (e.g., "James Ward-Prowse (West Ham)")
df_grouped2["player_label"] = df_grouped2["player_name"] + " (" + df_grouped2["team"] + ")"

# Sort all player labels alphabetically for cleaner dropdowns
player_labels = sorted(df_grouped2["player_label"])

# Create dropdown menus for selecting two players to compare
player1_label = st.selectbox("Compare Player 1", player_labels)
player2_label = st.selectbox("Compare Player 2", player_labels)

# Prevent user from comparing the same player-team combination
if player1_label == player2_label:
    st.warning("⚠️ Please select two different players to compare.")
else:
    # Filter DataFrame to include only the two selected players
    compare = df_grouped2[df_grouped2["player_label"].isin([player1_label, player2_label])].copy()

    # Maintain dropdown order in the chart for consistency
    compare["player_label"] = pd.Categorical(
        compare["player_label"],
        categories=[player1_label, player2_label],
        ordered=True
    )
    compare = compare.sort_values("player_label")

    # Set player label as index and plot comparison chart
    compare = compare.set_index("player_label")
    st.bar_chart(compare[["goals", "assists", "expected_goals"]])


st.caption("Created by Behram Aras")
