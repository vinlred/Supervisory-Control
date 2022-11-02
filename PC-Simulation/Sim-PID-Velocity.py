import math
import matplotlib
import matplotlib.pyplot as plt
import time

kp = 10
ki = 3
kd = 0.5

inp = 0

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
errors = []

for counter in range(0,3000):
    if 4 < st <= 8:
        inp = inp + 0.001
    elif 18 < st <= 22:
        inp = inp - 0.001
    else:
        inp = inp

    inps.append(inp)

    error = inp - output
    ierror = ierror + (error * perioda)
    derror = (preverror - error)/perioda
    preverror = error
    outpid = kp * error + ki * ierror + kd * terror
    errors.append(error)

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
fig.savefig("pid-vel.jpg")
