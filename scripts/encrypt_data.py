#!/usr/bin/env python3
import time
import json
import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class RSAUtil:
    rsa_key = "RSA"
    transformation = "RSA/ECB/PKCS1Padding"
    max_encrypt_byte = 117
    max_decrypt_type = 128

    @staticmethod
    def sign_by_sha256_with_rsa(data, private_key):
        key_bytes = base64.b64decode(private_key)
        pri_key = RSA.import_key(key_bytes)
        h = SHA256.new(data.encode())
        signature = pkcs1_15.new(pri_key).sign(h)
        return base64.b64encode(signature).decode()

    @staticmethod
    def verify_sha256_with_rsa(data, signature_to_be_verified, public_key):
        key_bytes = base64.b64decode(public_key)
        pub_key = RSA.import_key(key_bytes)
        h = SHA256.new(data.encode())
        signature = base64.b64decode(signature_to_be_verified)
        try:
            pkcs1_15.new(pub_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def big_encrypt_by_public_key(input_text, rsa_public_key):
        key_bytes = base64.b64decode(rsa_public_key)
        public_key = RSA.import_key(key_bytes)
        cipher = PKCS1_v1_5.new(public_key)
        input_bytes = input_text.encode()
        encrypted_data = b""
        for i in range(0, len(input_bytes), RSAUtil.max_encrypt_byte):
            chunk = input_bytes[i : i + RSAUtil.max_encrypt_byte]
            encrypted_chunk = cipher.encrypt(chunk)
            encrypted_data += encrypted_chunk
        return base64.b64encode(encrypted_data).decode()

    @staticmethod
    def big_decrypt_by_private_key(text, private_key):
        key_bytes = base64.b64decode(private_key)
        private_key = RSA.import_key(key_bytes)
        cipher = PKCS1_v1_5.new(private_key)
        encrypted_data = base64.b64decode(text)
        decrypted_data = b""
        for i in range(0, len(encrypted_data), RSAUtil.max_decrypt_type):
            chunk = encrypted_data[i : i + RSAUtil.max_decrypt_type]
            decrypted_chunk = cipher.decrypt(chunk, None)
            decrypted_data += decrypted_chunk
        return decrypted_data.decode()


# Example Usage:
data = {
    "headMerchantId": "256622070716625",
    "merchantId": "256623091343434",
    "outOrderNo": "1219",
    "amount": "3000",
    "currency": "NGN",
    "orderExpireTime": 180,
    "sceneEnum": "CASH_API",
    "subSceneEnum": "ORDER",
    "sn": "98220417981802",
}

json_data = json.dumps(data)
private_key = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAItdfLhGP+Hd7rL/H4fxR2PxSyCyOMRVrKbs9Dv5nBc9wWMpVlxnkkM4ZGlGLDhwTPr2S+AWWGgPFVcBRj2o4dzEHZ8rZCpzrfmlPbjEaI2QsQTqnlDxVOepLqijh/rttBrGGYDSOacWztCYjo02dFutMteCKfxMPOlVfyBkz+xDAgMBAAECgYAlfP9YnmT+v/E+qwvzSH74rmaUI/zLK3Sm7mSAYZOQWOdVYkA92QpqFJhGDT9F60d51pjwbXJYg34tCkW3vl8K1vss2g2XqQp8FwJN9NRRkhJVlLnYypff2MYNsrvVI9ey2bE7uKOx6sE/SiY1qRnTqUMLiXazMg/liJS/EyPqCQJBAPoha0fIIC3s20J1q+dfb2WV46NTIzt73zt8Ci+Vl6NCqebo3d198eHT2sFmOkukDb6dsJkukbTXXeVZTxNsjw8CQQCOoq4OLiF/atC7akVOgLnRp53FSm4xrX2x6CNxs+sHOa7FfFTNkAiVQXJ5FG6iY0QG6RMnRqhIRHwrRJ9wKM+NAkAS6VHuJHBiaIUPWkw7+xg2CwYiBBgm2C/BlJhEjr/fRRwJbFPR+kK+e0EP3EXOEEJFxjBi9IVpsdrUi1MSOeP7AkAlLxnLDpGjAvipcxngTkSi+Fxz+2RgxQa4o3jiAnJp7sq2JySAdmUWa/powD/bS5+HYamhmpTyShBIw1oBRlJdAkEAqqPUJ1APOBzZncxFhwt8dniAm/xTp90Wof3aatli2RseFL+PMNPev8fprShIrxeLae87gf3VXqQandoMu4jgjg=="
rsa_public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC7QCbAn4Qv8YqM3iDLFyfWJKVrXVh4AidGR/KxlFA/YFce3qHgOLJhGDLpEi8rVOMkvpBS/5jzYs8Cx7jaW8G9dDUopL9Yjc+/+60/k++KLQpbfNNfuSZYLfqYQmMLAI7V32kEU/9KRUD9l1m7DrGLNZ1pnbIrciFnKA/buuQoOwIDAQAB"

# Encrypt and Decrypt
print(json_data)
encrypted_data = RSAUtil.big_encrypt_by_public_key(json_data, rsa_public_key)
print("Encrypted Data:", encrypted_data)

timestamp = f"{round(time.time() * 1000)}"

print(timestamp)

data_to_sign = encrypted_data + timestamp

# Sign and Verify
signature = RSAUtil.sign_by_sha256_with_rsa(data_to_sign, private_key)
print("Signature:", signature)
