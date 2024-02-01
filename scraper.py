import urllib.request
import json

from bs4 import BeautifulSoup

LAST_YEAR = 2023
N_YEARS = 10

all_data = {}
for year in range(LAST_YEAR-N_YEARS, LAST_YEAR+1):
    with urllib.request.urlopen(f"https://www.fussballdaten.de/bundesliga/{year}/tabelle/") as r:
        body = r.read().decode("utf-8")

    soup = BeautifulSoup(body, "html.parser")
    rows = soup.select(".content-statistik .content-tabelle table tbody tr")

    data = []
    for row in rows:
        cells = row.select("td")
        if len(cells) == 10:
            sample = {}
            for i, cell in enumerate(cells):
                if i == 0:
                    ...
                elif i == 1:
                    sample["ranking_number"] = int(cell.text)
                elif i == 2:
                    sample["name"] = cell.text.strip()
                elif i == 3:
                    sample["number_of_games"] = int(cell.text)
                elif i == 4:
                    sample["win"] = int(cell.text)
                elif i == 5:
                    sample["draw"] = int(cell.text)
                elif i == 6:
                    sample["lose"] = int(cell.text)
                elif i == 7:
                    sample["goals"], sample["goals_conceded"] = [int(it) for it in cell.text.split(":")]
                elif i == 8:
                    sample["goals_diff"] = int(cell.text)
                elif i == 9:
                    sample["points"] = int(cell.text)
                else:
                    raise NotImplementedError
            data.append(sample)

    assert len(data) == 18
    all_data[year] = data
    print(f"scrape bundesliga-{year-1}/{year}")

with open("data.json", "w") as f:
    json.dump(all_data, f, indent=4)
