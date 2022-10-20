# VINF - Alternatívne mená k Wiki stránkam - možnosti, parsovanie, vyhodnotenie (Python, Framework?)
# Filip Slimák

import requests
from process_data import *

DATA_URL = "data/wikidata5m_entity.txt"
STEMMED_DATA_JSON_URL = "data/stemmed_data_file.json"
ORIGINAL_DATA_JSON_URL = "data/original_data_file.json"
UNIQUE_DATA_JSON_URL = "data/unique_data_file.json"
WIKIDATA_URL = "https://www.wikidata.org/wiki/"


def search_id(search_term):
    search_term = search_term.replace(" ", "+")
    search_url = f"https://www.wikidata.org/w/index.php?search=%22{search_term}%22&title=Special:Search&profile=advanced&fulltext=1&ns0=1&ns120=1"
    response = requests.get(search_url)
    response = response.text.split("<div class=\"mw-search-result-heading\">")
    if len(response) <= 1:
        return None
    heading_id = response[1].split("\"")[1][6:]
    return heading_id


if __name__ == '__main__':
    raw_data = load_raw_data(DATA_URL)
    original_data_json, unique_words = parse_data(raw_data)
    store_data(original_data_json, ORIGINAL_DATA_JSON_URL)
    store_data(unique_words, UNIQUE_DATA_JSON_URL)




    # stemmed_data_json = load_json_data(STEMMED_DATA_JSON_URL)
    # original_data_json = load_json_data(ORIGINAL_DATA_JSON_URL)
    # term = ""
    # while not term == "X":
    #     term = input("Zadaj vyraz pre vyhladanie\n")
    #     heading_id = search_id(term)
    #
    #     if heading_id in list(original_data_json.keys()):
    #         print(f"Hladany vyraz: {term} sa nachadza v databaze pod ID: {heading_id}")
    #         print(f"Alternativne mena pre vyraz {term}:")
    #         for ind in range(len(original_data_json[heading_id])):
    #             print(f"    {original_data_json[heading_id][ind]}")
    #     elif heading_id:
    #         print(f"Hladany vyraz: {term}, s ID: {heading_id} sa v databaze nenachadza")
    #     else:
    #         print(f"Pre hladany vyraz: {term} neexistuje ID")
