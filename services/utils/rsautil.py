import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from collections import OrderedDict
from urllib.parse import urlencode
import json

# PRIVATE_KEY = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAItdfLhGP+Hd7rL/H4fxR2PxSyCyOMRVrKbs9Dv5nBc9wWMpVlxnkkM4ZGlGLDhwTPr2S+AWWGgPFVcBRj2o4dzEHZ8rZCpzrfmlPbjEaI2QsQTqnlDxVOepLqijh/rttBrGGYDSOacWztCYjo02dFutMteCKfxMPOlVfyBkz+xDAgMBAAECgYAlfP9YnmT+v/E+qwvzSH74rmaUI/zLK3Sm7mSAYZOQWOdVYkA92QpqFJhGDT9F60d51pjwbXJYg34tCkW3vl8K1vss2g2XqQp8FwJN9NRRkhJVlLnYypff2MYNsrvVI9ey2bE7uKOx6sE/SiY1qRnTqUMLiXazMg/liJS/EyPqCQJBAPoha0fIIC3s20J1q+dfb2WV46NTIzt73zt8Ci+Vl6NCqebo3d198eHT2sFmOkukDb6dsJkukbTXXeVZTxNsjw8CQQCOoq4OLiF/atC7akVOgLnRp53FSm4xrX2x6CNxs+sHOa7FfFTNkAiVQXJ5FG6iY0QG6RMnRqhIRHwrRJ9wKM+NAkAS6VHuJHBiaIUPWkw7+xg2CwYiBBgm2C/BlJhEjr/fRRwJbFPR+kK+e0EP3EXOEEJFxjBi9IVpsdrUi1MSOeP7AkAlLxnLDpGjAvipcxngTkSi+Fxz+2RgxQa4o3jiAnJp7sq2JySAdmUWa/powD/bS5+HYamhmpTyShBIw1oBRlJdAkEAqqPUJ1APOBzZncxFhwt8dniAm/xTp90Wof3aatli2RseFL+PMNPev8fprShIrxeLae87gf3VXqQandoMu4jgjg=="


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


class OpayApiConstants:
    SIGN = "sign"


class StringUtils:
    @staticmethod
    def get_sign_content(data):
        sorted_params = OrderedDict(sorted(data.items()))
        content = []

        for key, value in sorted_params.items():
            if (
                key is None
                or key == ""
                or value is None
                or key == OpayApiConstants.SIGN
            ):
                continue
            content.append(f"{key}={value}")

        return "&".join(content)


# data = "QypW6radUREsvBQhUbj+TBQ+SJEnWpy5qTjWItxh5xm9DJS3a7BYypbSi4/pZm2hSugDniHj6KbrT6HFohznPq85MEWSmb0NQ157VS6h+eQ2pOL9smhUX9VrSyWfMDF9dbEUWQLHwzpqDOeDP0rEB9BIBNmXSRi9rznSpfatPyF+ugm7wWY2Cfu9Dj54PYAKPi0QoN9lBmUR6qjPsrnaEUx5jTrpzPr1DokpaTHH5/fQdSZ0K2QScReguLqZw7/kaHb6MLVFs4i3JDcZPRy5E3oOPC/p2BwYr0YFcGYLY71yOkmPlWzUx9R5bRJo+In7ZkQx8p+KbPJyMZZWDElPKBFif8jXIIGVrNXGhTzLeJI52MfhoqRE2LIeoKjSAmqfnrTkGwfkKy2c2ziJnPtSxEpHN3S++OhRjGf+R9O9JRwits1E8tcjMKtx9QnVYSNe4cykKFIZdRt4lT32zzc+RftfdT7c/v3k1fO2O+Xj7N7gKGInpj/aOOXAFGWVmZhYBd0tBvTZmFNIJrzqmq0Ap9DwxwZoxZ5VqolrgFkwv9+2U+gXM+cLtGxtwqCcovf5s14ZTgOo+FMnxggQB7zO2Bp1FBnYHc4Uo0A5HqAL3TYzE/KR3cH4XAfGOOD8QuVoTuNR1Am1BcsRiBhPow6lf60w2a5aYi/OcTwHeBHS0Bt3uMQQWq66YA03PlECmW7648PcZy5eDEW+74giZkcrxJxv4XnvTwUpRvqDo9MVPp428Lpy1GJ/yXYaJxExjs3C48zXmrIzbM97Jftswj/7aERG95axak+GOMy0XZzWkhtlZnhtOXMV/rIIILUirX++OpFw6wduwdxPgFWkngYuyy4iT2rEmR8fv9ZdMs6kMDTySAW7muyt610qZ+yPZjHKSJK5EhpcCsNZf8CSnpvAnMZ2K+rzQ3AKBiD4nzR+KoPILaGv+n50Ow2/3SY14fl3s2igG4bPionnCWXLUkP7pBP2o+ftsO073/+fCbEI3FKAmvX72QWK0xd+as5QTVdp"
# content = RSAUtil.big_decrypt_by_private_key(data, PRIVATE_KEY)

# dd = json.loads(content)
# print(dd, type(dd))

# 20231226937113402337574912 Order No
# sing = "mLJSxUStleHcA/IX5NLIoED+5Ezskj/MSGUGOjGQ2Zffds/HVCz6H80AtHQ7zCQoNx5r5ImFVYSmGEw0nm+zl5qm4gDMSlD91+9JjI/e6JiIQssLJa17ELwFU8rf21YFYV0A3sN6vbBppZCZGuxSnuyFgk/hIaieCwSLndGmjKY="
# {'orderNo': '20231227937442649484738560'}} RESPONSE "20231227937442649484738560"

