#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import pi, sin, cos, radians, sqrt, copysign
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import newton
import matplotlib.pyplot as plt


def projectile_motion(g, k, xy0, vxy0, vspinyz0, tt):
    # use a four-dimensional vector function vec = [x, y, vx, vy, vspin]
    def dif(vec, t):
        # time derivative of the whole vector vec
        v = sqrt(vec[3] ** 2 + vec[4] ** 2 + vec[5] ** 2)
        vspin = sqrt(vspinyz0[0] ** 2 + vspinyz0[1] ** 2)
        if vspin == 0:
            # Drag coefficient (spherical projectile)
            cD, cL, cS = 0.55, 0, 0
        else:
            cD = 0.55 + 1 / (22.5 + 4.2 * (v / vspin) ** 2.5) ** 0.4
            if vspinyz0[1] == 0:
                cL = 0
            else:
                cL = copysign(1, vspinyz0[1]) / (2 + (v / abs(vspinyz0[1])))
            if vspinyz0[0] == 0:
                cS = 0
            else:
                cS = copysign(1, vspinyz0[0]) / (2 + (v / abs(vspinyz0[0])))
        return [vec[3], vec[4], vec[5],
                - k * v * (cD * vec[3] + cL * vec[4]),
                k * v * (cL * vec[3] - cD * vec[4]) - g,
                k * v * (cS * vec[3] - cD * vec[5])]

    # solve the differential equation numerically
    vec = odeint(dif, [xy0[0], xy0[1], 0, vxy0[0], vxy0[1], 0], tt)

    # return x, y, z, vx, vy, vz
    return vec[:, 0], vec[:, 1], vec[:, 2], vec[:, 3], vec[:, 4], vec[:, 5]


# Parameters of projectile (modelled after a tennis ball)
g = 9.81              # Acceleration due to gravity (m/s^2)
rho_air = 1.29        # Air density (kg/m^3)
m = 0.057             # Mass of projectile (kg)
r = 0.033            # Radius of projectile (m)
k = 0.5 * rho_air * pi * r ** 2 / m

# Initial position, launch velocity, spin and launch angle
x0 = -6.95             # Initial x-position
y0 = 0.3               # Initial y-position
v0 = 22                # Initial velocity (m/s)
vspiny0 = 9.9          # Initial tangential rotational velocity (m/s) (300rad/s)
vspinz0 = 9.9          # Initial tangential rotational velocity (m/s) (300rad/s)
alpha0 = radians(8.5)  # Launch angle (deg.)

vx0, vy0 = v0 * cos(alpha0), v0 * sin(alpha0)

T_peak = newton(lambda t: projectile_motion(g, k, (x0, y0), (vx0, vy0),
                                            (vspiny0, vspinz0), [0, t])[4][1],
                0)
y_peak = projectile_motion(g, k, (x0, y0), (vx0, vy0),
                           (vspiny0, vspinz0), [0, T_peak])[1][1]
T_net = newton(lambda t: projectile_motion(g, k, (x0, y0), (vx0, vy0),
                                           (vspiny0, vspinz0), [0, t])[0][1],
               0)
y_net = projectile_motion(g, k, (x0, y0), (vx0, vy0),
                          (vspiny0, vspinz0), [0, T_net])[1][1]
T = newton(
        lambda t: projectile_motion(g, k, (x0, y0), (vx0, vy0),
                                    (vspiny0, vspinz0), [0, t])[1][1],
        2 * T_peak)
t = np.linspace(0, T, 501)
x, y, z, vx, vy, vz = projectile_motion(g, k, (x0, y0), (vx0, vy0),
                                        (vspiny0, vspinz0), t)

print("Time of flight: {:.1f} s".format(T))
print("Horizontal range: {:.1f} m".format(x[-1] - x0))
print("Maximum height: {:.1f} m".format(y_peak))
print("Height at net: {:.1f} m".format(y_net))

# Plot of trajectory
fig, ax = plt.subplots()
ax.plot(x, y, "r-", label="Trajectory")
ax.set_title(r"Ball trajectory (XY-plane)")
ax.set_aspect("equal")
ax.set_xlim(-10,10)
ax.set_ylim(0,6)
ax.grid(b=True)
ax.legend()
ax.set_xlabel("$x$ (m)")
ax.set_ylabel("$y$ (m)")
plt.savefig("01 XY Path.png")

# Plot of trajectory
fig, ax = plt.subplots()
ax.plot(x, z, "r-", label="Trajectory")
ax.set_title(r"Ball trajectory (XZ-plane)")
ax.set_aspect("equal")
ax.set_xlim(-10,10)
ax.set_ylim(-5,5)
ax.grid(b=True)
ax.legend()
ax.set_xlabel("$x$ (m)")
ax.set_ylabel("$z$ (m)")
plt.savefig("02 XZ Path.png")

# ax = plt.axes(projection='3d')
# ax.plot3D(y, x, z, "r-")
# ax.set_xlabel("$y$ (m)")
# ax.set_ylabel("$x$ (m)")
# ax.set_zlabel("$z$ (m)")
# ax.set_xlim3d(-5, 5)
# ax.set_ylim3d(-10, 10)
# ax.set_zlim3d(0, 6)
# plt.show()
#plt.savefig("02 Path.png")
