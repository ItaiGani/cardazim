from card import Card
import json
import pathlib
from CardDriver import CardDriver
from fsDriver import fsDriver

class CardManager:
    
    def __init__(self, database_url: str, images_dir: str):
        self.path = ""
        self.driver: CardDriver = CardManager.get_driver(database_url)
        self.images_dir = images_dir


    def save(self, card: Card, dir_path: str = "."):
        self.path = dir_path + "/" + self.generate_identifier(card)
        p = pathlib.Path(self.path)
        p.mkdir(parents=True, exist_ok=True)
        card.image.save(self.path + "/im.png")
        
        data = {
            "name": card.name,
            "creator": card.creator,
            "riddle": card.riddle,
            "solution": card.solution,
            "path": self.path
        }
        json_object = json.dumps(data, indent=4)
        with open(self.path + "/metadata.json", "w") as outfile:
            outfile.write(json_object)
        print(f"Saved card to path ‘./data/unsolved_cards/{self.generate_identifier(card)}’.")


    def generate_identifier(self, card: Card) -> str:
        return card.creator + "_" + card.name


    def load(self, dirpath: str, identifier: str) -> Card:
        with open(dirpath + "/" + identifier + "/metadata.json", 'r') as file:
            data = json.load(file)
            card = Card.create_from_path(data["name"], data["creator"], dirpath + "/" + identifier + "/im.png", data["riddle"], data["solution"])
            return card
        

    @classmethod
    def get_driver(database_url: str) -> CardDriver:
        """function to parse the url and understand which driver we should use"""
        return fsDriver()