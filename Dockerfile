FROM python:3.13

WORKDIR /bingobot

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]
