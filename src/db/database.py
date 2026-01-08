from peewee import *
from datetime import datetime
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
db_path = os.path.join(PROJECT_ROOT, "reactions.db")

db = SqliteDatabase(db_path)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class Reaction(BaseModel):
    topic = CharField(max_length=100)
    emoji = CharField(max_length=10)

    @classmethod
    def add(cls, topic, emoji):
        return cls.create(topic=topic, emoji=emoji)

    @classmethod
    def latest(cls, topic, limit=10):
        return (
            cls.select()
            .where(cls.topic == topic)
            .order_by(cls.created_at.desc())
            .limit(limit)
        )
    
    @classmethod
    def count_by_emoji(cls, topic):
        return (
            cls
            .select(cls.emoji, fn.COUNT(cls.id).alias("cnt"))
            .where(cls.topic == topic)
            .group_by(cls.emoji)
            .order_by(fn.COUNT(cls.id).desc())
        )
    
    # お題ごとに集計リセット（削除）
    @classmethod
    def reset_topic(cls, topic):
        return cls.delete().where(cls.topic == topic).execute()
    
    



TABLES = [Reaction]


def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables(TABLES)


def close_db():
    if not db.is_closed():
        db.close()
