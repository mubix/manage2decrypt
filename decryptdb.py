#!/usr/bin/env python3

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

# Find in /opt/ManageEngine/OpManager/conf/customer-config.xml as "CryptTag"
# Example: <configuration name="CryptTag" value="PMMk9CtzPx1dNr1fSzb7"/>

passphrase = "PMMk9CtzPx1dNr1fSzb7"

# Find in /opt/ManageEngine/OpManager/conf/database_params.conf
# Example: password=064f66097e46438ede9e4d2048f33b6171c973381f9631ae4bb57caeaba1310fab74a36e897307000111dad91e3aed4a29e508fc89dfb54d0001e38a3c9ff498d47edd02

encrypted = "064f66097e46438ede9e4d2048f33b6171c973381f9631ae4bb57caeaba1310fab74a36e897307000111dad91e3aed4a29e508fc89dfb54d0001e38a3c9ff498d47edd02"

salt = encrypted[0:40]
print("       Salt: " + salt)
ciphertext = bytearray.fromhex(encrypted[40:])
print("Cipher Text: " + ciphertext.hex())
key = PBKDF2(passphrase, bytearray.fromhex(salt), 64, count=65556)[:32]
print("Derived Key: " + key.hex())

print("Testing Decryption...")
iv = 16 * b'\0'

cipher = AES.new(bytes(key), AES.MODE_CBC, iv)
plaintext = cipher.decrypt(bytes(ciphertext))
padding = plaintext[-1]
print("Plain Text: " + plaintext[:-padding].decode())

