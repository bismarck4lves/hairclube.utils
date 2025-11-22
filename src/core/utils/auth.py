from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import base64


key_crypt = "RecomeceSeDerErrado"
saltArray = b"security hidden"
iterations = 10000  #


def encode(clear_text: str) -> str:
    try:
        password = key_crypt.encode("utf-8")

        key_iv = PBKDF2(
            password, saltArray, dkLen=48,
            count=iterations,
            hmac_hash_module=SHA256
        )
        key = key_iv[:32]
        iv = key_iv[32:]

        cipher = AES.new(key, AES.MODE_CBC, iv)

        clear_bytes = clear_text.encode("utf-16le")

        encrypted = cipher.encrypt(pad(clear_bytes, AES.block_size))

        return base64.b64encode(encrypted).decode("utf-8")
    except Exception:
        return ""


def decode(cipher_text: str) -> str:
    try:
        cipher_text = cipher_text.replace(" ", "+")
        encrypted_bytes = base64.b64decode(cipher_text)

        password = key_crypt.encode("utf-8")
        key_iv = PBKDF2(password, saltArray, dkLen=48, count=iterations, hmac_hash_module=SHA256)
        key = key_iv[:32]
        iv = key_iv[32:]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

        # .NET usa UTF-16 LE
        return decrypted.decode("utf-16le")

    except:
        return ""
