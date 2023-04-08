def decrypt(message):
    """
    This function decrypts a message using a known decryption key.
    """
    key = 5  # known decryption key
    decrypted = ""
    for character in message:
        if character.isalpha():
            code = ord(character)
            code = code - key
            if character.isupper():
                if code < ord('A'):
                    code = code + 26
                elif code > ord('Z'):
                    code = code - 26
            elif character.islower():
                if code < ord('a'):
                    code = code + 26
                elif code > ord('z'):
                    code = code - 26
            decrypted += chr(code)
        else:
            decrypted += character
    return decrypted
