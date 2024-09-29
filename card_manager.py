from card import Card
import json
import pathlib

class CardManager:

    def __init__(self):
        self.path = ""


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