import flask
from flask import Flask
from hashlib import sha256
app = Flask(__name__)


def open_db():
    with open("db.txt", "r") as file:
        data = {i.split(":")[0]: i.split(":")[1:] for i in file}
    return data


def update_db(text):
    with open("db.txt", "w") as file:
        for i in text:
            line = i+":"+":".join(text[i])
            file.write(line)


@app.route('/user/<nickname>', methods=['GET'])
def do_GET(nickname):
    data = open_db()
    return flask.jsonify(name=nickname, password=data[nickname][0], date=data[nickname][1])


@app.route('/user/<nickname>', methods=["POST", "PUT"])
def do_POST(nickname):
    data = open_db()
    content = flask.request.json
    content["password"] = sha256(content["password"].encode()).hexdigest()
    data.update(content)
    update_db(data)


@app.route('/user/<nickname>', methods=["DELETE"])
def do_POST(nickname):
    data = open_db()
    data.pop(nickname)
    update_db(data)



if __name__ == '__main__':
    app.run()
