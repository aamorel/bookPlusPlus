import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from num2words import num2words
import gensim
model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300-SLIM.bin', binary=True)
word_vectors = model.wv
id = 0

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
    #data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    #data = stemming(data)
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

def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim


def cosine_similarity(k, query,Da):
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))
    print("Query:", query)
    print(tokens)
    d_cosines = []

    score_q = []
    big_model_q = np.zeros(len(model['car']))
    oov=[]
    for i in range(len(tokens)):
        if tokens[i] in word_vectors.vocab:
            pass
        else:
            oov.append(i)
    oov.sort(reverse=True)
    for n in oov:
        del tokens[n]
    for s in range(len(tokens)):
        big_model_q += model[tokens[s]]
    score_q.append(big_model_q / len(tokens))

    for d in Da:
        d_cosines.append(cosine_sim(score_q, d))
    new_d_cosine=[]
    for d_cos in d_cosines:
        new_d_cosine.append(d_cos.tolist()[0])
    out = np.array(new_d_cosine).argsort()[-k:][::-1]
    return out



def create_json(parags,out):
    str_list2=[]
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
    global id
    parags,processed_text,processed_title=clean_json(webtext)
    score = []
    for j in range(len(processed_text)):
        tokens = processed_text[j]
        big_model = np.zeros(len(model['car']))
        oov=[]
        for i in range(len(tokens)):
            if tokens[i] in word_vectors.vocab:
                pass
            else:
                oov.append(i)
        oov.sort(reverse=True)
        for n in oov:
            del tokens[n]
        for s in range(len(tokens)):
            big_model += model[tokens[s]]
        score.append(big_model / len(tokens))
    D=score
    out=cosine_similarity(nbPar,query,D)
    final_dict=create_json(parags,out)
    print(final_dict)
    for h in range(len(final_dict)):
        pre_text=final_dict[h]['text']
        new_t=pre_text.split('.')
        new_t = [x for x in new_t if x.strip()]
        score2=[]
        for j in range(len(new_t)):
            sentence = new_t[j]
            post_text=preprocess(sentence)
            tokens = word_tokenize(str(post_text))
            big_model = np.zeros(len(model['car']))
            oov = []
            for i in range(len(tokens)):
                if tokens[i] in word_vectors.vocab:
                    pass
                else:
                    oov.append(i)
            oov.sort(reverse=True)
            for n in oov:
                del tokens[n]
            for s in range(len(tokens)):
                big_model += model[tokens[s]]
            score2.append(big_model / len(tokens))
        D = score2
        out2 = cosine_similarity(1, query, D)
        hg=new_t[out2[0]]
        final_dict[h]['id'] = id
        id += 1
        final_dict[h]['sentence'] = hg
    return final_dict
