FROM python

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]