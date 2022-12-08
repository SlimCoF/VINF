# coding=utf-8
# VINF - Alternatívne mená k Wiki stránkam - možnosti, parsovanie, vyhodnotenie (Python, Framework?)
# Filip Slimák

from process_data import *
from searching import *

import nltk
nltk.download('stopwords')
nltk.download('wordnet')

DATA_URL = "./data/wikidata5m_entity.txt"
ORIGINAL_DATA_JSON_URL = "./data/original_data_file.json"
UNIQUE_DATA_JSON_URL = "./data/unique_data_file.json"
WIKIDATA_URL = "https://www.wikidata.org/wiki/"

if __name__ == '__main__':
    option = input("L - pre spracovanie dat\n" +
                   "S - pre vyhladavanie nad datami\n" +
                   "E - pre ukoncenie\n")
    if option.lower() == "l":
        raw_data = load_raw_data(DATA_URL)
        original_data_json, unique_words = parse_data(raw_data)
        unique_words = tf_idft(unique_words, len(original_data_json))
        store_data(original_data_json, ORIGINAL_DATA_JSON_URL)
        store_data(unique_words, UNIQUE_DATA_JSON_URL)
    elif option.lower() == "s":
        unique_words = load_json_data(UNIQUE_DATA_JSON_URL)
        original_data_json = load_json_data(ORIGINAL_DATA_JSON_URL)
        option = ""
        while option.lower() != "e":
            option = input("H - pre zadanie nazvu\n" +
                           "A - pre zadanie alternativneho mena\n" +
                           "E - pre ukoncenie\n")

            if option.lower() == "h":
                title = input("Zadaj nazov\n")
                heading_id = search_id(title, original_data_json)

            elif option.lower() == "a":
                alt_name = input("Zadaj alternativne meno\n")
                heading_ids = search_alt_name(alt_name, unique_words, original_data_json)
            else:
                print("Zvolena moznost nema funkcionalitu")
    else:
        print("Zvolena moznost nema funkcionalitu")
        
