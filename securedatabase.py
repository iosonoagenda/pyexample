import hashlib
import secrets

class SecureDatabase:
    def __init__(self, master_password):
        self.master_password = hashlib.sha256(master_password.encode()).hexdigest()
        self.database = {}

    def add_data(self, key, data):
        nonce = secrets.token_bytes(16)
        key = hashlib.pbkdf2_hmac('sha256', key.encode(), nonce, 100000)
        ciphertext = self._encrypt(data, key, nonce)
        self.database[key] = (nonce, ciphertext)

    def get_data(self, key):
        nonce, ciphertext = self.database.get(hashlib.pbkdf2_hmac('sha256', key.encode(), self.master_password.encode(), 100000))
        return self._decrypt(ciphertext, key, nonce)

    def delete_data(self, key):
        del self.database[hashlib.pbkdf2_hmac('sha256', key.encode(), self.master_password.encode(), 100000)]

    def _encrypt(self, data, key, nonce):
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_data = self._pad(data)
        return encryptor.update(padded_data) + encryptor.finalize()

    def _decrypt(self, ciphertext, key, nonce):
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        return self._unpad(padded_data)

    def _pad(self, data):
        block_size = algorithms.AES.block_size // 8
        padding_size = block_size - len(data) % block_size
        padding = bytes([padding_size] * padding_size)
        return data + padding

    def _unpad(self, padded_data):
        padding_size = padded_data[-1]
        return padded_data[:-padding_size]
