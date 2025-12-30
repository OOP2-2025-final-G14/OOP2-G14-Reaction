from peewee import *
from datetime import datetime
import os

# DBファイルの場所
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "reactions.db")

db = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = db


class Reaction(BaseModel):
    emoji = CharField(max_length=10)
    created_at = DateTimeField(default=datetime.now)


def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables([Reaction])
