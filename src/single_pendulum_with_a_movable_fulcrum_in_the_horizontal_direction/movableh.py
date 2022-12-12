from numpy import sin, cos, pi
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.integrate import odeint
#
# Constants
#
L = 1               # [m]      length of the pendulum
PHI0 = -pi/6        # [rad]    initial phi
V0 = 0.0            # [m/s]    initial velocity
X0 = 0              # [m]      initial location
G  = 9.8            # [m/s^2]  acceleration of gravity
M1 =  1             # [kg]     mass
M2 =  1             # [kg]     mass
DURATION = 10       # [s]      duration time
INTERVAL = 0.05     # [s]      interval time
#
# Differential equation
#
def ode(f, t):
    phi, dphi, x, dx = f
    dpdt = sin(phi)/L*dx-sin(phi)/L*dx*dphi-G/L*sin(phi)
    dxdt = -M2*L*dphi*cos(phi)/(M1+M2)
    return [dphi, dpdt, dx, dxdt]
#
# Initial condition
#
f_0 = [PHI0, V0/L, X0, V0/L]
t = np.arange(0, DURATION + INTERVAL, INTERVAL)
#
# Solve the equation
#
sol = odeint(ode, f_0, t)
phi, x = sol[:, 0], sol[:, 2]
x1 = M2*L*sin(phi)/(M1+M2)
y1 = 0*t
x2 = x1 + L * sin(phi)
y2 = -y1 - L * cos(phi)
#
# Prepare the screen to display the results
#
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,\
                     xlim = [-L - L, L + L], ylim = [-L - L, L + L])
ax.grid()
ax.set_title('M1={}, M2={}, L={}'.format(M1,M2,L))
line, = plt.plot([], [], 'ro-', animated = True)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
#
# Simulate with animation
#
def init():
    time_text.set_text('')
    return line, time_text

def update(i):
    next_x = [x1[i], x2[i]]
    next_y = [y1[i], y2[i]]
    line.set_data(next_x, next_y)    
    time_text.set_text(time_template % (i * INTERVAL))
    return line, time_text

FRAME_INTERVAL = 1000 * INTERVAL # [msec] interval time between frames
ani = FuncAnimation(fig, update, frames=np.arange(0, len(t)),
                    interval=FRAME_INTERVAL, init_func=init, blit=True)
#
# Show and save the results  
#
FPS = 1000/FRAME_INTERVAL        # frames per second
plt.show()
#ani.save('pendulum3.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
ani.save('pendulum3.gif', writer='imagemagick', fps=FPS)