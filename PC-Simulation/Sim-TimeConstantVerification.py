import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
import time

t = -1
xn = 0
xn1 = 0
yn1 = 0
period = 0.01

xs = []
ys = []
ts = []

for counter in range(0,1000):
    if t < 0:
        xn = 0        
    else:
        xn = 1
        
    t = t + period
    xs.append(xn)                    
    y = (0.00415 * xn + 0.00415 * xn1 + 0.9917 * yn1)
    ys.append(y)
    ts.append(t)
    yn1 = y
    xn1 = xn
