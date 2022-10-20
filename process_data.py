import json
from tqdm import tqdm
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


stop_words = set(stopwords.words('english'))
ps = PorterStemmer()
wl = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')


def load_json_data(data_url):
    with open(data_url, "r") as json_file:
        json_data = json.loads(json_file.read())
    return json_data


def load_raw_data(data_url):
    with open(data_url) as file:
        lines = file.readlines()
        return lines


def store_data(data_json, data_url):
    with open(data_url, "w") as write_file:
        json.dump(data_json, write_file, ensure_ascii=False)


def preprocessing(alt_names, uniqe_words, title_id):
    # tokenization = nltk.word_tokenize(alt_names)
    tokenization = tokenizer.tokenize(alt_names)
    words = []
    for w in tokenization:
        if len(w) > 2 or w.isnumeric():
            word_root = ps.stem(w)
            if word_root not in stop_words:
                # words.append(wl.lemmatize(w)) # sample: 1000, uw: 15 497
                # words.append(ps.stem(w)) # sample: 1000, uw: 7 980

                l_w = wl.lemmatize(w)
                s_w = ps.stem(l_w)
                words.append(s_w) # sample: 1000m uw: 7 992

                get_unique(s_w, uniqe_words, title_id)
    return words


# {
#   word: {
#           id: 10,
#           id2: 20,
#          }
# }

# def get_unique(term, uniqe_words, title_id):
def get_unique(word, uniqe_words, title_id):

    # for word in term:
    if word not in uniqe_words:
        uniqe_words.update({word: {title_id: 1}})
    else:
        if title_id in uniqe_words[word]:
            uniqe_words[word][title_id] += 1
        else:
            uniqe_words[word].update({title_id: 1})


def parse_data(data_arr):
    original_output = {}
    unique_words = {}

    for line in tqdm(data_arr[0:1000]):
        line_arr = line.split('\t')
        title_id = line_arr[0]
        alt_names = line_arr[1:]
        alt_names[-1] = alt_names[-1][:-1]
        orig_names = []

        for x in range(len(alt_names)):
            orig_names.append(alt_names[x])
            alt_names[x] = preprocessing(alt_names[x], unique_words, title_id)
            # get_unique(alt_names[x], unique_words, title_id)

        original_line_json = {
                        title_id: orig_names
                    }
        original_output.update(original_line_json)

    # print(len(unique_words))
    # print(json.dumps(original_output["Q7777598"], indent=4))
    # print(json.dumps(unique_words, indent=4, ensure_ascii=False))
    return original_output, unique_words


# time: 26
# u_w: 6 851