from PIL import Image
from Crypto.Cipher import AES
import hashlib



class CryptImage():

    def __init__(self, image: Image = None):
        self.image = image
        self.key_hash = None
        self.nonce = b'arazim'


    @classmethod
    def create_from_path(cls, path):
        im = Image.open(path)
        im = im.convert("RGB")
        return CryptImage(im)
    

    def encrypt(self, key: str) -> None:
        encryption_key = hashlib.sha256(key.encode()).digest()
        self.key_hash = hashlib.sha256(encryption_key).digest()   # applying sha256 twice

        img_binary = self.image.tobytes()
        cipher = AES.new(encryption_key, AES.MODE_EAX, self.nonce)
        encrypted_data = cipher.encrypt(img_binary)
        
        self.image = Image.frombytes(self.image.mode, self.image.size, encrypted_data)


    def decrypt(self, key: str):
        encryption_key = hashlib.sha256(key.encode()).digest()
        if hashlib.sha256(encryption_key).digest() != self.key_hash:
            print("------------Wrong key-------------")
            return
        
        encrypted_data = self.image.tobytes()
        cipher = AES.new(encryption_key, AES.MODE_EAX, self.nonce)
        decrypted_data = cipher.decrypt(encrypted_data)
        self.image = Image.frombytes(self.image.mode, self.image.size, decrypted_data)
        self.key_hash = None

    
    def save(self, path):
        self.image.save(path)