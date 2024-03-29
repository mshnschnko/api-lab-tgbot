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
# COPY app.py ./app.py
# COPY startup.sh ./startup.sh

EXPOSE 5000
EXPOSE 8000
EXPOSE 5432

# RUN chmod a+x startup.sh
RUN mkdir -p ./storage/temp
RUN mkdir -p ./storage/backup
RUN touch storage/dump.sql

RUN chmod ugo+rwx storage/dump.sql

CMD [ "python", "run.py" ]
# ENTRYPOINT ["./startup.sh"]