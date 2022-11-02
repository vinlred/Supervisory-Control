import serial
import matplotlib.pyplot as plt

monitor = serial.Serial('COM3', 
                         115200, 
                         bytesize = serial.EIGHTBITS,
                         parity = serial.PARITY_NONE,
                         stopbits = serial.STOPBITS_ONE,
                         timeout = None)

xn = 0.0
yn = 0.0
xn1 = 0.0
yn1 = 0.0
posisi = 0.0
acc = 0.0
t = -100.0  # -100*0.01 = -1 sec

xs = [0.0]
ys = [0.0]
poss = [0.0]
accs = [0.0]
ts = [0.0]
plt.axis([-100, 3000, -4, 4])  # from -1 to 30 sec

if monitor.is_open:
    monitor.write(("%f;%f\r\n" % (0.0, 0.0)).encode("utf-8"))
    
    while(1):
        try:
            if monitor.inWaiting():
                xn = float(monitor.readline().decode("utf-8"))

                yn = (0.00415 * xn + 0.00415 * xn1 + 0.9917 * yn1)
                ys.append(yn)
                xs.append(xn)
                
                acc = (yn - yn1)/0.01
                accs.append(acc)
                
                posisi = posisi + (yn*0.01)
                poss.append(posisi)
                
                yn1 = yn
                xn1 = xn
                
                t = t + 1
                ts.append(t)

                monitor.write(("%f;%f\r\n" % (yn, posisi)).encode("utf-8"))
                
                plt.clf()
                plt.axis([-100, 3000, -3, 3])
                plt.plot(ts, ys, label = "Speed")
                plt.plot(ts, xs, label = "outpid")
                plt.legend()
                plt.draw()
                plt.pause(0.1)
                
        except Exception as e:
            plt.clf()
            plt.axis([-100, 3000, -3, 3])
            plt.plot(ts, ys, label = "Speed")
            plt.plot(ts, xs, label = "outpid")
            plt.legend()
            plt.savefig("Output-Motor.jpg")
            print(e)
            break

monitor.close()
