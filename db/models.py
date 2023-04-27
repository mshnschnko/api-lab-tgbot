from peewee import *
from dotenv import load_dotenv
import os
# from .db_config import *

dotenv_path = 'db.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_URL=os.environ.get("DB_URL")
DB_NAME=os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
DB_HOST=os.environ.get("DB_HOST")
DB_PORT=os.environ.get("DB_PORT")
DB_API_TOKEN=os.environ.get("DB_API_TOKEN")

conn = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

class BaseModel(Model):
    class Meta:
        database = conn

# class Notification(BaseModel):
#     notification_id = AutoField(column_name = 'notification_id')
#     user_id = IntegerField(column_name='user_id', null=False)
#     text = CharField(max_length=200, null=False)
#     time = DateTimeField(formats='%Y-%m-%d %H:%M:%S', null=True)
#     attachments = CharField(max_length=100, null=True)
#     is_done = BooleanField(default=False, null=True)
#     is_periodic = BooleanField(default=False, null=True)

class Notification(BaseModel):
    notification_id = AutoField(column_name = 'notification_id')
    user_id = IntegerField(column_name='user_id', null=False)
    notification_type = CharField(max_length=20)
    text = CharField(max_length=200, null=False)
    time = DateTimeField(formats='%Y-%m-%d %H:%M:%S', null=True)
    attachments = TextField(null=True)
    is_done = BooleanField(default=False, null=True)
    frequency = IntegerField(default=0, null=True)