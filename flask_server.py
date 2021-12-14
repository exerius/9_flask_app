import flask
from flask import Flask
from hashlib import sha256
from datetime import datetime
from os import remove
from pickle import dump, load
app = Flask(__name__)


def open_db():
    try:
        with open("db.txt", "rb") as file:
            content = load(file)
        data = {i.split(":")[0]: i.split(":")[1:] for i in content}
    except: data = {}
    return data


def update_db(text):
    remove("db.txt")
    content = ["%s:%s:%s" % (i, sha256(text[i][0].encode()).hexdigest(), text[i][1]) for i in text]
    with open("db.txt", "wb") as file:
        dump(content, file)


@app.route('/user/<nickname>', methods=['GET'])
def do_GET(nickname):
    data = open_db()
    return flask.jsonify(name=nickname, password=data[nickname][0], date=data[nickname][1])


@app.route('/user/<nickname>', methods=["POST", "PUT"])
def do_POST(nickname):
    content = flask.request.get_json()
    data = open_db()
    data.update({nickname: [content["password"], datetime.now().strftime('%d/%m/%y')]})
    update_db(data)
    resp = flask.jsonify(success=True)
    return resp


@app.route('/user/<nickname>', methods=["DELETE"])
def do_DELETE(nickname):
    data = open_db()
    data.pop(nickname)
    update_db(data)
    return flask.jsonify(success=True)


if __name__ == '__main__':
    app.run()
