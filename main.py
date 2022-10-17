# VINF - Alternatívne mená k Wiki stránkam - možnosti, parsovanie, vyhodnotenie (Python, Framework?)
# Filip Slimák

import requests
import json
from tqdm import tqdm

DATA_URL = "data/wikidata5m_entity.txt"
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


def load_data():
    with open(DATA_URL) as file:
        lines = file.readlines()
        return lines


def store_data(data_json):
    with open("data/data_file.json", "w") as write_file:
        json.dump(data_json, write_file, ensure_ascii=False)


def parse_data(data_arr):
    output_json = {}
    # s = requests.session()
    # s.mount('http://', requests.adapters.HTTPAdapter(max_retries=0))

    for line in tqdm(data_arr):
        line_arr = line.split('\t')
        title_id = line_arr[0]
        alt_names = line_arr[1:]
        alt_names[-1] = alt_names[-1][:-1]
        # alt_names[-1] = alt_names[-1].split("\n")[0] # pridava na case

        # response = s.get(WIKIDATA_URL + title_id)
        # title = response.text.split("<title>")[1].split("</title>")[0]
        # title = title[:-11]
        # title = title.split(" - Wikidata")[0] # pridava na case

        line_json = {
                        title_id: alt_names
                    }
        output_json.update(line_json)

    return output_json


def load_json_data():
    with open("data/data_file.json", "r") as json_file:
        json_data = json.loads(json_file.read())
    return json_data

if __name__ == '__main__':
    # data = load_data()
    # data_json = parse_data(data)
    # store_data(data_json)

    data_json = load_json_data()
    term = ""
    while not term == "X":
        term = input("Zadaj vyraz pre vyhladanie\n")
        heading_id = search_id(term)

        if heading_id in list(data_json.keys()):
            print(f"Hladany vyraz: {term} sa nachadza v databaze pod ID: {heading_id}")
            print(f"Alternativne mena pre vyraz {term}:")
            for alt_name in data_json[heading_id]:
                print(f"    {alt_name}")
        elif heading_id:
            print(f"Hladany vyraz: {term}, s ID: {heading_id} sa v databaze nenachadza")
        else:
            print(f"Pre hladany vyraz: {term} neexistuje ID")
