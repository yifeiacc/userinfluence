
"""
this moduel is for testing artificial data provided by ConTinEst
"""

import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import kendalltau
from scipy.stats import spearmanr
import pickle
def influence(p):
    n = len(p)
    m = np.zeros((n, n)) #intiallize at step 1
    m[0, 0] = 1
    for i in range(0, n-1):
        vec = p[:i+1, i+1]
        m[:i+1, i+1] = m[:i+1, :i+1]@vec
        m[i+1, i+1] = 1
        if len(vec)%100 == 0:print("current matrix size is ",len(vec))
    return np.sum(m, axis = 1)
def p_ji(d1):
    r = np.log(np.zeros((1024,1024)))
    n = d1[:,0:2]
    n = np.array(n,dtype = np.int32) 
    b = d1[:,2]
    a = d1[:,3]
    t = n[:,1] - n[:,0]
    p = np.array(list(map(lambda x, y, z: np.log(x/y)+(x-1)*np.log(z/y)+(-1*(z/y)**x),b,a,t)))
    norm = np.zeros(len(r))
    for i in range(0,len(n)):
        r[n[i,0], n[i,1]] = p[i]
    for i in range(1,len(r)):
        li = r[:i,i]
        norm[i] = reduce(np.logaddexp, li)
        if(norm[i]!= -np.inf):
            r[:i,i] = r[:i,i]-norm[i]
    r = np.exp(r)
    return r**2
r1 = []
r2 = []
r3 = []
with open("./data/data_n_pow") as f:
    for line in f:
        r1.append(line.split(","))
with open("./data/Con_result_n_pow")as f1:
    for line in f1:
        r2.append(line.strip(" ").strip("ConTinEst").strip().strip(":").strip(" "))

d1 = np.array(r1, dtype = np.float64)
d2 = np.array(r2, dtype = np.float64)


p = p_ji(d1)
our_appr = influence(p)
m1 = np.max(our_appr)
our_appr = (our_appr / m1)
m2= np.max(d2)
continest = d2/m2

print ('****************************')
print("PersonrResult" ,pearsonr(our_appr,d2))
print (spearmanr(our_appr,d2))
print (kendalltau(our_appr,d2))
plt.plot([i for i in range(0,1024)],our_appr, "x")
plt.ylabel("influence")
plt.xlabel("time")
plt.title("ConTinEst")
plt.legend(["user"])
plt.show()
plt.plot([i for i in range(0,1024)],continest, "x")
plt.ylabel("influence")
plt.title("Our approch")
plt.xlabel("time")
plt.legend(["user"])
plt.show()

