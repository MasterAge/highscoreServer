import os
import sqlite3
from flask import g as ctx, Flask

from data import Datastore, Player

DATABASE_FILE = "highscores.db"

# https://flask.palletsprojects.com/en/2.1.x/patterns/sqlite3/


def close_connection(_):
    db = getattr(ctx, '_database', None)
    if db is not None:
        db.close()


class SQLDatastore(Datastore):
    def __init__(self, app: Flask) -> None:
        super().__init__()
        self.app = app
        app.teardown_appcontext(close_connection)

    def init(self):
        if os.path.exists(DATABASE_FILE):
            return

        with self.app.app_context():
            db = self.get_db()
            with self.app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    def get_db(self):
        db = getattr(ctx, '_database', None)
        if db is None:
            db = ctx._database = sqlite3.connect(DATABASE_FILE)
            db.row_factory = lambda cursor, row: Player(row[0], row[1], location=row[2])
        return db

    def query_db(self, query, args=(), one=False, update=False):
        cursor = self.get_db().execute(query, args)
        if update:
            self.get_db().commit()
            cursor.close()
        else:
            rows = cursor.fetchall()
            cursor.close()

            if one:
                return rows[0] if rows else None
            return rows

    def create_player(self, new_player: Player):
        self.query_db("insert into SCORES values (?, ?, ?)",
                      [new_player.username, new_player.score, new_player.location], update=True)

    def update_player_score(self, player_name: str, score: int):
        self.query_db("update SCORES set SCORE=? where NAME=?", [score, player_name], update=True)

    def get_scores(self, start, count) -> list:
        return self.query_db("select * from SCORES order by SCORE DESC")[start:count]

    def get_player(self, username) -> Player:
        return self.query_db("select * from SCORES where NAME = ?", [username], True)
