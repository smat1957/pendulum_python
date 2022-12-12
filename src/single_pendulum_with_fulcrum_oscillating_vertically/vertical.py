import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
#
# Constants
#
A = 1.0          # [m]
F = 0.1          # [Hz]
GAMMA = 2*pi*F
G  = 9.8         # [m/s^2] gravitational acceleration
THETA0 = pi/4    # [rad]   initial angle
V0 = 0.05        # [m/s]   initial velocity
L = 1            # [m]     length of the pendulum
DURATION = 20    # [s]     duration time
INTERVAL = 0.05  # [s]     interval time
#
# Differential equation
#
def ode(f, t):
    theta, dtheta = f
    dfdt = [dtheta, -1*(A*GAMMA*GAMMA/L) * cos(GAMMA * t) * sin(theta) - (G/L) * sin(theta)]
    return dfdt
#
# Initial condition
#
f0 = [THETA0, V0/L]    # [theta, v] at t = 0
t = np.arange(0, DURATION + INTERVAL, INTERVAL)
#
# Solve the equation
#
sol = odeint(ode, f0, t)
theta = sol[:, 0]
x = L * sin(theta)
y = - L * cos(theta) - A * cos(GAMMA*t)
#
# Prepare the screen to display the results
#
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-2*L, 2*L), ylim=(-2*L, 2*L))
ax.grid()
markers_on = [1]
line, = plt.plot([], [], 'r-o', markevery=markers_on, animated=True)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
#
# Simulate the results
#
def init():
    time_text.set_text('')
    return line, time_text

def update(i):
    circ_x = 0*t
    circ_y = -A * cos(GAMMA*t)
    next_x = [circ_x[i], x[i]]
    next_y = [circ_y[i], y[i]]
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
#ani.save('pendulum5.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
# using the Pillow instead of the imagemagic for MovieWriter
ani.save('pendulum5.gif', writer='Pillow', fps=FPS)