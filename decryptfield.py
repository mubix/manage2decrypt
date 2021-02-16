#!/usr/bin/env python3

# This script requires pycrypto and pgpy 
# both can be installed using pip3 install pycrypto pgpy

import pgpy
from sys import argv
from Crypto.Cipher import DES
from base64 import b64decode, b64encode

# Source https://stackoverflow.com/a/45928164
def isBase64(sb):
  try:
    if isinstance(sb, str):
      # If there's any unicode here, an exception will be thrown and the function will return false
      sb_bytes = bytes(sb, 'utf-8')
    elif isinstance(sb, bytes):
      sb_bytes = sb
    else:
      raise ValueError("Argument must be string or bytes")
    return b64encode(b64decode(sb_bytes)) == sb_bytes
  except Exception:
    return False


if (len(argv) < 2):
  print("This script requires one argument, the database field you wish to decrypt starting in c30c04090102")
elif (not(argv[1].upper().startswith('C30C04090102'))):
  print("This script requires one argument, the database field you wish to decrypt starting in c30c04090102")
else:
  pgp_hexmsg = argv[1]
  pgp_key = 'Mickey'

  pgp_msg = bytes.fromhex(pgp_hexmsg)
  pgp_msgblob = pgpy.PGPMessage.from_blob(pgp_msg)
  pgp_dec_message = pgp_msgblob.decrypt(pgp_key)
  #print(pgp_dec_message.message.__class__.__name__)
  if isinstance(pgp_dec_message.message, str):
    print("PGP Decrypted Message: " + pgp_dec_message.message)

    if isBase64(pgp_dec_message.message):
      des_key = b'APMEXTPR'
      des_msg = b64decode(pgp_dec_message.message)
      des_cipher = DES.new(des_key, DES.MODE_ECB)
      plaintext = des_cipher.decrypt(des_msg)
      padding = plaintext[-1]
      print("DES Decrypted Message: " + plaintext[:-padding].decode())
  else:
    print("PGP Deccrypted Message (hex): ")
    print(''.join(format(x, '02x') for x in pgp_dec_message.message))
    try:
      s = pgp_dec_message.message.decode('utf-8')
      print("PGP Decrypted Message:")
      print("######## PGP DECRYPTED MESSAGE ########")
      print(s)
      print("######## PGP DECRYPTED MESSAGE END ########")
    except Exception:
      print("Failed to decode the hex")
