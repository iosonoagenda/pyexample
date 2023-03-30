import hashlib
import secrets

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = hashlib.sha256(master_password.encode()).hexdigest()
        self.passwords = {}

    def add_password(self, service, username, password):
        salt = secrets.token_bytes(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        encrypted_password = salt + key
        self.passwords[(service, username)] = encrypted_password

    def get_password(self, service, username):
        if (service, username) not in self.passwords:
            raise ValueError("Password not found for given service and username")

        encrypted_password = self.passwords[(service, username)]
        salt = encrypted_password[:16]
        key = encrypted_password[16:]
        password_attempt = hashlib.pbkdf2_hmac('sha256', self.master_password.encode(), salt, 100000)

        if key != password_attempt:
            raise ValueError("Invalid master password")

        return key

    def delete_password(self, service, username):
        if (service, username) not in self.passwords:
            raise ValueError("Password not found for given service and username")

        del self.passwords[(service, username)]
