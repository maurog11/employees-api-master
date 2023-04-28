from flask import current_app
import time
import hashlib
import json
from Crypto.Cipher import AES
from Crypto import Random

from api.email import send_password_recovery_email
from ..employee.services import get_employee_by_id, update_employee_password

encryptor = None


def __get_aes_obj():
    global encryptor
    if not encryptor:
        encryptor = AESCipher(current_app.config['PASSWORD_RECOVERY_SECRET'])
    return encryptor


def send_password_reset_link(email):
    employee = get_employee_by_id(email)
    if employee:
        obj = {'employee_id': employee.id, 'valid': time.time() + current_app.config['PASSWORD_RECOVERY_TTL']}
        payload = json.dumps(obj, ensure_ascii=False)
        ciphertext = __get_aes_obj().encrypt(payload)
        send_password_recovery_email(employee.email, employee.surname if not employee.first_name else employee.first_name, ciphertext)
    else:
        raise ValueError('No employee found')


def reset_employee_password(token, new_password):
    payload = __get_aes_obj().decrypt(token)
    obj = json.loads(payload)

    if obj['valid'] < time.time():
        raise Exception('Reset password token has expired')

    employee = get_employee_by_id(obj['employee_id'])
    if employee:
        update_employee_password(employee, new_password)


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return (iv + cipher.encrypt(raw.encode('utf8'))).hex()

    def decrypt(self, enc):
        enc = bytes.fromhex(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
