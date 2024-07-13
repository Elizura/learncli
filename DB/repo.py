from dataclasses import dataclass
from injector import inject
import sqlite3


@dataclass
class State:
    level: str
    qno: int


@dataclass
@inject
class DBRepo:
    def __init__(self):
        self.conn = sqlite3.connect("/learncli/state.db")
        self.cur = self.conn.cursor()

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Status (
                level INTEGER,
                qno INTEGER
            )
        """
        )
        self.cur.execute("SELECT COUNT(*) FROM Status")
        result = self.cur.fetchone()

        if result[0] == 0:
            self.cur.execute(
                """
                INSERT INTO Status (level, qno) VALUES (?, ?)
            """,
                (1, 1),
            )

        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS app_usage(                
                    first_run BOOLEAN
                )
            """
        )
        self.conn.commit()

    def get_status(self) -> State:
        return self.cur.execute("SELECT * FROM Status").fetchall()[0]

    def set_status(self, level, qno):
        cur_level, cur_qno = self.get_status()
        self.cur.execute(
            "UPDATE Status SET level = ?, qno = ? WHERE level = ? AND qno = ?",
            (level, qno, cur_level, cur_qno),
        )
        self.conn.commit()

    def reset_status(self):
        self.set_status(1, 1)

    def is_first_run(self):
        self.cur.execute('SELECT COUNT(*) FROM app_usage WHERE first_run = 1')
        res = self.cur.fetchone()
        is_first_run = res[0] == 0
        return is_first_run

    def mark_as_run(self):
        self.cur.execute('INSERT INTO app_usage (first_run) VALUES (1)')
        self.conn.commit()
