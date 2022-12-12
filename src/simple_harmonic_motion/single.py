import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
#
# Constants
#
G = 9.8                 # [m/s^2] acceleration of gravity
THETA0 = pi/4.      # [rad]   initial angle
V0 = 1.          # [m/s]   initial velocity
L = 1.           # [m]     length of the pendulum
DURATION = 10.   # [s]     duration time
INTERVAL = 0.05  # [s]     interval time
#
# Differential Equation
#
def ode(f, t):
    theta, dtheta = f
    dfdt = [dtheta, -(G/L) * sin(theta)]
    return dfdt
#
# Initial condition
#
f0 = [THETA0, V0/L]    # [theta, v] at t = 0
t = np.arange(0, DURATION + INTERVAL, INTERVAL)    # domain of definition
#
# Solve the equation
#
sol = odeint(ode, f0, t)
theta = sol[:, 0]
x = L * sin(theta)
y = - L * cos(theta)   # coordinates of the mass point
#
# Prepare the Screen to display
#
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-L, L), ylim=(-L, L))
ax.grid()
markers_on = [1]
line, = plt.plot([], [], 'ro-', markevery=markers_on, animated=True)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
#
# Animate the simulated results 
#
def init():
    time_text.set_text('')
    return line, time_text

def update(i):
    next_x = [0, x[i]]
    next_y = [0, y[i]]
    line.set_data(next_x, next_y)
    time_text.set_text(time_template % (i*INTERVAL))
    return line, time_text

FRAME_INTERVAL = 1000 * INTERVAL # [msec] interval between frames
ani = FuncAnimation(fig, update, frames=np.arange(0, len(t)),
                    interval=FRAME_INTERVAL, init_func=init, blit=True)
#
# Show on the screen and Save the results
#
plt.show()
FPS = 1000/FRAME_INTERVAL # frames per second
#ani.save('single_pendulum.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
ani.save('single_pendulum.gif', writer='imagemagick', fps=FPS)
