from flask import Flask
from requests import get
import os

app = Flask(__name__)

PROVIDER_URL = 'https://provider-go.herokuapp.com/'


@app.route('/')
def hello():
    res = get(PROVIDER_URL)
    return res.content


port = os.getenv('PORT')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port if port is not None else 5000)
