import requests
import re
import lucene

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.en import EnglishAnalyzer
lucene.initVM()

from java.io import File

class color:
   BOLD = '\033[1m'
   END = '\033[0m'

INDEX_PATH = "./index"
index_dir = FSDirectory.open(File(INDEX_PATH).toPath())
searcher = IndexSearcher(DirectoryReader.open(index_dir))
searcher.setSimilarity(BM25Similarity(1.2, 0.75))


def searchAltNames(term):
    query = QueryParser("alt_names", EnglishAnalyzer()).parse(term)
    query_output = searcher.search(query, 10).scoreDocs
    output = []
    for item in query_output:
        doc = searcher.doc(item.doc)
        output.append((doc.get("title_id"), doc.get("alt_names").split(";")))
    return output


def searchTitle(title_id):
    query = QueryParser("title_id", EnglishAnalyzer()).parse(title_id)
    query_output = searcher.search(query, 1).scoreDocs
    output = []
    for item in query_output:
        doc = searcher.doc(item.doc)
        output.append((doc.get("title_id"), doc.get("alt_names").split(";")))
    return output


def getTitle(title_id):
    wiki_url = f"https://www.wikidata.org/wiki/{title_id}"
    response = requests.get(wiki_url)
    title = re.search(r'(<title>).*(<\/title>)', response.text)
    return title.group(0)[7:-19]


def getTitleId(title):
    title = title.replace(" ", "+")
    wiki_url = f"https://www.wikidata.org/w/index.php?search=%22{title}%22&title=Special:Search&profile=advanced&fulltext=1&ns0=1&ns120=1"
    response = requests.get(wiki_url)
    response = response.text.split("<div class=\"mw-search-result-heading\">")
    if len(response) <= 1:
        return None
    heading_id = response[1].split("\"")[1][6:]
    return heading_id


def showOutput(searchOutput):
    for item in searchOutput:
        title = getTitle(item[0])
        print(f"Link: {color.BOLD}https://en.wikipedia.org/wiki/{title.replace(' ', '_')}{color.END}")
        print(f"Nazov: {color.BOLD}{title}{color.END}")
        print("Alternativne mena:")
        print("    " + "\n    ".join(item[1][:10]))


if __name__ == "__main__":

    option = ""
    while option.lower() != "e":
        print("--------------------------------------------")
        option = input("H - Hladanie podla nazvu\n" +
                       "A - Hladanie v alternativnych menach\n" +
                       "E - Ukoncenie\n")

        if option.lower() == "h":
            title = input("Zadaj nazov:\n")
            title_id = getTitleId(title)
            if title_id == None:
                print("Neexistuje clanok s hladanym nazvom!!")
                continue;
            searchOutput =  searchTitle(title_id)
            if searchOutput == []:
                print(f"Nazov: {color.BOLD}{title}{color.END} , id: {color.BOLD}{title_id}{color.END} sa nenachadza v databaze")
                continue;
            print(f"Vysledok hladania pre nazov: {title}")
            showOutput(searchOutput)

        elif option.lower() == "a":
            term = input("Zadaj vyraz:\n")
            searchOutput = searchAltNames(term)
            if searchOutput == []:
                print(f"Pre vyraz: {color.BOLD}{term}{color.END} sa nenasla ziadna zhoda")
                continue;
            print(f"Vysledok hladania pre vyraz: {term}")
            showOutput(searchOutput)

        elif option.lower() == "e":
            break

        else:
            print("Pre zadany znak neexistuje funkcionalita!!")
         