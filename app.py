import uuid
import tfidf_final
import w2vec
import w2vec_new

from flask import Flask, jsonify, request
from flask_cors import CORS



TEXT = []
QUERY = []
PARAGRAPHS = []

state = 0

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_book(book_id):
    for book in TEXT:
        if book['id'] == book_id:
            TEXT.remove(book)
            return True
    return False

def launchProcess():
    global PARAGRAPHS
    text = TEXT[0]['text']

    query = QUERY[0]['myQuery']
    nbPar = QUERY[0]['nbPar']

    mode = QUERY[0]['mode']
    QUERY.clear()

    if (mode == 'vague'):

        PARAGRAPHS = w2vec_new.process(text,query,nbPar)

        print("with word embedding")
    if (mode == 'precise'):
        PARAGRAPHS = tfidf_final.process(text,query,nbPar)
        print("with tfidf")

    return



@app.route('/books', methods=['GET', 'POST'])
def all_books():
    global state
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        if (post_data.get('id') == 1):
            print('in text receiving')
            TEXT.append({
                'id': post_data.get('id'),
                'text': post_data.get('text')
            })
        if (post_data.get('id') == 2):
            QUERY.append({
                'id': post_data.get('id'),
                'myQuery': post_data.get('myQuery'),
                'nbPar': post_data.get('nbPar'),
                'mode': post_data.get('mode')
            })

            state = 1

            launchProcess()

        response_object['message'] = 'Book added!'
    else:
        if state == 0:
            print('in text publishing')
            print(TEXT)
            response_object['books'] = TEXT.copy()

        if state == 1:
            print(PARAGRAPHS)
            response_object['books'] = PARAGRAPHS.copy()
            TEXT.clear()
            PARAGRAPHS.clear()
            state = 0
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        TEXT.append({
            'id': uuid.uuid4().hex,
            'text': post_data.get('text')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
