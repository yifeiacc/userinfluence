"""
Main code of user influence estimation are implimented in this modle.
all code are implimented by Yifei Zhang by using Scientific computing 
library numpy and scipy 
"""
from functools import reduce
from multiprocessing import Pool
import numpy as np
import math
import bz2, json
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import datetime, timedelta
import pickle
from Parallel import *
class User(object):
    def __init__(self,uid):
        self.uid = uid
        self.tweets = []
        self.inf = 0
        self.cas_count = 0
    def setInf(inf):
        self.inf = inf
    def addTweets(tweet):
        self.tweets.append(tweet)
        
class Tweet(object):
    def __init__(self,tweet):
        if isinstance(tweet['user']['id'], dict):
            self.uid = list(tweet['user']['id'].values())[0]
        else:
            self.uid = tweet['user']['id']    
        self.num_follower = tweet['user']['followers_count']
        self.time = datetime.strptime(tweet['created_at']['$date'],'%Y-%m-%dT%H:%M:%S.000+1000').timestamp()
        #self.time = datetime.strptime(tweet[u'created_at'][:18]+tweet[u'created_at'][-5:],'%a %b %d %H:%M:%S %Y').timestamp()
        if isinstance(tweet['id'], dict):
            self.tid = list(tweet['id'].values())[0]
        else:
            self.tid = tweet['id']
        self.influence = None
        self.step =0
    def setInfluence(self,influence):
        self.influence = influence
"""
Next four function are helper function for parallel computing
"""        
def compute_one_cas(cas):
    #p = p_ij(cas)
    p = P_ij(cas)
    inf = influence(p)
    for i in range(0,len(cas)):
        cas[i].influence = inf[i]
    return cas

def compute_muti_cas(muti_cas):
    L = list(map(compute_one_cas, muti_cas))
    return L
    
def para_compute_muti_cas(muti_cas, n = 20):
    nproc = 1 if len(muti_cas) < n else n
    muti_cas_list = split(muti_cas, nproc)
    pool = Pool(nproc)
    result = pool.map(compute_muti_cas, muti_cas_list)
    pool.close()
    pool.join()
    cascades = list(reduce(lambda x, y: x+y, result))
    tweets = list(reduce(lambda x, y: x+y, cascades))
    cascades.sort(key = lambda cas: cas[0].time)
    tweets.sort(key = lambda t: t.time)
    return tweets, cascades

"""
Main function sfor user influence estimation
"""

def P_ij (cas,r = -0.01):
    """Compute the probability of retweet bewtween any two user
    This function compute the Prob^2_ij for each user and Store 
    it in matrix p_ij
    Args:
        cas: a list of Tweet object with in one cascade
        r: time decay coefficient,defaut set to -0.01
    Returns: 
        p_ij: 2d numpy array    
    """ 
    nodes = cas
    n = len(nodes)
    if n > 50 : print("the size of cascade is", n) 
    k = 0
    t = np.zeros(n,dtype = np.float64)
    f = np.zeros(n,dtype = np.float64)
    p = np.zeros((n,n),dtype = np.float64)
    norm = np.zeros(n,dtype = np.float64)
    for node in nodes:
        if k == 0:
            p[0][0] = 1
            t[0] = node.time
            f[0] = node.num_follower
            k = k + 1
            continue
        t[k] = node.time
        f[k] = 1 if node.num_follower == 0 else node.num_follower
        p[:k, k] = ((r * (node.time - t[0:k])) + np.log(f[0:k])) # store the P_ji in log space
        norm[k] = reduce(np.logaddexp, p[:k, k])
        p[:k, k] = np.exp(p[:k, k] - norm[k])# recover the P_ji from log space
        k = k + 1
    return p**2
 # this function compute the user influence and store it in matirx m_ij
def influence(p):
    """Estimate user influence
    this function compute the user influence and store 
    it in matirx m_ij
    Args:
        p: 2d np array p_ij
    Returns: 
        m_ij: 2d numpy array
    """
    n = len(p)
    m = np.zeros((n, n))
    m[0, 0] = 1
    for i in range(0, n-1):
        vec = p[:i+1, i+1]
        m[:i+1, i+1] = m[:i+1, :i+1]@vec
        m[i+1, i+1] = 1
        if len(vec)%100 == 0: print("current matrix size is ",len(vec))
    m_ij = np.sum(m, axis = 1)

    return m_ij
# compute user influence in a cascde
def user_inf(tweets):
    """Gourp user inluence in each cascade
    Args:
        tweets :a list of Tweet object among mutiple cascades
    Returns: 
        u_dir: a dictory maping key to corresponding user influence
        u_num: number of users
    """
    u_dir = {}
    u_num =[]
    fir_t = tweets[0].time
    las_t = tweets[-1].time
    for t in tweets:
        if t.uid in u_dir:
            u_dir[t.uid].inf = u_dir[t.uid].inf + t.influence - 1
            u_dir[t.uid].tweets.append(t)
        else:
            u = User(t.uid)
            u.inf = t.influence
            u.tweets.append(t)
            u_dir[t.uid] = u
        u_num.append(len(u_dir))
    # for each user sort his tweet by time
    for user in list(u_dir.values()):
        user.tweets.sort(key=lambda t:t.time) 
    return u_dir, u_num