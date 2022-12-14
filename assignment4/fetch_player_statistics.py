import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html
from filter_urls import find_urls

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    # assert len(teams) == 8
    print(type(teams))
    # teams = teams[:3]

    # Gets the player for every team and stores in dict (get_players)
    all_players = dict()

    for team in teams:
        all_players[team["name"]] = get_players(team["url"])

    # get player statistics for each player,
    # using get_player_stats
    for team, players in all_players.items():
        for player in players:
            player.update(get_player_stats(player["url"], team))

    # Select top 3 for each team by points:
    best = {}
    for team in teams:
        best[team["name"]] = list()

    for i in range(3):
        for team_name in all_players:
            num_players = len(all_players[team_name])

            # best_index = max(range(num_players), all_players[team_name], key=lambda x: x["points"])
            best_index = max(
                range(num_players), key=lambda x: all_players[team_name][x]["points"]
            )
            best[team_name].append(all_players[team_name].pop(best_index))

    stats_to_plot = ["points", "assists", "rebounds"]
    for stat in stats_to_plot:
        plot_best(best, stat=stat)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds]??which stat to plot.
            Should be a key in the player info dictionary.
    """
    stats_dir = "NBA_player_statistics"

    if not os.path.exists(stats_dir):
        os.mkdir(stats_dir)

    for team_name in best:
        best[team_name].sort(key=lambda x: x[stat])

    X = list(best)
    first = list()
    f_name = list()

    second = list()
    s_name = list()

    third = list()
    t_name = list()

    for team_name in best:
        first.append(best[team_name][2][stat])
        f_name.append(best[team_name][2]["name"])

        second.append(best[team_name][1][stat])
        s_name.append(best[team_name][1]["name"])

        third.append(best[team_name][0][stat])
        t_name.append(best[team_name][0]["name"])

    X_axis = np.arange(len(X))

    max_val = max(first + second + third)

    fig, ax = plt.subplots()

    width = 0.3
    p1 = ax.bar(X_axis - width, first, width, label="First")
    p2 = ax.bar(X_axis, second, width, label="Second")
    p3 = ax.bar(X_axis + width, third, width, label="Third")

    ax.bar_label(
        p1,
        f_name,
        rotation=90,
        padding=4,
    )

    ax.bar_label(
        p2,
        s_name,
        rotation=90,
        padding=4,
    )

    ax.bar_label(
        p3,
        t_name,
        rotation=90,
        padding=4,
    )

    ax.set_xticks(X_axis, X)
    ax.set_xlabel("Team")
    ax.set_ylabel(f"{stat} per game")
    ax.set_title(f"{stat} per game for 2021-22 NBA regular season")
    ax.set_ylim(0, max_val * 1.5)
    ax.legend()

    plt.savefig(f"{stats_dir}/{stat}.png")
    plt.show()


def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Get the table
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    roster = soup.find(id="Roster")
    table = roster.find_next("table", {"class": "toccolours"})

    players = []
    # Loop over every row and get the names from roster
    rows = table.find_all("tr")
    # players only show up after row 4
    rows = rows[3:]
    for row in rows:
        # Get the columns
        cols = row.find_all("td")
        url = find_urls(str(cols[2])).pop()
        match = re.search(r"<a.*?>(.*)?<\/a>", str(cols[2]))
        name = match.group(1)

        players.append({"name": name, "url": url})

    # return list of players
    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    # gets a float from a cell in the table
    def get_floats(cols: list, index: int) -> float:
        if cols[index].string:
            return float(cols[index].string.strip().replace("*", ""))
        else:
            return float(cols[index].b.string)

    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    regular = soup.find(id="Regular_season")
    if not regular:
        regular = soup.find(id="NBA")
    table = regular.find_next("table", {"class": "wikitable"})

    rows = table.find_all("tr")
    rows = rows[1:]

    stats = None

    # Loop over rows and extract the stats

    for row in rows:
        cols = row.find_all("td")

        href_body_pattern = r"<a.*>(.*)<\/a>"

        date = ""
        match = re.search(r"title=\"(\d{4}).(\d{2})", str(cols[0]))
        if match:
            date = f"{match.group(1)} {match.group(2)}"

        colteam = ""
        match = re.search(href_body_pattern, str(cols[1]))
        if match:
            colteam = match.group(1)

        # if colteam == team and date == "2021 22":
        if colteam == team and date == "2021 22":
            rpg = get_floats(cols, 8)
            apg = get_floats(cols, 9)
            spg = get_floats(cols, 10)
            bpg = get_floats(cols, 11)
            ppg = get_floats(cols, 12)

            return {
                "rebounds": rpg,
                "assists": apg,
                "steals": spg,
                "blocks": bpg,
                "points": ppg,
            }

    # if player did not play, return 0
    return {
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "points": 0,
    }


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
