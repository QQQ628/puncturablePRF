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



    def PRSGen(self,n,iv,size):
        k=self.Gen()
        S=[]
        sk=[]
        r=random.sample(range(0,n),size)
        #print(r)
        for i in range(0,size):
               S.append(self.F(r[i],k,iv))

      #  l=list(set(S))   #generate the corresponding set


          
        if len(S)==size: #ensure the length of S
            sk.append(n)
            sk.append(k)
            sk.append(r)
        return sk


    def PRSpunc(self,sk,i,iv,size):
        skp=[]
        n=sk[0]
        k=sk[1]
        r=sk[2]

        S=self.FS(sk,iv,size,n)
#        print(S)

        if i in S: #if l can be found
            r_index=S.index(i)
            r_punc=r[r_index]
            punc=self.Punc(iv,r_punc,sk[1])
            skp.append(n)
            skp.append(punc)
            skp.append(r)
        return skp
       
              
    def PRSEval(self,skp,iv,size):
        S1=[]
        S=[]
        n=skp[0]
        kp=skp[1]
        r=skp[2]
        count=0
#        print(kp)
       # print(r)
        for i in range(0,size):
            if self.Eval(iv,r[i],kp)!=False:  #Eval(iv,r[i],kp==F(r[i],k,iv)
                S1.append(self.Eval(iv,r[i],kp))

                int_result = int.from_bytes(S1[count], sys.byteorder)
                count+=1
                int_result=int_result%n
                while int_result in S:
                    int_result=(int_result+1)%n 
                S.append(int_result)
                
            else:
                continue
       # S=list(set(S))

        return S 

    def FS(self,sk,iv,size,n):
        S1=[]
        S=[]
        n=sk[0]
        k=sk[1]
        r=sk[2]
        for i in range(0,size):
            S1.append(self.F(r[i],k,iv))
            int_result = int.from_bytes(S1[i], sys.byteorder)
            int_result=int_result%n
            while int_result in S:
                int_result=(int_result+1)%n   #the member of set must be (0,n)
            S.append(int_result)
        #S=list(set(S))
        return S


    def Genwith(self,iv,i,n,size):
        while True:
            sk=self.PRSGen(n,iv,size)
            k=sk[1]
            r=sk[2]

            #f=self.F(i,k,iv)
            S=self.FS(sk,iv,size,n)


            if i in S:
                break

       # print(sk)
        return sk
            



"""

if  __name__ == '__main__':
    iv=os.urandom(16)
    i=prs()
    x=5
    size=int(abs(cmath.sqrt(500)))
    sk=i.Genwith(iv,x,500,size)
    S0=i.FS(sk,iv,size,500)
    print(S0)
    skp=i.PRSpunc(sk,x,iv,size)
    S=i.PRSEval(skp,iv,size)
    print(S)
"""
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
        
        



