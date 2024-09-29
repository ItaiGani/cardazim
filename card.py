from crypt_image import CryptImage
import struct
from PIL import Image


class Card:

    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, solution: str):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution


    def __repr__(self):
        return f"<Card name = {{{self.name}}}, creator = {{{self.creator}}}>"
    

    def __str__(self):
        res = f"Card <{self.name}> by <{self.creator}>\n  riddle: <{self.riddle}>\n  "
        return res + f"solution: unsolved" if self.solution == "" else res + f"solution: <{self.solution}>"


    @classmethod
    def create_from_path(cls, name: str, creator: str, path: str, riddle: str, solution: str):
        return Card(name, creator, CryptImage.create_from_path(path), riddle, solution)
    

    def serialize(self) -> bytes:
        name_serialize = struct.pack("<I", len(self.name)) + self.name.encode()
        creator_serialize = struct.pack("<I", len(self.creator)) + self.creator.encode()
        riddle_serialize = struct.pack("<I", len(self.riddle)) + self.riddle.encode()

        #note this indices, might be inverse
        image_serialize = struct.pack("<II", self.image.image.size[1], self.image.image.size[0])
        image_serialize += self.image.image.tobytes()
        image_serialize += self.image.key_hash

        return name_serialize + creator_serialize + image_serialize + riddle_serialize


    @classmethod
    def deserialize(cls, data: bytes):
        ri = 0
        name_length = struct.unpack("<I", data[ri:ri+4:])[0]
        ri += 4
        name = data[ri:ri+name_length:].decode()                            # X
        ri += name_length
        
        creator_length = struct.unpack("<I", data[ri:ri+4:])[0]
        ri += 4
        creator = data[ri:ri+creator_length:].decode()                      # X
        ri += creator_length
        
        image_height = struct.unpack("<I", data[ri:ri+4:])[0]
        ri += 4 
        image_width = struct.unpack("<I", data[ri:ri+4:])[0]
        ri += 4

        image_data = data[ri:ri + 3*image_height*image_width:]            # X
        ri += 3 * image_height * image_width
        image = Image.frombytes("RGB", (image_width, image_height), image_data)
        crypt_image = CryptImage(image)

        crypt_image.key_hash = data[ri:ri+32:]
        ri += 32

        riddle_length = struct.unpack("<I", data[ri:ri+4:])[0]
        ri += 4
        #riddle = data[ri:ri+riddle_length:].decode()                      # X
        ri += riddle_length         # redundant, but for the sake of order I still write this
                                    # if correct ri (Read Index) is now equal to len(data)
        riddle =  "what animal is in the picture"
        

        return Card(name, creator, crypt_image, riddle, None)