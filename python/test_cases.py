#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ball_trajectory import TennisBallTrajectory


class LCBallTrajectory(TennisBallTrajectory):
    def ploty(self):
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
        ax.view_init(elev=0., azim=-90)
        ax.text2D(0.05, 0.95, f'p0={self.p[0:2]} γ={self.gamma0} '
                  f'α={self.alpha0} v0={self.v0} vt0={self.vspinyz0}',
                  transform=ax.transAxes)
        plt.savefig(f'p0={self.p[0:2]} γ={self.gamma0} '
                    f' α={self.alpha0} v0={self.v0} vt0={self.vspinyz0}'
                    ' SIDE.pdf')

    def plotz(self):
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
        ax.view_init(elev=90., azim=180)
        ax.text2D(0.05, 0.95, f'p0={self.p[0:2]} γ={self.gamma0} '
                  f'α={self.alpha0} v0={self.v0} vt0={self.vspinyz0}',
                  transform=ax.transAxes)
        plt.savefig(f'p0={self.p[0:2]} γ={self.gamma0} '
                    f' α={self.alpha0} v0={self.v0} vt0={self.vspinyz0}'
                    ' TOP.pdf')

    def print(self):
        super().print()
        x, _, z = list(zip(*self.x_trans))
        h_net = np.interp(0, x, z)
        h_max = max(z)
        print('\nHeights:')
        print(f' h_net: {h_net:.2f}\n h_max: {h_max:.2f}\n')


t_TC1 = LCBallTrajectory(10, 30, vspinyz0=(0, 0))
t_TC1.transform((-5, 0), 0)
t_TC1.ploty()
t_TC1.plotz()
t_TC1.print()

t_TC2a = LCBallTrajectory(10, 30, vspinyz0=(4, 0))
t_TC2a.transform((-5, 0), 0)
t_TC2a.ploty()
t_TC2a.print()

t_TC2b = LCBallTrajectory(10, 30, vspinyz0=(-4, 0))
t_TC2b.transform((-5, 0), 0)
t_TC2b.ploty()
t_TC2b.print()

t_TC3 = LCBallTrajectory(10, 30, vspinyz0=(0, 4))
t_TC3.transform((-5, 0), 0)
t_TC3.plotz()
t_TC3.print()
