
"""
this moduel is for testing in real world data with mutiple cascades
"""
from userinfluence import *
muti_cas =  pickle.load(open('./data/test_muticas.pickle', 'rb'))
t, c = para_compute_muti_cas(muti_cas)# return list of Tweet and list of cascade
u_dir, u_num = user_inf(t)#get the time of first tweet and last tweet 

u_list = list(u_dir.values())
frist_t = t[0].time  
last_t =t[-1].time 
#sort user by it's frist tweet's time
u_frist = sorted(u_list,key=lambda u:u.tweets[0].time)
u_last =  sorted(u_list,key=lambda u:u.tweets[-1].time)
for cas in c:
    u_dir[cas[0].uid].cas_count += 1

f_u = [u.tweets[0].time-frist_t for u in u_frist]
f_inf = [u.inf for u in u_frist]
l_u = [u.tweets[-1].time-frist_t for u in u_last]
l_inf = [u.inf for u in u_last]
plt.plot(f_u, f_inf,"x")
plt.xlabel('time(second)')
plt.ylabel('influence')
plt.legend(["user"])
plt.show()