import os, sys
import binascii
from Crypto.Cipher import AES
import pickle
import hashlib, hmac
from prs import prs
import math 
from copy import deepcopy
from paillier import *
from boosted_paillier import *
from timeit import default_timer as timer

y = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


class oops_server:
    def __init__(self,Mes,m,n,s,iv,pub):
        self.Record=Mes
        self.ConM=[]
        self.p=prs()
        self.fixed_iv=iv
        self.m=m
        self.n=n
        self.s=s
        self.pub=pub
        
    def initrecord(self):
        for i in self.Record:
            if i in y:
                self.ConM.append(ord(i))
       # printk [3, 4]self.ConM)
#transfer char to int

    
 

    def hint(self,CK,CT_R):
        start=timer()
        h=0
        hct=[]
        Hint=[]
#        print(len(self.ConM))

        for i in range(self.m):
            S=self.p.FS(CK[i],self.fixed_iv,self.s,self.n)
            h=0
            for e in S:
                h+=self.ConM[e]
            Hint.append(h)
        count=0
        #print(len(CT_R))
        #print(len(CT_R[0]))
        for ct in CT_R:
            const_mult=[]
            for j in range(len(ct)):
               # count+=1
               # print(count)
                const_mult.append(cmult1(self.ConM[j],ct[j],self.pub))
            hct.append(const_mult)
       # print("Run here")
        end=timer()
        print(">>>>>>OFFline hint taken " + str((end - start)*1000) + " ms")
        return Hint,hct
        
         



    def Answer(self,skp,CT_new,sk_new,s0):
        start=timer()
        S=self.p.PRSEval(skp,self.fixed_iv,s0)
#        print("puncset",S)
    #    S_new=self.p.FS(sk_new,self.fixed_iv,self.s,self.n)
       # print("hintset",S_new)
        a=0
        h_CT_new=[]
        h_new=0
        start1=timer()
        for e in S:
            a+=self.ConM[e]
# print("a",a)
        end=timer()
        print(">>>>>>search answer taken " + str((end - start)*1000) + " ms")
        print(">>>>>>search over database taken " + str((end - start1)*1000) + " ms")
         


        start=timer()
        S_new=self.p.FS(sk_new,self.fixed_iv,self.s,self.n)

        for i in range(self.n):
            const_mult=cmult1(self.ConM[i],CT_new[i],self.pub)
            h_CT_new.append(const_mult)
    
        for i in S_new:
            h_new+=self.ConM[i]
        end=timer()
        print(">>>>>>Online update time taken " + str((end - start)*1000) + " ms")

    

        return a,h_CT_new,h_new



         

        








