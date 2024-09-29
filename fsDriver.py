from CardDriver import CardDriver

class fsDriver(CardDriver):
    
    def __init__(self, dir: str):
        self.dir = None

    def set_dir(self, dir: str):
        self.dir = dir
