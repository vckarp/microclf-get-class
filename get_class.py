import pickle
import json
import requests

from flask import Flask
from tokenizer import tokenizer, sw_en_dk
from flask import jsonify

app = Flask(__name__)
clf = None


@app.route("/")
def index():
    return "<h1>Welcome to the classification service</h1>"


@app.route("/get_clf")
def get_clf():
    global clf
    clf = pickle.load(open("clf.pickle", "rb"))
    return "<h1>Classifier loaded</h1>"


@app.route("/classify/<message>", methods=['GET'])
def classify(message):
    if not clf:
        get_clf()
    try:
        pred = clf.predict([message])
        prob = clf.predict_proba([message]).tolist()[0]
        prob = list(map((lambda x: str(round(x * 100, 2)) + "%"), prob))
        names = clf.named_steps.classifier.classes_.tolist()
        probs = list(zip(names, prob))
        probs.sort(reverse=True, key=(lambda x: x[1]))
        return jsonify([{"prediction": pred[0], "probabilities": dict(probs)}])
    except Exception as e:
        return "No classifier could be found", str(e)


# @app.route("/post_new")
# def post_new_data():
#     """A function to check the functionality of the append_db function from the ModelTrainService.py"""
#     with open('sample_data.json') as f:
#         data = json.load(f)
#     request = requests.post('http://127.0.0.1:5000/append_db', json=data)
#     return request.content


if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