#  {'data': 'LKQJOJXRBXiSRICGZBKcD2ZvRTmw44bZOmSsuYzmBLIB0gjDTOumCTW/D07VeEYj8jMtIDa+hyqhTVUIA1mUeMRnf/22La5cwpNHr058jcBRT+YQU+9HX3n8H/YINafbI/OehkRyf3TLhabjlRdo2SZbEVHt+Zu6O77RDJqWFYRVO8aj1KsgEdttg8k4PaP6J2l5eRDSQ82agJEDx2v+flbXurXLRDvcfyOkoprWqXV2E3oP9I4GeCb0aAkKi3a0bJy7X71iPgy5UZxBF/lQ8ihwJ7noCk4pVIdZJK8c7SGu4mRLvmc5UqbXzr/dPjPriqeNcJGxkPV4l35qC/v4+X/VR3Sb3j56DMrgLdzptXk/tAvfPw+00dR8P5FKr/X2GLBbubgqKl84nnjqzNnWaGlbj9o/q65F3wBKdKfhRVgU+hgOQQjatfOeHFhJ/tHKXfhhD8LtVR3PAKpcoaif0PvaSdndXiiGo9S4xWhDdkpuhYlOWUvWe/KskB2e6VvoiWccADjmy90pqOb0158SNwcsf0TL86c2dbxh5oef7/6OZr46CxZLYKdCvnsfo1dtA5IJGfOQh5PMfHoEhs6rCAfFAYj7pSeGIJ6LbnhyjSms8akAZgT8zUNYgu+1P8FMz2e6vxl7EVCp2yWiveMOIgusvK8VwsW521ChpZUkB2CFwT2ntt2rHptvIjAK6goZPLSIshy7l+sdp6gkjayYGkQBiI86DcCsAjJcu7fnuajlrZJNEAuyLX7LMhSYOQXmbJAbCawOc4VGGyKG02kExKlvCcf2bAyB+fqpDsSC4h4RvtRiUUAY84ZX1UL0cU81fCjq9EaccDICL7/9THVf/T/nBMLrt8d8a7cTZn7JSygFdFQfsTT5fQnaZFtmHIOQyrVMGLNNqGTyIHdssZrspaLkmZDnx9dsGl3H+PHDAdOqDGsE+hwMbo8FxyhSid/YRvM5EejJSAaOMwLtdBZYRL5QWi5LzqDWSNbPgWvwcb91a1h65gW/XZIFweh4+dvMB48S7y4a9lRhhuag+gvmmja4lEjEZaCH3gQ4ZDtp13GwpEl/NRpxpIeBB5NKBJVMI2PbTdMm7p3aFql8wfugtt/3ZiXTLdlkL14tHYJ7dDTAFbVwXpK6Ika+QUpGcXLgfJLqUjDzgSEbyYO5aShOIRDihwMfAY9lwi7adCLONPA='}
# Dec 27 09:44:14 ip-10-1-1-118 daphne[65145]: 2023-12-27 09:44:14,784 INFO     {"feePattern":"IN_DEDUCT","senderAccount":"524282******2376","amount":"50.00","orderNo":"20231227937442649484738560","completedTime":"1703670248000","fee":"0.25","sign":"Sd+B/eTXWoPk9mGZZB6k6ko7gdYoXUgLxDQn5Y7kdYbx8ZT1JU9G2hP6zHR0nGYUwimOV7CONKbyMj/xcyZ/Xx3hin3yReqntMYLhP3jP6b3y2NXna8G1uQfD2dZNoLo7JqZlF8Phn0di42IXqOy1cjZ4/BO/F0b3oF4IvMgc+A=","remark":"POS_INWARD","transactionTime":"1703670248000","recipientBank":"","errorMsg":"Approved or completed successfully","payNo":"231227051484836736","senderName":"","merchantId":"256623091343434","payMethod":"BankCard","recipientAccount":"","recipientName":"AAJ EXPRESS ONLINE PAYMENT","currency":"NGN","headMerchantId":"256622070716625","sn":"98220417981802","senderBank":"","status":"SUCCESS"}
# Dec 27 09:44:14 ip-10-1-1-118 daphne[65145]: 2023-12-27 09:44:14,784 INFO     {'payload': {'feePattern': 'IN_DEDUCT', 'senderAccount': '524282******2376', 'amount': '50.00', 'orderNo': '20231227937442649484738560', 'completedTime': '1703670248000', 'fee': '0.25', 'sign': 'Sd+B/eTXWoPk9mGZZB6k6ko7gdYoXUgLxDQn5Y7kdYbx8ZT1JU9G2hP6zHR0nGYUwimOV7CONKbyMj/xcyZ/Xx3hin3yReqntMYLhP3jP6b3y2NXna8G1uQfD2dZNoLo7JqZlF8Phn0di42IXqOy1cjZ4/BO/F0b3oF4IvMgc+A=', 'remark': 'POS_INWARD', 'transactionTime': '1703670248000', 'recipientBank': '', 'errorMsg': 'Approved or completed successfully', 'payNo': '231227051484836736', 'senderName': '', 'merchantId': '256623091343434', 'payMethod': 'BankCard', 'recipientAccount': '', 'recipientName': 'AAJ EXPRESS ONLINE PAYMENT', 'currency': 'NGN', 'headMerchantId': '256622070716625', 'sn': '98220417981802', 'senderBank': '', 'status': 'SUCCESS'}
