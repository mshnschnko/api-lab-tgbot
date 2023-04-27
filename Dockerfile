FROM python:3.10.10

WORKDIR /api-lab-tgbot

COPY requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get update && apt-get install -y postgresql

RUN pip install -r requirements.txt

COPY .env ./.env
COPY db.env ./db.env

COPY bot/ ./bot/
COPY db/ ./db/
COPY backup.py ./backup.py
COPY exceptions.py ./exceptions.py
COPY run.py ./run.py


EXPOSE 5000
EXPOSE 5432

RUN mkdir -p ./storage/temp
RUN mkdir -p ./storage/backup
RUN touch storage/dump.sql
RUN chmod ugo+rwx storage/dump.sql

CMD [ "python", "bot.py" ]