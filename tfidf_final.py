import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words
import math


def txt_json(webtext):
    read_text_file = webtext.splitlines()
    str_list = list(filter(None, read_text_file))
    dictOfParagraphs = {i: str_list[i] for i in range(0, len(str_list))}
    json_list=[]
    for j in range(0,len(str_list)):
        json_data = {
            "id": str(j),
            "text": dictOfParagraphs[j]
        }
        json_list.append(json_data)
    return json_list

def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

def stemming(data):
    stemmer = PorterStemmer()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = remove_stop_words(data)
    return data


def clean_json(webtext):
    processed_title = []
    processed_text = []
    paragraphs= txt_json(webtext)
    for j in range(len(paragraphs)):
        processed_text.append(word_tokenize(str(preprocess(paragraphs[j]['text']))))
        processed_title.append(paragraphs[j]['id'])
    return paragraphs,processed_text, processed_title

def calc_df(processed_text):
    DF = {}
    N = len(processed_text)
    for i in range(N):
        tokens = processed_text[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}
    for i in DF:
        DF[i] = len(DF[i])
    total_vocab_size = len(DF)
    total_vocab = [x for x in DF]
    return total_vocab_size, total_vocab, DF

def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

def calc_tfidf(doc,processed_text):
    tf_idf = {}
    N = len(processed_text)
    for i in range(N):
        tokens = processed_text[i]
        counter = Counter(tokens)
        words_count = len(tokens)
        for token in np.unique(tokens):
            tf = counter[token] / words_count
            df = doc_freq(token)
            idf = np.log((N + 1) / (df + 1))
            tf_idf[doc, token] = tf * idf
        doc += 1
    return tf_idf

def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

def vectorise(processed_text,vocab_size,vocab,tf_idf):
    N = len(processed_text)
    Da = np.zeros((N, vocab_size))
    for i in tf_idf:
        try:
            ind = vocab.index(i[1])
            Da[i[0]][ind] = tf_idf[i]
        except:
            pass
    return Da

def gen_vector(tokens,processed_text,vocab):
    N = len(processed_text)
    Q = np.zeros((len(vocab)))
    counter = Counter(tokens)
    words_count = len(tokens)
    for token in np.unique(tokens):
        tf = counter[token] / words_count
        df = doc_freq(token)
        idf = math.log((N + 1) / (df + 1))
        try:
            ind = vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass
    return Q


def cosine_similarity(k, query,Da,processed_text,vocab):
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))

    d_cosines = []
    query_vector = gen_vector(tokens,processed_text,vocab)

    for d in Da:
        d_cosines.append(cosine_sim(query_vector, d))
    out = np.array(d_cosines).argsort()[-k:][::-1]

    return out

str_list2=[]

def create_json(parags,out):
    for k in range(len(out)):
        str_list2.append(parags[out[k]]['text'])
    dictOfParagraphs = {i: str_list2[i] for i in range(0, len(str_list2))}
    json_list=[]
    for j in range(0,len(str_list2)):
        json_data = {
            "text": dictOfParagraphs[j] ,
            "paragraph_id": str(j)
        }
        json_list.append(json_data)
    return json_list


def process(webtext,query,nbPar):
    doc = 0
    parags,processed_text,processed_title=clean_json(webtext)
    vocab_size,vocab, DF = calc_df(processed_text)
    tf_idf=calc_tfidf(doc,processed_text)
    D=vectorise(processed_text,vocab_size,vocab,tf_idf)
    out=cosine_similarity(nbPar,query,D,processed_text,vocab)
    final_dict=create_json(parags,out)
    return(final_dict)
