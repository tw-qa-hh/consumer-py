# Welcome to consumer-py

##### How to run locally:
```
Pre-requisites:
- Installed python3 (3.8)
- Installed pip
```

1. Install dependencies `python -m pip install -r requirements.txt`
2. Run app `python app.py`
3. Open `http://localhost:5000/`

---


Run with Docker:
```
docker build . -t consumer-py
docker run -p5000:5000 consumer-py
```
