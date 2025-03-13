import numpy as np
from numpy import mod,linspace,cos,arccos,pi,exp
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import rc
rc('animation', html='jshtml')

f = 100   # fundamental frequency in Hz
w = 2*pi*f # angular frequency
T = 1/f   # fundamental period

# switching function for phase-u, v, and w
def hu(t):
    return np.heaviside(0.5 - 1/pi*arccos(cos(2*pi*f*t)),0)
def hv(t):
  return hu(t-T/3)
def hw(t):
  return hu(t+T/3)

#space vector
def sv(u,v,w):
  return 2/3*(u + v*exp(1j*2*pi/3) + w*exp(-1j*2*pi/3))

def hsvp(t,k):
  return 2/((6*k+1)*pi)*exp(1j*(6*k+1)*w*t)

def hsvn(t,k):
  return 2/((6*k-1)*pi)*exp(-1j*(6*k-1)*w*t)
# a= linspace(1,0,0)
# print(a)
def hsv(t,k): #include harmonics up to 6k+1
  y=hsvp(t,0)
  for i in linspace(1,k,k):
    y = y+hsvp(t,i)+hsvn(t,i)
  return y

def hsv1(t,k): # only include harmonics up to 6k-1
  y=hsvp(t,0)
  for i in linspace(1,k,k):
    y = y+hsvp(t,i)+hsvn(t,i)
  y=y-hsvp(t,k)
  return y


Ntp = 200 #total number of points
t=np.linspace(0,T,Ntp)


# print(sv(hut,hvt,hwt))
fig = plt.figure(figsize=(6,6))
ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))
line1, = ax.plot([], [], lw=1,linestyle='--',color='b') # fundamental circle
line11, = ax.plot([], [], '-bo') # fundamental vector
line2, = ax.plot([], [], lw=1, linestyle='--',color='g') # 5th order circle
line22, = ax.plot([], [], '-go') # 5th order vector
line3, = ax.plot([], [], lw=1,linestyle='--',color='r') # 7th order circle
line33, = ax.plot([], [], '-ro') # 7th order vector
line4, = ax.plot([], [], lw=2,linestyle='-',color='m') # total
line44, = ax.plot([], [], '-mo') # total vector
# initialization function: plot the background of each frame
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1,line2,

# animation function.  This is called sequentially
def animate(i):
    line1.set_data(hsv(t,0).real,hsv(t,0).imag)
    line11.set_data([0,hsv(t,0)[i].real],[0,hsv(t,0)[i].imag])
    line2.set_data(hsvp(t,0)[i].real + hsvn(t[0:int(Ntp/5)+1],1).real, hsvp(t,0)[i].imag + hsvn(t[0:int(Ntp/5)+1],1).imag)
    # line22.set_data([hsvp(t,0)[i].real,hsvp(t,0)[i].real+hsvn(t,1)[i].real],[hsvp(t,0)[i].imag,hsvp(t,0)[i].imag+hsvn(t,1)[i].imag])
    line22.set_data([hsv(t,0)[i].real,hsv1(t,1)[i].real],[hsv(t,0)[i].imag,hsv1(t,1)[i].imag])
    line3.set_data(hsv1(t,1)[i].real + hsvp(t[0:int(Ntp/7)+1],1).real, hsv1(t,1)[i].imag + hsvp(t[0:int(Ntp/7)+1],1).imag)
    line33.set_data([hsv1(t,1)[i].real,hsv(t,1)[i].real],[hsv1(t,1)[i].imag,hsv(t,1)[i].imag])
    line4.set_data(hsv(t,1)[0:i].real, hsv(t,1)[0:i].imag)
    return line1,line11,line2,line22,line3,line33,


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=Ntp, interval=50, blit=True)
anim
# to save the animation, uncomment the following three lines
f = r"FourierSeries.mp4" 
writervideo = animation.FFMpegWriter(fps=60) 
anim.save(f, writer=writervideo)

plt.show()