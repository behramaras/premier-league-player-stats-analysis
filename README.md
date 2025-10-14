# Premier League Player Stats Explorer (2024–2025)

An interactive Streamlit web app to explore, compare, and analyze player performance data from the **Premier League 2024–25** season.  
Built with **Python**, **Streamlit**, and **Pandas**, this tool allows you to easily search for players, view detailed stats, and compare performances.
- Link: [Premier League Player Stats Explorer](https://behramaras-premier-league-player-stats-analysis.streamlit.app)
---

# Premier League Player Stats Explorer (2024-2025)

This project scrapes, cleans, and visualizes Premier League player statistics for the 2024-2025 season using Python, pandas, and Streamlit.

---

## Features

1. **Data Scraping**
   - Scrapes player stats from [FBref Premier League Stats](https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats) using `requests` and `BeautifulSoup`.
   - Extracts the standard stats table hidden inside HTML comments.

2. **Data Cleaning**
   - Selects relevant columns such as player name, team, position, goals, assists, minutes played, age, and expected stats.
   - Renames columns to standardized and readable names.
   - Removes repeated headers or invalid rows.
   - Converts numeric columns to proper data types.
   - Outputs a cleaned CSV file: `clean_players.csv`.

3. **Interactive Streamlit App**
   - Uses `st_aggrid` for interactive tables with sorting, filtering, and pagination.

### Player Search
- Instantly search for players by name (case-insensitive).  
- Displays key metrics like **team**, **position**, **goals**, and **assists**.

### Top 10 Goal Contributors
- Shows the players with the **highest combined total** of goals and assists.  
- Stats from multiple teams (for transferred players) are merged automatically.

### Player Details
- Select any player to view their **full individual statistics**, including:
  - Goals, assists, expected goals, expected assists, minutes, matches, and age.

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
| **Streamlit-AgGrid**| Interactive tables with sorting, filtering, pagination, and sidebar options |
---

## Project Structure

The project is organized as follows:

- **app.py** — Main Streamlit app (entry point).  
- **clean_data.py** — Script for cleaning and preprocessing player data.  
- **export_data.py** — Script for scraping and exporting raw player data.  
- **clean_players.csv** — Cleaned dataset containing player statistics.  
- **README.md** — Project documentation and usage guide.

## Setup Instructions

Follow these steps to set up and run the project locally.

---

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/premier-league-player-stats-explorer.git
cd premier-league-player-stats-explorer
```

### 2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On macOS/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```
## Usage

### 1. Launch the Streamlit app:
```bash
streamlit run app.py
```
### 2. Explore player stats:
- Use the search bar to filter players.
- Click table headers to sort by goals, assists, minutes, etc.
- Compare two players using the dropdown menus.
- View the top 10 goal contributors.

### 3. Live Demo
- You can also check the live application directly here: [Premier League Player Stats Explorer](https://behramaras-premier-league-player-stats-analysis.streamlit.app)

**Author: Behram Aras**
