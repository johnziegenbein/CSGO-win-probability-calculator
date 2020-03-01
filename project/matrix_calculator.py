import sys

import requests
from bs4 import BeautifulSoup

OK_CODE = 200

MAP_DICT = {"Cache": 29,
            "Dust2": 31,
            "Mirage": 32,
            "Inferno": 33,
            "Nuke": 34,
            "Train": 35,
            "Cobblestone": 39,
            "Overpass": 40,
            "Vertigo": 46}


def calculate_probability_from_matrix(map_played, ct_rounds, t_rounds):
    url = resolve_url(map_played)
    document = requests.get(url)
    if document.status_code == OK_CODE:
        data = get_matrix_from_document(document)
        assert len(data) == 16  # Sanity check to make sure correct data has been extracted
        return data[ct_rounds][t_rounds]
    else:
        sys.exit("Could not retrieve html document")


def resolve_url(map_played):
    map_id = MAP_DICT[map_played]
    url = "https://www.hltv.org/stats/maps/map/" + str(map_id) + "/" + map_played + "?showKills=true&showDeaths=false&firstKillsOnly=false&allowEmpty=false&showKillDataset=true&showDeathDataset=false"
    return url


def get_matrix_from_document(document):
    data = []
    soap = BeautifulSoup(document.content, 'html.parser')
    table = soap.find("table", class_="stats-table no-sort stats-matrix")
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')[3:]  # First 3 indices are headers and empty
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data
