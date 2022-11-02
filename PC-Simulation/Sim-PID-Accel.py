import math
import matplotlib
import matplotlib.pyplot as plt
import time

kp = 15
ki = 5
kd = 1

inp = 0

arropen = [0,0,0,1,1,0,0,0,0,-1,-1,0,0,0,0]
arrclose = [0,0,0,-1,-1,0,0,0,0,1,1,0,0,0,0]

st = -1

outpid = 0
prevpid = 0

output = 0
prevoutput = 0

error = 0
preverror = 0
ierror = 0
terror = 0

perioda = 0.01

outs = []
inps = []
sts = []

for counter in range(0,3000):
    if 1 < st <= 15:
        inp = arropen[math.floor(st)]
    elif 15 < st <= 30:
        inp = arrclose[math.floor(st)-15]

    inps.append(inp)

    error = inp - output
    ierror = ierror + (error * perioda)
    derror = (preverror - error)/perioda
    preverror = error
    outpid = kp * error + ki * ierror + kd * terror

    st = st + perioda
    sts.append(st)
    
    output = (0.00415 * outpid) + (0.00415 * prevpid) + (0.9917 * prevoutput)  
    outs.append(output)
    
    prevpid = outpid
    prevoutput = output
    
fig = plt.figure(figsize = (8,4))
plt.plot(sts, inps, "b-", label = "Input")
plt.plot(sts, outs, "g-", label = "Output")
plt.xlabel("Time", family = "serif", fontsize = 12)
plt.ylabel("Number", family = "serif", fontsize = 12)
plt.legend(loc = 'best')
plt.grid(True)
fig.savefig("pid-acc.jpg")
