import hashlib

def generar_pass(p):
    return hashlib.pbkdf2_hmac('sha512', p.encode('utf-8'), b'salt', 100000).hex()

print(generar_pass("agaliani"))