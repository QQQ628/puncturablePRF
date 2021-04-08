import os, sys
import binascii
from Crypto.Cipher import AES
import pickle
import hashlib, hmac
from copy import deepcopy
import cmath
import random

class prs:

    def Gen(self,key_length=32):#Basic Setting For PPRF
        K=os.urandom(key_length)
        return K
        
   

    def _pad(self,s,bs=32):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    
    def encrypt(self,key,raw,iv):
        raw=self._pad(raw)
        cipher=AES.new(key,AES.MODE_CBC,iv)
        return cipher.encrypt(raw)


    def inttobinary(self,x):
        init="0000000000000000" #init: a binary with 16 bits
        xbin=bin(x).replace('0b','')

        if len(xbin)==16:
            result=xbin
        if len(xbin)<16:
            split=len(init)-len(xbin)
            init=init[0:split]+xbin
        if len(xbin)>16:
            print("Wrong number") #超过十六位
            return false

        return init


    def keytrim(self,key):
        if len(key) == 32:
           return key
        if len(key) >= 32:
           return key[:32]
        else:
           return _pad(key)   
        
    def Punc(self,iv,x_punc,k):

        traveled=''
        x_id=self.inttobinary(x_punc)
        path_tuples=[]
        for b_index in range(len(x_id)):
            if len(traveled)==0:
              if x_id[b_index] == '0':
                  result=self.encrypt(self.keytrim(k),'1',iv)
                  i_tuple= (result,'1')
                  path_tuples.append(i_tuple)
              else:
                  result =self.encrypt(self.keytrim(k),'0', iv)
                  i_tuple= (result,'0')
                  path_tuples.append(i_tuple)
            else:
                t_path=''
                if x_id[b_index] == '0':
                  t_path = traveled +'1'
                else:
                  t_path = traveled +'0'
                result=k
                for tranvers_digit in t_path:
                  result =self.encrypt(self.keytrim(result),tranvers_digit,iv)
                i_tuple = (result,t_path)
                path_tuples.append(i_tuple)
            traveled+= x_id[b_index]
            kp=path_tuples

        return kp  


    def Eval(self,iv,x,kp):

        x_id=self.inttobinary(x)
        result=False #random value for punc point


        for e in kp:         #check the path in the siblings
            if e[1]== x_id[0:len(e[1])]:
                if len(e[1])!=16:  #find the maximum same node 
                    result=e[0]
                    for j in range(len(e[1]),16):
                        result=self.encrypt(self.keytrim(result),x_id[j],iv)
                else:
                    result=e[0]
                break
             #if e[1]!=x_id[0:len(e[1])]: 
              #  count++
        #if count==16:
         #   return 0
        
        return result

    def F(self,x,k,iv):# F function
        x_id=self.inttobinary(x)
        k_id=0
        #for b in range(len(x_id)):

        result =self.encrypt(self.keytrim(k),x_id[0], iv)
        result =self.encrypt(self.keytrim(result),x_id[1], iv)
        result =self.encrypt(self.keytrim(result),x_id[2], iv)
        result =self.encrypt(self.keytrim(result),x_id[3], iv)
        result =self.encrypt(self.keytrim(result),x_id[4], iv)
        result =self.encrypt(self.keytrim(result),x_id[5], iv)
        result =self.encrypt(self.keytrim(result),x_id[6], iv)
        result =self.encrypt(self.keytrim(result),x_id[7], iv)
        result =self.encrypt(self.keytrim(result),x_id[8], iv)
        result =self.encrypt(self.keytrim(result),x_id[9], iv)
        result =self.encrypt(self.keytrim(result),x_id[10], iv)
        result =self.encrypt(self.keytrim(result),x_id[11], iv)
        result =self.encrypt(self.keytrim(result),x_id[12], iv)
        result =self.encrypt(self.keytrim(result),x_id[13], iv)
        result =self.encrypt(self.keytrim(result),x_id[14], iv)
        result =self.encrypt(self.keytrim(result),x_id[15], iv)
        return result



    def PRSGen(self,n,iv):
        k=self.Gen()
        S=[]
        sk=[]
        count=int(abs(cmath.sqrt(n)))
        r=random.sample(range(0,n),count)
        #print(r)
        l=list(set(S))
        for i in range(0,int(abs(cmath.sqrt(n)))):
               S.append(self.F(r[i],k,iv))

        l=list(set(S))   #generate the corresponding set



        if len(l)==int(abs(cmath.sqrt(n))): #ensure the length of S
            sk.append(n)
            sk.append(k)
            sk.append(r)
        #print(sk)
        return sk


    def PRSpunc(self,sk,i,iv):
        skp=[]
        n=sk[0]
        r=sk[2]
        for l in range(0,int(abs(cmath.sqrt(n)))):

            if self.F(r[l],sk[1],iv)==i: #if l can be found
               punc=self.Punc(iv,r[l],sk[1])
               skp.append(n)
               skp.append(punc)
               break


       # print(skp[1])
        return skp
       
              
        

    def PRSEval(self,skp,iv):
        S=[]
        n=skp[0]
        kp=skp[1]
#        print(kp)
        for i in range(0,int(abs(cmath.sqrt(n)))):
            if self.Eval(iv,i,kp)!=False:
                S.append(self.Eval(iv,i,kp))
            else:
                continue
        S=list(set(S))
        return S 

    def FS(self,sk,iv):
        S=[]
        n=sk[0]
        k=sk[1]
        r=sk[2]
        for i in range(0,int(abs(cmath.sqrt(n)))):
            S.append(self.F(r[i],k,iv))
        S=list(set(S))
        return S

    def Genwith(self,iv,i,n):
        while True:
            sk=self.PRSGen(n,iv)
            k=sk[1]
            r=sk[2]
            #f=self.F(i,k,iv)
            #S=self.FS(sk,iv)
            if i in r:
                break
        print(sk)
        return sk
            





if  __name__ == '__main__':
    iv=os.urandom(16)
    i=prs()
    x=5

    sk=i.Genwith(iv,x,200)
    #skp=i.PRSpunc(sk,Fx,iv)
    #S=i.FS(sk,iv)
    #SP=i.PRSEval(skp,iv)
    #print(sk[2])




        

        #iv=os.urandom(16)
        #sk=PRSGen(5000,iv)
        #print("this is the key")
        #x_punc=1
        #print(inttobinary(x_punc))
        #kp=Punc(iv,x_punc,k)
        #x=2
        #if Eval(iv,x,kp)==F(x,k,iv):
         #   print("This is not the punc point")
        #else:
         #   print("This is the punc point")
        
        



