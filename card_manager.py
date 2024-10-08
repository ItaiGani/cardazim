from card import Card
from CardDriver import CardDriver
from fsDriver import fsDriver
from SQLDriver import SQLDriver
import pathlib
from furl import furl
import os



class CardManager:
    
    def __init__(self, database_url: str, images_dir: str):
        self.driver: CardDriver = CardManager.get_driver(database_url)
        self.images_dir = pathlib.Path(images_dir)

        # creating images dir
        p = self.images_dir / "unsolved"
        p.mkdir(parents=True, exist_ok=True)
        p = self.images_dir / "solved"
        p.mkdir(parents=True, exist_ok=True)


    def save(self, card: Card):
        is_solved_dir = "unsolved" if card.solution == None else "solved"
        image_path = self.images_dir / f"{is_solved_dir}/{card.generate_identifier()}.png"
        card.image.save(image_path)  
        self.driver.save(card, os.fspath(image_path))
        print(f"Saved card and image successfully.")


    def load(self, identifier: str) -> Card:
        return self.driver.load(identifier)
        

    def getCreators(self):
        return self.driver.getCreators()
    

    def getCreatorCards(self, creator: str):
        return self.driver.getCreatorCards(creator)
    

    @classmethod
    def get_driver(cls, database_url: str) -> CardDriver:
        """parse url and return which driver we should use"""
        f = furl(database_url)
        if f.scheme == "sql":
            return SQLDriver(f.netloc)
        elif f.scheme == "filesystem":
            return fsDriver(f.netloc)