from CardDriver import CardDriver
from card import Card
import json
import pathlib
import os


class fsDriver(CardDriver):
    
    def __init__(self, dir: str):
        self.dir = pathlib.Path(dir)

        # making the dir
        self.dir.mkdir(parents=True, exist_ok=True)


    def save(self, card: Card, image_path):
        data = {
            "name": card.name,
            "creator": card.creator,
            "riddle": card.riddle,
            "solution": card.solution,
            "path": image_path
        }
        json_object = json.dumps(data, indent=4)
        with open(self.dir / f"{card.generate_identifier()}.json", "w") as outfile:
            outfile.write(json_object)


    def load(self, identifier: str) -> Card:
        if os.path.isfile(self.dir / f"{identifier}.json"):
            with open(self.dir / f"{identifier}.json") as file:
                data = json.load(file)
                return Card.create_from_path(data["name"], data["creator"], data["path"], data["riddle"], data["solution"])
        else:
            print("Card does not exist.")
            exit(1)


    def getCreators(self) -> set[str]:
        cards = os.listdir(self.dir)
        return set([card.split("_")[0] for card in cards])


    def getCreatorCards(self, creator: str) -> list[Card]:
        cards = os.listdir(self.dir)
        return [self.load(card[:-5:]) for card in cards if creator == card.split("_")[0]]
    
    
    def getCards(self) -> list[Card]:
        cards = os.listdir(self.dir)
        return [self.load(card[:-5:]) for card in cards]