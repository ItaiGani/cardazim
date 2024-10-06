from CardDriver import CardDriver
from card import Card
import sqlite3 as sq


table_name = "metadata"

class SQLDriver(CardDriver):

    def __init__(self, db: str):
        self.con = sq.connect(db, check_same_thread = False) # Should ask if we need to use locks or something like that
        self.cur = self.con.cursor()
        if self.cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table'
                            AND name='{table_name}'; """).fetchall()  == []:
            self.cur.execute("CREATE TABLE metadata(\
                            id varchar(511),\
                            name varchar(255),\
                            creator varchar(255),\
                            riddle varchar(511),\
                            solution varchar(511),\
                            image_path varchar(511));")
        

    def save(self, card: Card, image_path):
        self.cur.execute(f"""INSERT INTO metadata VALUES('{card.generate_identifier()}','{card.name}', '{card.creator}', '{card.riddle}', '{card.solution}', '{image_path}')""")
        self.con.commit()


    def load(self, identifier: str) -> Card:
        data = self.cur.execute(f"""SELECT * FROM {table_name} WHERE id = '{identifier}'""").fetchone()
        return Card.create_from_path(data[1], data[2], data[5], data[3], data[4])


    def getCreators(self) -> set[str]:
        creators = self.cur.execute(f"""SELECT creator FROM {table_name} GROUP BY creator""")
        return set(creators)


    def getCreatorCards(self, creator: str) -> list[Card]:
        cards = self.cur.execute(f"""SELECT * FROM {table_name} WHERE creator = '{creator}'""").fetchall()
        return [Card.create_from_path(data[1], data[2], data[5], data[3], data[4]) for data in cards]