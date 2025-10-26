import sqlite3
import os
from datetime import datetime

class DatabaseController:
    def __init__(self):
        self.con, self.cur = self.start_database()

    def start_database(self):
        db_path = "Server/devices.db"
        if not os.path.isfile(db_path):
            _con = sqlite3.connect(db_path, check_same_thread=False)
            _cur = _con.cursor()
            _cur.execute("CREATE TABLE devices (pass_key TEXT)")
            _con.commit()
        else:
            _con = sqlite3.connect(db_path, check_same_thread=False)
            _cur = _con.cursor()
        return _con, _cur

    def add_device(self, guid):
        self.cur.execute("INSERT INTO devices (pass_key) VALUES (?)", (str(guid),))
        self.con.commit()
        print("Device added!")

    def add_session(self, auth_key):
        session_start = datetime.now()
        self.cur.execute("INSERT INTO sessions (auth_key, session_start, session_valid) VALUES (?, ?, ?)",
                            (auth_key, session_start, 1,))
        return auth_key

    def validate_user(self, guid):
        self.cur.execute('SELECT pass_key FROM devices WHERE pass_key == ?', (str(guid),))
        self.con.commit()
        result = self.cur.fetchone()
        return result is not None and result[0] == str(guid)
    
    def validate_token(self, token):
        self.cur.execute('SELECT auth_key FROM sessions WHERE session_valid == 1 AND auth_key == ?', (str(token),))
        self.con.commit()
        result = self.cur.fetchall()
        return result is not None and str(token) in [r[0] for r in result]