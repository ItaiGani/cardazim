from CardDriver import CardDriver
from card import Card
import sqlite3 as sq
import threading


table_name = "metadata"

# note: I just use lock on every function 
# note: Better to use context manager to implement the usage of the lock + cursor, but I dont have the mentality for that right now
class SQLDriver(CardDriver):

    def __init__(self, db: str):
        self.con = sq.connect(db, check_same_thread = False)
        self.lock =threading.Lock()

        cur = self.con.cursor()
        if cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table'
                            AND name='{table_name}'; """).fetchall()  == []:
            cur.execute("CREATE TABLE metadata(\
                            id varchar(511),\
                            name varchar(255),\
                            creator varchar(255),\
                            riddle varchar(511),\
                            solution varchar(511),\
                            image_path varchar(511));")
        cur.close()


    def save(self, card: Card, image_path):
        self.lock.acquire()
        cur = self.con.cursor()
        cur.execute(f"""INSERT INTO metadata VALUES('{card.generate_identifier()}','{card.name}', '{card.creator}', '{card.riddle}', '{card.solution}', '{image_path}')""")
        self.con.commit()
        cur.close()
        self.lock.release()


    def load(self, identifier: str) -> Card:
        self.lock.acquire()
        cur = self.con.cursor()
        data = cur.execute(f"""SELECT * FROM {table_name} WHERE id = '{identifier}'""").fetchone()
        cur.close()
        self.lock.release()
        return Card.create_from_path(data[1], data[2], data[5], data[3], data[4])


    def getCreators(self) -> set[str]:
        self.lock.acquire()
        cur = self.con.cursor()
        creators = cur.execute(f"""SELECT creator FROM {table_name} GROUP BY creator""")
        cur.close()
        self.lock.release()
        return set(creators)


    def getCreatorCards(self, creator: str) -> list[Card]:
        self.lock.acquire()
        cur = self.con.cursor()
        cards = cur.execute(f"""SELECT * FROM {table_name} WHERE creator = '{creator}'""").fetchall()
        cur.close()
        self.lock.release()
        return [Card.create_from_path(data[1], data[2], data[5], data[3], data[4]) for data in cards]
    

    def getCards(self):
        self.lock.acquire()
        cur = self.con.cursor()
        cards = cur.execute(f"""SELECT * FROM {table_name}""").fetchall()
        cur.close()
        self.lock.release()
        return [Card.create_from_path(data[1], data[2], data[5], data[3], data[4]) for data in cards]