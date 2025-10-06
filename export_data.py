import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd 

url = "https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats"

headers = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
comments = soup.find_all(string=lambda text: isinstance(text, Comment))

table = next(
    (BeautifulSoup(comment, "html.parser").find("table", id="stats_standard") for comment in comments if "stats_standard" in comment),
    None
)

for comment in comments:
    if "stats_standard" in comment:
        comment_soup = BeautifulSoup(comment, "html.parser")
        table = comment_soup.find("table", id="stats_standard")

        if table:
            print("Table founded!")
            break
else:
    print("❌ No player table!")

try:
    players_df = pd.read_html(str(table))[0]
    players_df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in players_df.columns]
    players_df.to_csv("players.csv", index=False)
    print("Saved.")
except Exception as e:
    print("❌ No player table!", e)