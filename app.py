from flask import Flask
from requests import get

app = Flask(__name__)

PROVIDER_URL = 'https://provider-go.herokuapp.com/'


@app.route('/')
def hello():
    res = get(PROVIDER_URL)
    return res.content


if __name__ == '__main__':
    app.run()
