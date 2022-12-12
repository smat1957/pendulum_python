import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
#
# Constants
#
CCW = False       # CW = not CCW
A = 0.8           # [m]       radius
F = 0.1           # [Hz]      frequency
GAMMA = 2.0*pi*F  # [rad/s]   angular velocity
G  = 9.8          # [m/s^2]   acceleration of gravity
PHI0 = pi/6.      # [rad]     initial angle
V0 = 0.05         # [m/s]     initial velocity
L = 1.            # [m]       length of the pendulum
DURATION = 20.    # [s]       duration time
INTERVAL = 0.05   # [s]       interval time
#
# Differential equation
#
def ode(f, t):
    phi, dphi = f
    if CCW:
        # CCW at the right figure
        dfdt = [dphi, (A*GAMMA*GAMMA/L)*cos(phi-GAMMA*t)\
                          + (A*GAMMA/L)*cos(phi-GAMMA*t)*dphi\
                          - (G/L)*sin(phi)]
    else:
        # CW at the left figure
        dfdt = [dphi, (A*GAMMA*GAMMA/L)*cos(phi+GAMMA*t)\
                          - (A*GAMMA/L)*cos(phi+GAMMA*t)*dphi\
                          - (G/L)*sin(phi)]
    return dfdt
#
# Initial condition
#
f0 = [PHI0, V0/L]    # [theta, v] at t = 0
t = np.arange(0, DURATION + INTERVAL, INTERVAL)
#
# Solve the equation
#
sol = odeint(ode, f0, t)
phi = sol[:, 0]
if CCW:
    # CCW at the right sided figure
    circ_x = A * cos(GAMMA*t)
    circ_y = A * sin(GAMMA*t)
    x = circ_x + L * sin(phi)
    y = circ_y - L * cos(phi)
else:
    # CW at the left sided figure
    circ_x = A * cos(GAMMA*t)
    circ_y = - A * sin(GAMMA*t)
    x = circ_x + L * sin(phi)
    y = circ_y - L * cos(phi)
#
# Prepare the screen to display
#
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,\
                     xlim=(-2*L, 2*L), ylim=(-2*L, 2*L))
ax.grid()
markers_on = [2]
line, = plt.plot([], [], 'ro-', markevery=markers_on,  animated = True)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
#
# Simulate
#
def init():
    time_text.set_text('')
    return line, time_text

def update(i):
    next_x = [0, circ_x[i], x[i]]
    next_y = [0, circ_y[i], y[i]]
    line.set_data(next_x, next_y)
    time_text.set_text(time_template % (i*INTERVAL))
    return line, time_text

FRAME_INTERVAL = 1000 * INTERVAL # [msec] interval between frames
ani = FuncAnimation(fig, update, frames=np.arange(0, len(t)),
                    interval=FRAME_INTERVAL, init_func=init, blit=True)
#
# Show and save the results
#
plt.show()
FPS = 1000/FRAME_INTERVAL # frames per second
if CCW:
    fname = 'pendulum4CCW'
else:
    fname = 'pendulum4CW'
#ani.save(fname+'.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
ani.save(fname+'.gif', writer='imagemagick', fps=FPS)