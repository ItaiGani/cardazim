from PIL import Image
from Crypto.Cipher import AES
import hashlib

class CryptImage():

    def __init__(self, path):
        self.image = Image.open(path)
        self.key_hash = None

    @classmethod
    def create_from_path(cls, path):
        return 
    
    def encrypt(self, key: str) -> None:
        key = key.encode()
        encryption_key = hashlib.sha256(key).digest()
        self.key_hash = hashlib.sha256(encryption_key).digest()   # applying sha256 twice

        nonce = "arazim"
        plaintext = self.image.getdata()
        #cipher = AES.new(key, AES.MODE_EAX, nonce = bytes(nonce))
        #encrypted = cipher.encrypt(plaintext)
        self.image.putdata([0 for i in range(len(plaintext)//2)])
        self.image.save("abc.png")
        
