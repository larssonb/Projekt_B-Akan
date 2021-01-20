#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import pi, sin, cos, radians, sqrt
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import newton
import matplotlib.pyplot as plt


def projectile_motion(g, k, xy0, vxy0, vspinyz0, tt):
    # use a four-dimensional vector function vec = [x, y, vx, vy, vspin]
    def dif(vec, t):
        # time derivative of the whole vector vec
        v = sqrt(vec[2] ** 2 + vec[3] ** 2)
        vspin = sqrt(vspinyz0[0] ** 2 + vspinyz0[1] ** 2)
        if vspin == 0:
            # Drag coefficient (spherical projectile)
            cD, cL, cS = 0.55, 0, 0
        else:
            cD = 0.55 + 1 / (22.5 + 4.2 * (v / vspin) ** 2.5) ** 0.4
            cL = 1 / (2 + (v / vspinyz0[1]))
            cS = 0
        return [vec[2], vec[3],
                - k * v * (cD * vec[2] + cL * vec[3]),
                k * v * (cL * vec[2] - cD * vec[3]) - g]

    # solve the differential equation numerically
    vec = odeint(dif, [xy0[0], xy0[1], vxy0[0], vxy0[1]], tt)
    return vec[:, 0], vec[:, 1], vec[:, 2], vec[:, 3]  # return x, y, vx, vy


# Parameters of projectile (modelled after a tennis ball)
g = 9.81              # Acceleration due to gravity (m/s^2)
rho_air = 1.29        # Air density (kg/m^3)
m = 0.057             # Mass of projectile (kg)
r = 0.033            # Radius of projectile (m)
k = 0.5 * rho_air * pi * r ** 2 / m

# Initial position, launch velocity, spin and launch angle
x0 = 0.0              # Initial x-position
y0 = 0.0              # Initial y-position
v0 = 37.5             # Initial velocity (m/s)
vspiny0 = 0           # Initial tangential rotational velocity (m/s) (300rad/s)
vspinz0 = -9.4        # Initial tangential rotational velocity (m/s) (300rad/s)
alpha0 = radians(45)  # Launch angle (deg.)

vx0, vy0 = v0 * cos(alpha0), v0 * sin(alpha0)

T_peak = newton(lambda t: projectile_motion(g, k, (x0, y0), (vx0, vy0),
                                            (vspiny0, vspinz0), [0, t])[3][1],
                0)
y_peak = projectile_motion(g, k, (x0, y0), (vx0, vy0),
                           (vspiny0, vspinz0), [0, T_peak])[1][1]
T = newton(
        lambda t: projectile_motion(g, k, (x0, y0), (vx0, vy0),
                                    (vspiny0, vspinz0), [0, t])[1][1],
        2 * T_peak)
t = np.linspace(0, T, 501)
x, y, vx, vy = projectile_motion(g, k, (x0, y0), (vx0, vy0),
                                 (vspiny0, vspinz0), t)

print("Time of flight: {:.1f} s".format(T))
print("Horizontal range: {:.1f} m".format(x[-1]))
print("Maximum height: {:.1f} m".format(y_peak))

# Plot of trajectory
fig, ax = plt.subplots()
ax.plot(x, y, "r-", label="Numerical")
ax.set_title(r"Projectile path")
ax.set_aspect("equal")
ax.grid(b=True)
ax.legend()
ax.set_xlabel("$x$ (m)")
ax.set_ylabel("$y$ (m)")
plt.savefig("01 Path.png")
