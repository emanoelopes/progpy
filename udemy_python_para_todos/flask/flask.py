from flask import Flask

app = Flask(__name__)


@app.route("/")
def ola():
    return u'Olá Mundo'


if __name__ == '__main__':
    app.run()
