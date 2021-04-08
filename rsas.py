
import rsa
import rsa.core
import os,sys
iv=os.urandom(16)
int_iv=int.from_bytes(iv,sys.byteorder)
print(int_iv)
(public_key, private_key) = rsa.newkeys(512)
encrypto1 = rsa.core.encrypt_int(1, public_key.e, public_key.n)
print(encrypto1^int_iv)
encrypto2 = rsa.core.encrypt_int(0, public_key.e, public_key.n)
print(encrypto2^int_iv)
decrypto = rsa.core.decrypt_int(encrypto1*encrypto2, private_key.d, public_key.n)
print(decrypto)
