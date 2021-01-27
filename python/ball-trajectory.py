#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import pi, sin, cos, radians, sqrt, copysign
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import newton
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def projectile_motion(g, k, x0, v0, vspinyz0, tt):
    # use a four-dimensional vector function vec = [x, y, vx, vy, vspin]
    def dif(vec, t):
        # time derivative of the whole vector vec
        v = sqrt(vec[3] ** 2 + vec[4] ** 2 + vec[5] ** 2)

        cL = 1 / (2 + (v / abs(vspinyz0[0]))) if vspinyz0[0] != 0 else 0
        cS = 1 / (2 + (v / abs(vspinyz0[1]))) if vspinyz0[1] != 0 else 0

        if cL != 0 or cS != 0:
            vspin = sqrt(vspinyz0[0] ** 2 + vspinyz0[1] ** 2)
            # Drag coefficient (spinning spherical projectile)
            cD = 0.55 + 1 / (22.5 + 4.2 * (v / vspin) ** 2.5) ** 0.4
        else:
            # Drag coefficient (spherical projectile)
            cD = 0.55

        return [vec[3], vec[4], vec[5],
                - k * v * ((cD + cS) * vec[3] + cL * vec[4]),
                k * v * (copysign(1, vspinyz0[1]) * cS * vec[3] - cD * vec[4]),
                - k * v * (copysign(1, vspinyz0[0]) * cL * vec[3]
                - cD * vec[5]) - g]

    # solve the differential equation numerically
    vec = odeint(dif, [x0[0], x0[1], x0[2], v0[0], v0[1], v0[2]], tt)

    # return ((x, y, z), (vx, vy, vz))
    return (list(zip(vec[:, 0], vec[:, 1], vec[:, 2])),
            list(zip(vec[:, 3], vec[:, 4], vec[:, 5])))


class TennisBallTrajectory(object):
    # Parameters of projectile (modelled after a tennis ball)
    g = 9.81              # Acceleration due to gravity (m/s^2)
    rho_air = 1.29        # Air density (kg/m^3)
    m = 0.057             # Mass of tennis ball (kg)
    r = 0.033             # Radius of tennis ball (m)
    k = 0.5 * rho_air * pi * r ** 2 / m
    net_height = 0.95
    court_size = (20, 10, 6)
    machine_size = (0.4, 0.4)

    def __init__(self, v0, alpha0, z0=0.3, vspinyz0=(0.0, 0.0)):
        self.z0 = z0          # Initial launch height [m] (z)
        self.v0 = v0          # Initial velocity [m/s]
        self.alpha0 = alpha0  # Launch angle [°]
        self.vspinyz0 = vspinyz0  # Tan spin velocity [m/s] (r * ωy, r * ωz)
        self.p, self.gamma0 = (0., 0.), 0.
        self.solve()

    def solve(self):
        x0 = (0., 0., self.z0)
        v0 = (self.v0 * cos(radians(self.alpha0)), 0.,
              self.v0 * sin(radians(self.alpha0)))
        T_peak = newton(lambda t: projectile_motion(
            self.g, self.k, x0, v0, self.vspinyz0, [0, t])[1][1][2], 0)
        T = newton(lambda t: projectile_motion(
            self.g, self.k, x0, v0, self.vspinyz0, [0, t])[0][1][2],
            2 * T_peak)

        self.t = np.linspace(0, T, 501)
        self.x, self.v = projectile_motion(
            self.g, self.k, x0, v0, self.vspinyz0, self.t)

        self.x_trans = self.x

    def clear_net(self):
        x, _, z = list(zip(*self.x_trans))
        return np.interp(0, x, z) > self.net_height + self.r

    def clear_bounds(self):
        x, y, z = list(zip(*self.x_trans))
        return all(
            [max(max(x), abs(min(x))) <= self.court_size[0] / 2 - self.r,
             max(max(y), abs(min(y))) <= self.court_size[1] / 2 - self.r,
             max(z) <= self.court_size[2] - self.r])

    def in_court(self):
        return self.clear_bounds() and self.clear_net()

    def transform(self, p, gamma0):
        self.p, self.gamma0 = p, gamma0
        r = Rotation.from_euler('z', gamma0, degrees=True)
        x_rot = np.array([np.dot(r.as_matrix(), point) for point in self.x])
        x_trans = x_rot + (*p, 0.)
        self.x_trans = x_trans.tolist()

    def target(self):
        if self.in_court():
            return tuple(self.x_trans[-1:][0][:2])

    def print(self):
        print('Input:')
        print(f' p0: {self.p[0:2]}\n  γ: {self.gamma0}\n'
              f'  α: {self.alpha0}\n v0: {self.v0}\n'
              f'vt0: {self.vspinyz0}')

        if self.in_court():
            x, y = trajectory.target()
            print(f'\nTarget:\n  t: ({x:.2f}, {y:.2f})')
        elif self.clear_net():
            print('\nBall is out')
        else:
            print('\nBall in net')

    def plot(self):
        x, y, z = list(zip(*self.x_trans))
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(0, 20)
        X, Y = np.array([-10, 10]), np.array([-5, 5])
        X, Y = np.meshgrid(X, Y)
        Z = X * 0
        ax.plot_wireframe(X, Y, Z, color='red', linewidth=0.5)
        X, Y = np.arange(-6.95, 7, 6.95), np.arange(-5, 5.5, 5)
        X, Y = np.meshgrid(X, Y)
        Z = X * 0
        ax.plot_wireframe(X, Y, Z, color='red', linewidth=0.5)
        Y, Z = np.arange(-5, 5.5, 1), np.arange(0, 1, 0.95)
        Y, Z = np.meshgrid(Y, Z)
        X = Z * 0
        ax.plot_wireframe(X, Y, Z, color='red', linewidth=0.5)
        ax.plot(x, y, z, zdir='z', color='green')
        ax.view_init(elev=25., azim=-125)
        ax.text2D(0.05, 0.95, f'p0={self.p[0:2]} γ={self.gamma0} '
                  f'α={self.alpha0} v0={self.v0} vt0={self.vspinyz0}',
                  transform=ax.transAxes)
        plt.savefig(f'p0={self.p[0:2]} γ={self.gamma0} '
                    f' α={self.alpha0} v0={self.v0} vt0={self.vspinyz0}.pdf')


# # TennisBallTrajectory(v0, alpha0, z0=0.3, vspinyz0=(0.0, 0.0))
# trajectory = TennisBallTrajectory(15.0, 25, vspinyz0=(-9.9, 5.))
# # TennisBallTrajectory.transform((x, y), yaw)
# trajectory.transform((-8.95, -2.5), 20)
# trajectory.print()
# trajectory.plot()

if __name__ == "__main__":
    N = 3
    x = np.linspace(-9.5, -5.5, N, endpoint=True)
    y = np.linspace(-4.5, 4.5, N, endpoint=True)
    alpha =
    gamma = 
    
    x, t = np.meshgrid(x,y)
    for x, y in zip(xx, yy):
        print(x)
        print(y)



