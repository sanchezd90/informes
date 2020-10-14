import hashlib

hash_passwords= hashlib.pbkdf2_hmac('sha512', p.encode('utf-8'), b'salt', 100000).hex()