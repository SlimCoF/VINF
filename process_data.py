# pyspark
import json
from tqdm import tqdm
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


def lemmatize_and_stem(word):

    if (len(word) > 2 or word.isnumeric()) and word not in stop_words:
        l_w = wl.lemmatize(word)
        s_w = ps.stem(l_w)

        if s_w not in stop_words:
            return s_w
    else:
        return None


def preprocessing(alt_names, uniqe_words, title_id):
    tokenization = tokenizer.tokenize(alt_names)
    words = []
    for word in tokenization:
        processed_word = lemmatize_and_stem(word)
        if processed_word is not None:
            words.append(processed_word) #  sample: 1000m uw: 7 992
            get_unique(processed_word, uniqe_words, title_id)

    return words

def get_unique(word, unique_words, title_id):

    if word not in unique_words:
        unique_words.update({word: {title_id: 1}})
    else:
        if title_id in unique_words[word]:
            unique_words[word][title_id] += 1
        else:
            unique_words[word].update({title_id: 1})


"""
TF-ID:

cf(t) - pocet, kolkokrat sa vyraz t nachadza v celej kolekcii dokumentov
tf(t,d) - pocet, kolkokrat sa vyraz t nachadza v dokumente d
df(t) - pocet, v kolko dokumentoch sa vyraz t nachadza 
N - pocet vsetkych dokumentov

itdf(t) = log(N/df(t))
tf-idf(t,d) = tf(t,d) x idf(t)
"""
# def idft(unique_words, N):
#     print(f"Document number: {N}")
#
#     for item in unique_words:
#         df = len(unique_words[item])
#         idtf = math.log(N/df)
#         for key in unique_words[item]:
#             tf = unique_words[item][key]
#             tf_idtf = tf * idtf


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

        original_line_json = {
                        title_id: orig_names
                    }
        original_output.update(original_line_json)

    # idft(unique_words, len(data_arr[0:1000]))
    return original_output, unique_words


# time: 26
# u_w: 6 851