import os, sys
import binascii
from Crypto.Cipher import AES
import pickle
import hashlib, hmac
from prs import prs
import math
import cmath
from copy import deepcopy
from paillier import *
from boosted_paillier import *
import numpy as np
from timeit import default_timer as timer

class OOPS_Client:
    def __init__(self,iv,n):
        self.n=n
      #  print(n)
        self.s0=int(abs(cmath.sqrt(n)))
#        print("s0",self.s0)
 #       print(math.log10(n))
        self.m=int(n/self.s0) #*math.log10(n))
        self.s1=int(math.log(n))

        self.secret_key=[]
        self.secret_set=[]
        
        self.client_key=[]
        self.client_set=[]

        self.R=[]
        self.CT_R=[]
         
        self.hint=[]
        key_size=256
        self.priv,self.pub=generateKeys(key_size)

        self.message={}
        self.p=prs()
        self.iv=iv
        self.q={}

        self.isreplace=-1
        self.islong=0

    def initdic(self):
        with open("index_16.txt", "r") as f:
            self.message=f.read()
    
    def bernolli(self,p):
        n=1
        size=100
        bs=np.random.binomial(n,p,size)
       # print(bs)
        return bs



    def setup(self):
       # print(self.m)
        start=timer()
        for i in range(self.m):
            self.client_key.append(self.p.PRSGen(self.n,self.iv,self.s0))
            self.secret_key.append(self.p.PRSGen(self.n,self.iv,self.s1))
        for i in range(self.m):
            self.client_set.append(self.p.FS(self.client_key[i],self.iv,self.s0,self.n))
            self.secret_set.append(self.p.FS(self.secret_key[i],self.iv,self.s1,self.n))
            R=[item for item in self.client_set[i] if item not in self.secret_set[i]]+[item for item in self.secret_set[i] if item not in self.client_set[i]]
            self.R.append(R)
            
        m0=0
        m1=1
#        self.client_set=[]

        c0=CipherLevel1(-1,-1)
        c1=CipherLevel1(-1,-1)
        c0.prepare_message(self.pub, m0)
        c1.prepare_message(self.pub, m1)

        for rr in self.R:
            CT=[c0]*self.n
            for i in rr:
                CT[i]=c1
            self.CT_R.append(CT)
        end=timer()
        print(">>>>>>OFFline the client setup taken " + str((end - start)*1000) + " ms")

    def Rescon1(self,h_CT,h):
        self.CT_R=[]
        start=timer()
        for i in range(self.m):
            h_r=0
            for j in range(self.n):
                h_r+=h_CT[i][j].get_value(self.priv,self.pub)
            if len(self.client_set[i])>=len(self.R[i]):
                self.hint.append(h[i]-h_r)
            else:
                self.hint.append(h_r-h[i])
        h_CT=[]
        end=timer()
        print(">>>>>>OFFline Rescon1 time taken " + str((end - start)*1000) + " ms")

    def Query(self,i):
        start=timer()
        ck_new=self.p.Genwith(self.iv,i,self.n,self.s0)
        sk_new=self.p.Genwith(self.iv,i,self.n,self.s1)

        ck_new_set=self.p.FS(ck_new,self.iv,self.s0,self.n)
        sk_new_set=self.p.FS(sk_new,self.iv,self.s1,self.n)
         
#        print("sknew:",sk_new_set)
    
        R_new=[item for item in ck_new_set if item not in sk_new_set ]+[item for item in sk_new_set if item not in ck_new_set]

        if len(ck_new_set)>len(R_new):
            self.islong=1

       # print("rrr",R_new)
        m0=0
        m1=1
        c0=CipherLevel1(-1,-1)
        c1=CipherLevel1(-1,-1)
        c0.prepare_message(self.pub, m0)
        c1.prepare_message(self.pub, m1)
        CTR=[c0]*self.n
        for t in R_new:
            CTR[t]=c1
       # print()
        p=(self.s0-1)/self.n

        bs=list(self.bernolli(p))
      #  print(bs)
        b=random.sample(bs,1)
       # print(b)
        sk_punc=0
 #       print(len(self.secret_set))
        for j in range(len(self.secret_set)):
        #    print("RUN HERE")
            if i in self.secret_set[j] and b==[0]:
                self.isreplace=j
                sk_punc=self.p.PRSpunc(self.secret_key[self.isreplace],i,self.iv,self.s1)
                self.secret_key[self.isreplace]=sk_new
                self.secret_set[self.isreplace]=sk_new_set
                self.client_key[self.isreplace]=ck_new
                self.q[0]=sk_punc
                self.q[1]=ck_new
                self.q[2]=CTR
                print("Repalced")
                end=timer()
                print(">>>>>>Online Query time taken " + str((end - start)*1000) + " ms")
                return self.q

            if i not in self.secret_set[j] and b==[0] and j==self.m-1:
                sk_punc=self.p.PRSpunc(sk_new,i,self.iv,self.s1)
                self.q[0]=sk_punc
                self.q[1]=ck_new
                self.q[2]=CTR
                print("not repalced")
                end=timer()
                print(">>>>>>Online Query time taken " + str((end - start)*1000) + " ms")
                return self.q

            if b==[1]:
                ipunc=random.sample(self.secret_set[j],1)[0]
                self.isreplace=j
                sk_punc=self.p.PRSpunc(sk_new,i,self.iv,self.s1)
                self.q[0]=sk_punc
                self.q[1]=ck_new
                self.q[2]=CTR
                end=timer()
                print(">>>>>>Online Query time taken " + str((end - start)*1000) + " ms")
                return self.q

    def Recons2(self,a,h_CT_new,h_new):
        start=timer()
        h_r=0
        #print(h_CT_new)
        for i in h_CT_new:
            h_r+=i.get_value(self.priv,self.pub)
#        print(h_new)
 #       print(h_r)
        
        if self.isreplace!=-1:
            M=self.hint[self.isreplace]-a
            Mes=chr(abs(M))
            if self.islong==1:
                self.hint[self.isreplace]=h_new-h_r
            else:
                self.hint[self.isreplace]=h_r-h_new
            #update
            end=timer()
            print(">>>>>>Online recons2 time taken " + str((end - start)*1000) + " ms")
            return Mes
        else:
            if self.islong==1:
                M=h_new-h_r-a
                Mes=chr(abs(M))
                end=timer()
                print(">>>>>>Online recons2 time taken " + str((end - start)*1000) + " ms")
                return Mes
            else:
                M=h_r-h_new-a
                Mes=chr(abs(M))
                end=timer()
                print(">>>>>>Online recons2 time taken " + str((end - start)*1000) + " ms")
                return Mes

            
            




                
       





        
















