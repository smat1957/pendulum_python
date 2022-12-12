from numpy import sin, cos, pi
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.integrate import odeint
#
# Constants
#
G = 9.8            # [m/s^2]  acceleration of gravity
PHI1_0 = pi        # [rad] initial theta
PHI2_0 = -pi/6.    # [rad] initial theta
V1_0 = 0.          # [m/s]    initial velocity
V2_0 = 0.          # [m/s]    initial velocity
L1 = 1.            # [m]      length of pendulum
L2 = 1.            # [m]      length of pendulum
M1 = 1.            # [kg]     mass
M2 = 0.4           # [kg]     mass
DURATION = 15.     # [s]      duration time
INTERVAL = 0.05    # [s]      interval time
#
# Differential Equation
#
def ode(f, t):
    phi1, dphi1, phi2, dphi2 = f
    M, H = M1 + M2, phi1 - phi2
    dphi1dt = (M*G*sin(phi1)\
                + M2*(L2+L1*cos(H))*sin(H)*dphi1*dphi2\
                - M2*G*cos(H)*sin(phi2))\
                /(-M*L1+M2*L1*cos(H)*cos(H))
    dphi2dt = (M*G*cos(H)*sin(phi1)
                +(M2*L2*cos(H)+M*L1)*sin(H)*dphi1*dphi2\
                - M*G*sin(phi2))\
                /(M*L2-M2*L2*(cos(H))**2)
    return [dphi1, dphi1dt, dphi2, dphi2dt]
#
# Initial Condition
#
f_0 = [PHI1_0, V1_0/L1, PHI2_0, V2_0/L2]
t = np.arange(0, DURATION + INTERVAL, INTERVAL)
#
# Solve the Equation
#
sol = odeint(ode, f_0, t)
phi1, phi2 = sol[:, 0], sol[:, 2]
x1 = L1 * sin(phi1)
y1 = - L1 * cos(phi1)
x2 = x1 + L2 * sin(phi2)
y2 = y1 - L2 * cos(phi2)
#
# Prepare the Screen to display
#
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim = [-L1 - L2, L1 + L2], ylim = [-L1 - L2, L1 + L2])
ax.grid()
markers_on = [1,2]
line, = plt.plot([], [], 'ro-', markevery=markers_on, animated = True)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
#
# Simulate
#
def init():
    time_text.set_text('')
    return line, time_text

def update(i):
    next_x = [0, x1[i], x2[i]]
    next_y = [0, y1[i], y2[i]]
    line.set_data(next_x, next_y)
    time_text.set_text(time_template % (i * INTERVAL))
    return line, time_text

FRAME_INTERVAL = 1000 * INTERVAL # [msec] interval time between frames
ani = FuncAnimation(fig, update, frames=np.arange(0, len(t)),
                    interval=FRAME_INTERVAL, init_func=init, blit=True)
#
# Show and Save the results
#
plt.show()
FPS = 1000/FRAME_INTERVAL        # frames per second
#ani.save('double_pendulum.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
ani.save('double_pendulum.gif', writer='imagemagick', fps=FPS)