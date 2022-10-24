import requests
from collections import Counter
from process_data import lemmatize_and_stem
import re


def search_id(title, original_data_json):
    title = title.replace(" ", "+")
    search_url = f"https://www.wikidata.org/w/index.php?search=%22{title}%22&title=Special:Search&profile=advanced&fulltext=1&ns0=1&ns120=1"
    response = requests.get(search_url)
    response = response.text.split("<div class=\"mw-search-result-heading\">")
    if len(response) <= 1:
        return None
    heading_id = response[1].split("\"")[1][6:]

    if heading_id in list(original_data_json.keys()):
        print(f"Hladany vyraz: \"{title.replace('+', ' ')}\" sa nachadza v databaze pod ID: {heading_id}")
        print(f"Alternativne mena pre vyraz \"{title.replace('+', ' ')}\":")
        for alt_name in original_data_json[heading_id]:
            print(f"    {alt_name}")
    elif heading_id:
        print(f"Hladany vyraz: {title}, s ID: {heading_id} sa v databaze nenachadza")
    else:
        print(f"Pre hladany vyraz: {title} neexistuje ID")

    # return heading_id


def request_heading(id):
    search_url = f"https://www.wikidata.org/wiki/{id}"
    response = requests.get(search_url)
    title = response.text.split("title>")[1][:-13]

    return title


def search_alt_name(alt_name, unique_words, original_data_json):
    unique_output = []
    processed_words = []
    unique_count = 0
    operation = 0  # 0 - OR, 1 - AND
    if re.search("^\"((?!\").)*\"$", alt_name):
        alt_name = alt_name[1:-1]
        operation = 1
    for word in alt_name.split(" "):
        s_w = lemmatize_and_stem(word)
        processed_words.append(s_w)
        if s_w in unique_words:
            unique_count += 1
            unique_output += list(unique_words[s_w].keys())
        else:
            print(f"slovo: \"{word}\" (po uprave \"{s_w}\") sa v slovniku nenachadza")
            return None

    # AND
    if operation == 1:
        title_counts = dict(Counter(unique_output))
        output = list(filter(lambda x: title_counts[x] == unique_count, title_counts))

        print(f"Vysledok hladania alternativnych mien pre zadany vyraz \"{alt_name}\"")
        for item in output:
            # title = request_heading(item)
            # print(f"Title: {title}, ID: {item}")
            print(f"ID: {item}")
            print("    " + '\n    '.join(original_data_json[item]))
            print("\n")

        return output

    # OR
    elif operation == 0:
        output = list(dict.fromkeys(unique_output))

        print(f"Vysledok hladania alternativnych mien pre zadany vyraz {alt_name}")
        for item in output:
            # title = request_heading(item)
            # print(f"Title: {title}, ID: {item}")
            print(f"ID: {item}")
            print("    " + '\n    '.join(original_data_json[item]))
            print("\n")

        return output
