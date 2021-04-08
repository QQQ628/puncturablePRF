import os, sys
import math 
from oops_client import OOPS_Client
from oops_server import oops_server
from timeit import default_timer as timer

iv=os.urandom(16)
n=16
client=OOPS_Client(iv,n)
client.initdic()

start=timer()
#*****OFFline*******
client.setup()

Mes=client.message
m=client.m
#print(m)
s=client.s0
pub=client.pub #which is sent to the server


CT_R=client.CT_R
ck=client.client_key
end=timer()

server=oops_server(Mes,m,n,s,iv,pub)
server.initrecord()

hint,h_CT=server.hint(ck,CT_R)


client.Rescon1(h_CT,hint)
end=timer()
print(">>>>>>>>>>OFFline Total time taken " + str((end - start)*1000) + " ms")
#*****ONline********


start=timer()
q=client.Query(1)  
skp=q[0]
#print(skp)
ck_new=q[1]
CT_new=q[2]

a,h_CT_new,h_new=server.Answer(skp,CT_new,ck_new,client.s1)
MM=client.Recons2(a,h_CT_new,h_new)
end=timer()

print(">>>>>>>>>ONline total time taken " + str((end - start)*1000) + " ms")
print("First",MM)

"""
q=client.Query(16)
skp=q[0]
ck_new=q[1]
CT_new=q[2]
a,h_CT_new,h_new=server.Answer(skp,CT_new,ck_new,client.s1)
MM=client.Recons2(a,h_CT_new,h_new)
print("Second",MM)
"""

