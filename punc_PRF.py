import os, sys
import binascii
from Crypto.Cipher import AES
import pickle
import hashlib, hmac
from copy import deepcopy


class Punc_PRF:
    def Gen_(self,iv,key_length=32):#Basic Setting For PPRF
        K=os.urandom(key_length)
        return K
        
    
        
    def Punc(key,x_punc,k): #乱七八糟 不对

        traveled=''
        x_id=int.to_bytes(x_punc,byteorder = 'big')
        path_tuples=[]
        for b in range(len(x_id)):
            if len(traveled)==0:
              if x_id[b_index] == '0':
                  result=self.encrypt(self.keytrim(k),'1',self.fixed_iv)
                  i_tuple= (result,'1')
                  path_tuples.append(i_tuple)
              else:
                  result =self.encrypt(self.keytrim(k),'0', iv)
                  i_tuple= (result,'0')
                  path_tuples.append(i_tuple)
            else:
                t_path=''
                if t_id[b_index] == '0':
                  t_path = traveled +'1'
                else:
                  t_path = traveled +'0'
                result=k
                for tranvers_digit in t_path:
                  result =self.encrypt(self.keytrim(result),tranvers_digit,iv)
                i_tuple = (result,t_path)
                path_tuples.append(i_tuple)
            traveled+= t_id[b_index]
            kp=path_tuples

        return kp  


    def Eval(self,x,kp):

        x_id=int.to_bytes(x,byteorder = 'big')
        for i in range(len(x_id)):
            for e in kp:         #check the path in the siblings
                if e[1]== x_id[0:len(e[1])]:
                   if len(e[1])!=16:
                       result=e[0]
                      for j in range(len(e[1],16)):
                          result=self.encrypt(self.keytrim(result),x_id[j],iv)
                   else:
                       result=e[0]
                   break
        return result
    
        if __name__ == '__main__':



        
               




    
        
        
        
    def encrypt(self,key,raw,iv):
        raw=self._pad(raw)
        cipher=AES.new(key,AES.MODE_CBC,iv)
        return self.encrypt(raw)

    def _pad(self,s,bs):
         return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)



    def keytrim(self, key):
        if len(key) == 32:
           return key
        if len(key) >= 32:
           return key[:32
        else:
           return self._pad(key)
