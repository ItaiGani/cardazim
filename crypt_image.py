from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import io



class CryptImage():

    def __init__(self, path):
        self.image = Image.open(path)
        self.key_hash = None
        self.nonce = b'arazim'


    @classmethod
    def create_from_path(cls, path):
        return CryptImage(path)
    

    def encrypt(self, key: str) -> None:
        encryption_key = hashlib.sha256(key.encode()).digest()
        self.key_hash = hashlib.sha256(encryption_key).digest()   # applying sha256 twice

        img_binary = self.image.tobytes()
        cipher = AES.new(encryption_key, AES.MODE_EAX, self.nonce)
        encrypted_data = cipher.encrypt(img_binary)
        
        self.image = Image.frombytes(self.image.mode, self.image.size, encrypted_data)
        self.image.save("abc.png")


    def decrypt(self, key: str):
        encryption_key = hashlib.sha256(key.encode()).digest()
        if hashlib.sha256(encryption_key).digest() != self.key_hash:
            print("------------Wrong key-------------")
            return
        
        
        encrypted_data = self.image.tobytes()
        cipher = AES.new(encryption_key, AES.MODE_EAX, self.nonce)
        decrypted_data = cipher.decrypt(encrypted_data)
        # decrypted_data = unpad(decrypted_data, AES.block_size)
        # decrypted_image = Image.open(io.BytesIO(decrypted_data))
        # decrypted_image.save("abc.png", format=decrypted_image.format)
        self.image = Image.frombytes(self.image.mode, self.image.size, decrypted_data)
        self.image.save("abc.png")
        self.key_hash = None