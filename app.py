import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# ---------------------------
# --- UTILITY FUNCTIONS -----
# ---------------------------

def configure_aggrid(df, height=600):
    """Common AgGrid configuration."""
    gb = GridOptionsBuilder.from_dataframe(df, hide_index=True)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(
        resizable=True,
        filter=True,
        sortable=True,
        floatingFilter=True
    )
    return gb.build()

def rename_columns(df, col_map):
    """Rename columns based on a mapping dictionary."""
    return df.rename(columns=col_map)

def display_aggrid(df, height=600):
    """Display a dataframe with AgGrid."""
    AgGrid(
        df,
        gridOptions=configure_aggrid(df, height),
        height=height,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        theme="balham"
    )

def filter_players(df, search_term, columns=None):
    """Filter players by search term and optional columns."""
    filtered = df[df['player_name'].str.contains(search_term, case=False, na=False, regex=False)]
    if columns:
        filtered = filtered[columns]
    return filtered

def top_contributors(df, n=10):
    """Display top N goal contributors."""
    grouped = df.groupby("player_name", as_index=False).agg({
        "goals": "sum",
        "assists": "sum",
        "goals_assists_total": "sum"
    }).rename(columns={
        'player_name': 'Name',
        'goals': 'Goals',
        'assists': 'Assists',
        'goals_assists_total': 'Goals + Assists'
    })
    top10 = grouped.nlargest(n, "Goals + Assists")
    display_aggrid(top10)

def prepare_comparison_df(df):
    """Prepare dataframe for player comparison."""
    grouped = df.groupby(["player_name","team"], as_index=False).agg({
        "goals":"sum","assists":"sum","expected_goals":"sum"
    })
    duplicates = grouped[grouped.duplicated("player_name", keep=False)]["player_name"].unique()
    totals = grouped[grouped["player_name"].isin(duplicates)].groupby("player_name", as_index=False).sum()
    totals["team"] = "TOTAL"
    combined = pd.concat([grouped, totals], ignore_index=True)
    combined["player_label"] = combined["player_name"] + " (" + combined["team"] + ")"
    return combined.sort_values("player_label")

# ---------------------------
# --- STREAMLIT PAGE SETUP ---
# ---------------------------

st.set_page_config(
    page_title="Premier League Player Stats Explorer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background-color:#FFFFFF;color:#1C1C1E;}
[data-testid="stHeader"] {background:#3F1052;}
[data-testid="stSidebar"] {background-color:#F2F2F7;}
h1,h2,h3 {color:#3F1052;}
.stDataFrame {background-color:#F2F2F7;border-radius:10px;padding:8px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# --- DATA LOAD -------------
# ---------------------------

df = pd.read_csv("clean_players.csv")

# ---------------------------
# --- APP TITLE -------------
# ---------------------------

st.title("⚽ Premier League Player Stats Explorer (2024-2025)")

# ---------------------------
# --- INFO SECTION ----------
# ---------------------------

with st.expander("ℹ️ How to Use & Column Descriptions"):
    st.markdown("""
    **🔍 How to Use the Table:**
    - Click any **column header** to sort the table by that statistic.
    - Use the **search bar** to find a specific player.
    - Scroll horizontally or vertically to explore all stats.
    - In **Player Comparison**, select two different players to visualize their stats side by side.

    **📊 Column Descriptions:**
    | Column | Description |
    |:--|:--|
    | `Name` | Player’s full name |
    | `Team` | Club the player belongs to |
    | `Position` | On-field position (DF, MF, FW, GK) |
    | `Goals` | Total goals scored |
    | `Assists` | Total assists |
    | `Goals + Assists` | Combined goal contributions |
    | `Expected Goals` | Expected goals metric |
    | `Expected Assists` | Expected assists metric |
    | `Minutes Played` | Total minutes played in the season |
    | `Matches Played` | Number of matches played |
    | `Age` | Player age |
    | `Nationality` | Player nationality |
    """)


# ---------------------------
# --- PLAYER SEARCH ----------
# ---------------------------

st.write("### 🔍 Player Search")
search_term = st.text_input("Search for a player:", placeholder="Enter player name...")

columns_to_display = ['player_name', 'team', 'position', 'goals', 'assists',
                      'minutes_played', 'matches_played', 'age']

filtered = filter_players(df, search_term, columns_to_display)
col_map = {
    'player_name':'Name','team':'Team','position':'Position','goals':'Goals',
    'assists':'Assists','minutes_played':'Minutes Played','matches_played':'Matches Played',
    'age':'Age'
}
display_df = rename_columns(filtered, col_map)
display_aggrid(display_df)

# ---------------------------
# --- TOP 10 CONTRIBUTORS ---
# ---------------------------

st.write("### 🏆 Top 10 Goal Contributors")
top_contributors(df)

# ---------------------------
# --- PLAYER DETAIL ---------
# ---------------------------

st.write("### Player Details")
player = st.selectbox("Select a player to view details", sorted(df['player_name']))

player_data = df[df['player_name'] == player]
col_map_detail = {
    'player_name': 'Name','nationality':'Nationality','position':'Position','age':'Age',
    'team':'Team','matches_played':'Matches Played','minutes_played':'Minutes Played',
    'goals':'Goals','assists':'Assists','goals_assists_total':'Goals + Assists',
    'expected_goals':'Expected Goals','expected_assists':'Expected Assists',
    'expected_npxG_plus_xAG': 'Expected (Goals + Assists)'
}
player_display = rename_columns(player_data, col_map_detail)
display_aggrid(player_display, height=250)

# ---------------------------
# --- PLAYER COMPARISON -----
# ---------------------------

st.subheader("Player Comparison")
comparison_df = prepare_comparison_df(df)

player_labels = sorted(comparison_df["player_label"])
player1_label = st.selectbox("Compare Player 1", player_labels)
player2_label = st.selectbox("Compare Player 2", player_labels)

if player1_label == player2_label:
    st.warning("⚠️ Please select two different players to compare.")
else:
    compare = comparison_df[comparison_df["player_label"].isin([player1_label, player2_label])]
    compare["player_label"] = pd.Categorical(compare["player_label"], categories=[player1_label, player2_label], ordered=True)
    compare = compare.sort_values("player_label").set_index("player_label")
    compare_display = compare[["goals","assists","expected_goals"]].rename(columns={
        "goals":"Goals","assists":"Assists","expected_goals":"Expected Goals"
    })
    st.bar_chart(compare_display)

st.caption("Created by Behram Aras")
