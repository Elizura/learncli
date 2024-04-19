from dataclasses import dataclass
from injector import inject
import sqlite3


@dataclass
class State:
    level:str
    qno:int    

@dataclass
@inject
class DBRepo:
    def __init__(self):        
        self.conn = sqlite3.connect("state.db")
        self.cur = self.conn.cursor()
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Status (
                level INTEGER,
                qno INTEGER
            )
        ''')
        self.cur.execute('SELECT COUNT(*) FROM Status')
        result = self.cur.fetchone()

        if result[0] == 0:
            self.cur.execute('''
                INSERT INTO Status (level, qno) VALUES (?, ?)
            ''', (1, 1))

        self.conn.commit()        


    def get_status(self) -> State:            
        return self.cur.execute("SELECT * FROM Status").fetchall()[0]      
        # return [
        #     State(
        #         level=dt[0],
        #         qno=dt[1]                
        #     )
        #     for dt in self.cur.execute("SELECT * FROM Status").fetchall()
        # ]
    
    def set_status(self, level, qno):        
        cur_level, cur_qno = self.get_status()
        self.cur.execute("UPDATE Status SET level = ?, qno = ? WHERE level = ? AND qno = ?", (level, qno, cur_level, cur_qno))
        self.conn.commit()

    def reset_status(self):
        self.set_status(1, 1)


