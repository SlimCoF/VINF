import requests
from process_data import lemmatize_and_stem
import re
import operator

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
    title = re.search(r'(<title>).*(<\/title>)', response.text)

    return title.group(0)[7:-19]


def search_alt_name(alt_name, unique_words, original_data_json):
    title_ids = {}
    processed_words = []
    operation = 0  # 0 - OR, 1 - AND

    if re.search("^\"((?!\").)*\"$", alt_name):
        alt_name = alt_name[1:-1]
        operation = 1

    for word in alt_name.split(" "):
        s_w = lemmatize_and_stem(word)
        if s_w not in processed_words:
            if s_w not in unique_words:
                print(f"slovo: \"{word}\" (po uprave \"{s_w}\") sa v slovniku nenachadza")
            else:
                processed_words.append(s_w)

                if len(title_ids) == 0:
                    title_ids = unique_words[s_w]
                else:
                    set1 = set(title_ids)
                    set2 = set(unique_words[s_w])
                    if operation == 1:
                        title_ids = {
                            key: title_ids.get(key, 0) * (1 + unique_words[s_w].get(key, 0)) for key in set1 & set2
                        }
                    elif operation == 0:
                        title_ids = {
                            key: title_ids.get(key, 0) * (1 + unique_words[s_w].get(key, 0)) for key in set1 | set2
                        }

    if len(processed_words) == 0:
        return None

    print(processed_words)
    title_ids = dict(sorted(title_ids.items(), key=operator.itemgetter(1), reverse=True))
    output = list(title_ids.keys())

    # AND
    if operation == 1:
        print(f'Vysledok hladania alternativnych mien pre zadany vyraz: "{alt_name}"')
        for item in output[:10]:
            title = request_heading(item)
            print(f'Title: "{title}", ID: {item}, TF_IDF: {title_ids[item]}')
            print("    " + '\n    '.join(original_data_json[item][:10]))
            print("\n")

        return output

    # OR
    elif operation == 0:
        print(f"Vysledok hladania alternativnych mien pre zadany vyraz: {alt_name}")
        for item in output[:10]:
            title = request_heading(item)
            print(f'Title: "{title}", ID: {item}, TF_IDF: {title_ids[item]}')
            print("    " + '\n    '.join(original_data_json[item][:10]))
            print("\n")

        return output
