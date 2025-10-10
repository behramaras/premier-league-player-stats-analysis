# Premier League Player Stats Explorer (2024–2025)

An interactive Streamlit web app to explore, compare, and analyze player performance data from the **Premier League 2024–25** season.  
Built with **Python**, **Streamlit**, and **Pandas**, this tool allows you to easily search for players, view detailed stats, and compare performances.

---

## Features

### Player Search
- Instantly search for players by name (case-insensitive).  
- Displays key metrics like **team**, **position**, **goals**, and **assists**.

### Top 10 Goal Contributors
- Shows the players with the **highest combined total** of goals and assists.  
- Stats from multiple teams (for transferred players) are merged automatically.

### Player Details
- Select any player to view their **full individual statistics**, including:
  - Goals, assists, expected goals (xG), expected assists (xAG), minutes, matches, and age.

### Player Comparison
- Compare **two players side by side** (even if they changed teams mid-season).  
- Includes **total performance stats** (summed across multiple teams).  
- Visualized using a clean bar chart built directly in Streamlit.

### Custom UI Theme
- White background with a dark purple header (`#3F1052`).  
- Soft gray sidebar and styled dataframes for better readability.  
- Fully responsive layout optimized for wide displays.

---

## Tech Stack

| Component | Description |
|------------|-------------|
| **Python** | Core language |
| **Streamlit** | Web framework for interactive dashboards |
| **Pandas** | Data manipulation and aggregation |
| **CSV** | Cleaned dataset (`clean_players.csv`) |

---

## Project Structure

The project is organized as follows:

- **app.py** — Main Streamlit app (entry point).  
- **clean_data.py** — Script for cleaning and preprocessing player data.  
- **export_data.py** — Script for scraping and exporting raw player data.  
- **clean_players.csv** — Cleaned dataset containing player statistics.  
- **README.md** — Project documentation and usage guide.

