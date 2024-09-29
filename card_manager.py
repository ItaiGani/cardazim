from card import Card
from CardDriver import CardDriver
from fsDriver import fsDriver
import pathlib


class CardManager:
    
    def __init__(self, database_url: str, images_dir: str):
        self.driver: CardDriver = CardManager.get_driver(database_url)
        self.images_dir = images_dir

        # creating images dir
        p = pathlib.Path(self.images_dir + "/unsolved")
        p.mkdir(parents=True, exist_ok=True)
        p = pathlib.Path(self.images_dir + "/solved")
        p.mkdir(parents=True, exist_ok=True)


    def save(self, card: Card):
        is_solved_dir = "unsolved" if card.solution == None else "solved"
        image_path = f"{self.images_dir}/{is_solved_dir}/{CardManager.generate_identifier(card)}.png"
        card.image.save(image_path)  
        self.driver.save(card, image_path)
        print(f"Saved card and saved card image to path ‘{image_path}’.")


    def load(self, identifier: str) -> Card:
        return self.driver.load(identifier)
        

    def getCreators(self):
        return self.driver.getCreators()
    

    def getCreatorCards(self, creator: str):
        return self.driver.getCreatorCards(creator)

 
    @classmethod
    def generate_identifier(cls, card: Card) -> str:
        return card.creator + "_" + card.name
    

    @classmethod
    def get_driver(cls, database_url: str) -> CardDriver:
        """parse url and return which driver we should use"""
        return fsDriver("/home/pogo-arazim/Documents/arazim0/cardazim/metadata_cards")