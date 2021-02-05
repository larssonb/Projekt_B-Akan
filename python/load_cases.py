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


# ### LC1 "Serve"

# # LC 1a Serve - no side spin - "mycket lite topspin"
# t_LC1a = LCBallTrajectory(21.2, 12, vspinyz0=(3, 0))
# t_LC1a.transform((-7, -0.3), 2)
# t_LC1a.plot()
# t_LC1a.ploty()
# t_LC1a.plotz()
# t_LC1a.print()

# # LC 1b Serve - no side spin - Backspin
# t_LC1b = LCBallTrajectory(17.7, 12, vspinyz0=(-10, 0))
# t_LC1b.transform((-7, -0.3), 2)
# t_LC1b.plot()
# t_LC1b.ploty()
# t_LC1b.plotz()
# t_LC1b.print()

# # LC 1c Serve - some side spin + "mycket lite topspin"
# t_LC1c = LCBallTrajectory(21.8, 12, vspinyz0=(3, 8))
# t_LC1c.transform((-7, 0.4), -7)
# t_LC1c.plot()
# t_LC1c.ploty()
# t_LC1c.plotz()
# t_LC1c.print()

# # LC 1d Serve - some side spin + Backspin
# t_LC1d = LCBallTrajectory(17.8, 12, vspinyz0=(-10, 8))
# t_LC1d.transform((-7, 0.5), -8)
# t_LC1d.plot()
# t_LC1d.ploty()
# t_LC1d.plotz()
# t_LC1d.print()

# # LC 1e Serve - no side spin - "mycket lite topspin" diagonal
# t_LC1e = LCBallTrajectory(21.5, 12, vspinyz0=(3, 0))
# t_LC1e.transform((-7, -1), 21)
# t_LC1e.plot()
# t_LC1e.ploty()
# t_LC1e.plotz()
# t_LC1e.print()

# # LC 1f Serve - no side spin - Backspin diagonal
# t_LC1f = LCBallTrajectory(18.0, 12, vspinyz0=(-10, 0))
# t_LC1f.transform((-7, -1), 21)
# t_LC1f.plot()
# t_LC1f.ploty()
# t_LC1f.plotz()
# t_LC1f.print()

# # LC 1g Serve - some side spin - "mycket lite topspin" diagonal
# t_LC1g = LCBallTrajectory(21.7, 12, vspinyz0=(3, 8))
# t_LC1g.transform((-7, -1), 18)
# t_LC1g.plot()
# t_LC1g.ploty()
# t_LC1g.plotz()
# t_LC1g.print()

# # LC 1h Serve - some side spin - Backspin diagonal
# t_LC1h = LCBallTrajectory(18.0, 12, vspinyz0=(-10, 8))
# t_LC1h.transform((-7, -1), 18)
# t_LC1h.plot()
# t_LC1h.ploty()
# t_LC1h.plotz()
# t_LC1h.print()

# ### LC 2 "Vanligt Slag"

# # LC 2a Vanligt Slag - kort - låg - topspin
# t_LC2a = LCBallTrajectory(17.0, 16.6, vspinyz0=(10, 0))
# t_LC2a.transform((-7.5, 0.), 0)
# t_LC2a.plot()
# t_LC2a.ploty()
# t_LC2a.plotz()
# t_LC2a.print()

# # LC 2b Vanligt Slag - lång - låg - topspin
# t_LC2b = LCBallTrajectory(24.8, 12., vspinyz0=(10, 0))
# t_LC2b.transform((-7.5, 0.), 0)
# t_LC2b.plot()
# t_LC2b.ploty()
# t_LC2b.plotz()
# t_LC2b.print()

# # LC 2c Vanligt Slag - kort - hög - topspin
# t_LC2c = LCBallTrajectory(13.4, 30, vspinyz0=(10, 0))
# t_LC2c.transform((-7.5, 0.), 0)
# t_LC2c.plot()
# t_LC2c.ploty()
# t_LC2c.plotz()
# t_LC2c.print()

# # LC 2d Vanligt Slag - lång - hög - topspin
# t_LC2d = LCBallTrajectory(18.1, 23, vspinyz0=(10, 0))
# t_LC2d.transform((-7.5, 0.), 0)
# t_LC2d.plot()
# t_LC2d.ploty()
# t_LC2d.plotz()
# t_LC2d.print()

# # LC 2e Vanligt Slag - kort - låg - backspin
# t_LC2e = LCBallTrajectory(13.7, 17.5, vspinyz0=(-10, 0))
# t_LC2e.transform((-7.5, 0.), 0)
# t_LC2e.plot()
# t_LC2e.ploty()
# t_LC2e.plotz()
# t_LC2e.print()

# # LC 2f Vanligt Slag - lång - låg - backspin
# t_LC2f = LCBallTrajectory(18.1, 12.0, vspinyz0=(-10, 0))
# t_LC2f.transform((-7.5, 0.), 0)
# t_LC2f.plot()
# t_LC2f.ploty()
# t_LC2f.plotz()
# t_LC2f.print()

# # LC 2g Vanligt Slag - kort - hög - backspin
# t_LC2g = LCBallTrajectory(12, 29, vspinyz0=(-10, 0))
# t_LC2g.transform((-7.5, 0.), 0)
# t_LC2g.plot()
# t_LC2g.ploty()
# t_LC2g.plotz()
# t_LC2g.print()

# # LC 2h Vanligt Slag - lång - låg - backspin
# t_LC2h = LCBallTrajectory(15.1, 22, vspinyz0=(-10, 0))
# t_LC2h.transform((-7.5, 0.), 0)
# t_LC2h.plot()
# t_LC2h.ploty()
# t_LC2h.plotz()
# t_LC2h.print()

# # LC 2i Vanligt Slag - kort - låg - topspin - diag
# t_LC2i = LCBallTrajectory(17.0, 18, vspinyz0=(10, 0))
# t_LC2i.transform((-7.5, 0.), 18)
# t_LC2i.plot()
# t_LC2i.ploty()
# t_LC2i.plotz()
# t_LC2i.print()

# # LC 2j Vanligt Slag - lång - låg - topspin - diag
# t_LC2j = LCBallTrajectory(25.4, 12, vspinyz0=(10, 0))
# t_LC2j.transform((-7.5, 0.), 14)
# t_LC2j.plot()
# t_LC2j.ploty()
# t_LC2j.plotz()
# t_LC2j.print()

# # LC 2k Vanligt Slag - kort - hög - topspin - diag
# t_LC2k = LCBallTrajectory(14.3, 28, vspinyz0=(10, 0))
# t_LC2k.transform((-7.5, 0.), 18)
# t_LC2k.plot()
# t_LC2k.ploty()
# t_LC2k.plotz()
# t_LC2k.print()

# # LC 2l Vanligt Slag - lång - hög - topspin - diag
# t_LC2l = LCBallTrajectory(18.9, 22, vspinyz0=(10, 0))
# t_LC2l.transform((-7.5, 0.), 14)
# t_LC2l.plot()
# t_LC2l.ploty()
# t_LC2l.plotz()
# t_LC2l.print()

# # LC 2m Vanligt Slag - kort - låg - backspin - diag
# t_LC2m = LCBallTrajectory(14.4, 16.5, vspinyz0=(-10, 0))
# t_LC2m.transform((-7.5, 0.), 18)
# t_LC2m.plot()
# t_LC2m.ploty()
# t_LC2m.plotz()
# t_LC2m.print()

# # LC 2n Vanligt Slag - lång - låg - backspin - diag
# t_LC2n = LCBallTrajectory(18.9, 11, vspinyz0=(-10, 0))
# t_LC2n.transform((-7.5, 0.), 14)
# t_LC2n.plot()
# t_LC2n.ploty()
# t_LC2n.plotz()
# t_LC2n.print()

# # LC 2o Vanligt Slag - kort - hög - backspin - diag
# t_LC2o = LCBallTrajectory(12.6, 27, vspinyz0=(-10, 0))
# t_LC2o.transform((-7.5, 0.), 18)
# t_LC2o.plot()
# t_LC2o.ploty()
# t_LC2o.plotz()
# t_LC2o.print()

# # LC 2p Vanligt Slag - lång - hög - backspin - diag
# t_LC2p = LCBallTrajectory(15.6, 21, vspinyz0=(-10, 0))
# t_LC2p.transform((-7.5, 0.), 14)
# t_LC2p.plot()
# t_LC2p.ploty()
# t_LC2p.plotz()
# t_LC2p.print()

# ### LC3 "Svår Lobb"

# # LC 3a Svår lobb - rak
# t_LC3a = LCBallTrajectory(15, 50, vspinyz0=(0, 0))
# t_LC3a.transform((-7.5, 0.), 0)
# t_LC3a.plot()
# t_LC3a.ploty()
# t_LC3a.plotz()
# t_LC3a.print()

# # LC 3b Svår lobb - diag
# t_LC3b = LCBallTrajectory(15.1, 50, vspinyz0=(0, 0))
# t_LC3b.transform((-7.5, 0.), 14)
# t_LC3b.plot()
# t_LC3b.ploty()
# t_LC3b.plotz()
# t_LC3b.print()

# # LC 3c Svår lobb - rak 8m
# t_LC3c = LCBallTrajectory(16.4, 57, vspinyz0=(0, 0))
# t_LC3c.transform((-7.5, 0.), 0)
# t_LC3c.plot()
# t_LC3c.ploty()
# t_LC3c.plotz()
# t_LC3c.print()

# # LC 3d Svår lobb - diag
# t_LC3d = LCBallTrajectory(16.6, 56, vspinyz0=(0, 0))
# t_LC3d.transform((-7.5, 0.), 15)
# t_LC3d.plot()
# t_LC3d.ploty()
# t_LC3d.plotz()
# t_LC3d.print()


# ### LC4 "Lobb Bakglas"

# # LC 4a Lobb Bakglas - kort
# t_LC4a = LCBallTrajectory(11.6, 55, vspinyz0=(-15, 0))
# t_LC4a.transform((-7.5, 0.), 0)
# t_LC4a.plot()
# t_LC4a.ploty()
# t_LC4a.plotz()
# t_LC4a.print()

# # LC 4b Lobb Bakglas - lång
# t_LC4b = LCBallTrajectory(12.7, 49, vspinyz0=(-15, 0))
# t_LC4b.transform((-7.5, 0.), 0)
# t_LC4b.plot()
# t_LC4b.ploty()
# t_LC4b.plotz()
# t_LC4b.print()

# # LC 4c Lobb Bakglas - kort - diag
# t_LC4c = LCBallTrajectory(12.2, 52, vspinyz0=(-15, 0))
# t_LC4c.transform((-7.5, 0.), 27)
# t_LC4c.plot()
# t_LC4c.ploty()
# t_LC4c.plotz()
# t_LC4c.print()

# # LC 4d Lobb Bakglas - lång - diag
# t_LC4d = LCBallTrajectory(13.1, 47, vspinyz0=(-15, 0))
# t_LC4d.transform((-7.5, 0.), 21)
# t_LC4d.plot()
# t_LC4d.ploty()
# t_LC4d.plotz()
# t_LC4d.print()


# ### LC5 Lobb för smash/bandeja

# # LC 5a Lobb för smash/bandeja - kort
# t_LC5a = LCBallTrajectory(12.6, 58, vspinyz0=(0, 0))
# t_LC5a.transform((-7.5, 0.), 0)
# t_LC5a.plot()
# t_LC5a.ploty()
# t_LC5a.plotz()
# t_LC5a.print()

# # LC 5b Lobb för smash/bandeja - lång
# t_LC5b = LCBallTrajectory(14.6, 52, vspinyz0=(0, 0))
# t_LC5b.transform((-7.5, 0.), 0)
# t_LC5b.plot()
# t_LC5b.ploty()
# t_LC5b.plotz()
# t_LC5b.print()

# # LC 5c Lobb för smash/bandeja - kort - diag
# t_LC5c = LCBallTrajectory(12.9, 56, vspinyz0=(0, 0))
# t_LC5c.transform((-7.5, 0.), 22)
# t_LC5c.plot()
# t_LC5c.ploty()
# t_LC5c.plotz()
# t_LC5c.print()

# # LC 5d Lobb för smash/bandeja - lång -diag
# t_LC5d = LCBallTrajectory(14.8, 51, vspinyz0=(0, 0))
# t_LC5d.transform((-7.5, 0.), 17)
# t_LC5d.plot()
# t_LC5d.ploty()
# t_LC5d.plotz()
# t_LC5d.print()

# ### LC6 Volley

# # LC 6a Volley - kort - topspin
# t_LC6a = LCBallTrajectory(18.2, 20., vspinyz0=(10, 0))
# t_LC6a.transform((-7.5, 0.), 0)
# t_LC6a.plot()
# t_LC6a.ploty()
# t_LC6a.plotz()
# t_LC6a.print()

# # LC 6b Volley - lång - topspin
# t_LC6b = LCBallTrajectory(23.2, 18., vspinyz0=(10, 0))
# t_LC6b.transform((-7.5, 0.), 0)
# t_LC6b.plot()
# t_LC6b.ploty()
# t_LC6b.plotz()
# t_LC6b.print()

# # LC 6c Volley - kort - backspin
# t_LC6c = LCBallTrajectory(15.4, 18.0, vspinyz0=(-10, 0))
# t_LC6c.transform((-7.5, 0.), 0)
# t_LC6c.plot()
# t_LC6c.ploty()
# t_LC6c.plotz()
# t_LC6c.print()

# # LC 6d Volley - lång - backspin
# t_LC6d = LCBallTrajectory(18.1, 18.0, vspinyz0=(-10, 0))
# t_LC6d.transform((-7.5, 0.), 0)
# t_LC6d.plot()
# t_LC6d.ploty()
# t_LC6d.plotz()
# t_LC6d.print()

# # LC 6e Volley - kort - topspin - diag
# t_LC6e = LCBallTrajectory(18.4, 21., vspinyz0=(10, 0))
# t_LC6e.transform((-7.5, 0.), 15)
# t_LC6e.plot()
# t_LC6e.ploty()
# t_LC6e.plotz()
# t_LC6e.print()

# # LC 6f Volley - lång - topspin - diag
# t_LC6f = LCBallTrajectory(23.8, 18., vspinyz0=(10, 0))
# t_LC6f.transform((-7.5, 0.), 11)
# t_LC6f.plot()
# t_LC6f.ploty()
# t_LC6f.plotz()
# t_LC6f.print()

# # LC 6g Volley - kort - backspin - diag
# t_LC6g = LCBallTrajectory(15.5, 19.0, vspinyz0=(-10, 0))
# t_LC6g.transform((-7.5, 0.), 14)
# t_LC6g.plot()
# t_LC6g.ploty()
# t_LC6g.plotz()
# t_LC6g.print()

# # LC 6h Volley - lång - backspin -diag
# t_LC6h = LCBallTrajectory(18.8, 16.0, vspinyz0=(-10, 0))
# t_LC6h.transform((-7.5, 0.), 10)
# t_LC6h.plot()
# t_LC6h.ploty()
# t_LC6h.plotz()
# t_LC6h.print()

# ### LC7 Hörnspel

# # LC 7a Hörnspel - no side spin - "mycket lite topspin"
# t_LC7a = LCBallTrajectory(30.4, 9, vspinyz0=(3, 0))
# t_LC7a.transform((-7.5, -2), 21.)
# t_LC7a.plot()
# t_LC7a.ploty()
# t_LC7a.plotz()
# t_LC7a.print()

# # LC 7b Hörnspel - no side spin - Backspin
# t_LC7b = LCBallTrajectory(23.7, 8, vspinyz0=(-10, 0))
# t_LC7b.transform((-7.5, -2), 21)
# t_LC7b.plot()
# t_LC7b.ploty()
# t_LC7b.plotz()
# t_LC7b.print()

# # LC 7c Hörnspel - some side spin (pos) - "mycket lite topspin"
# t_LC7c = LCBallTrajectory(31, 9, vspinyz0=(3, 8))
# t_LC7c.transform((-7.5, -2), 17)
# t_LC7c.plot()
# t_LC7c.ploty()
# t_LC7c.plotz()
# t_LC7c.print()

# # LC 7d Hörnspel - some side spin (pos) - Backspin
# t_LC7d = LCBallTrajectory(24, 8, vspinyz0=(-10, 8))
# t_LC7d.transform((-7.5, -2), 17)
# t_LC7d.plot()
# t_LC7d.ploty()
# t_LC7d.plotz()
# t_LC7d.print()

# # LC 7e Hörnspel - some side spin (neg) - "mycket lite topspin"
# t_LC7e = LCBallTrajectory(31, 9, vspinyz0=(3, -8))
# t_LC7e.transform((-7.5, -2), 25)
# t_LC7e.plot()
# t_LC7e.ploty()
# t_LC7e.plotz()
# t_LC7e.print()

# # LC 7f Hörnspel - some side spin (neg) - Backspin
# t_LC7f = LCBallTrajectory(24, 8, vspinyz0=(-10, -8))
# t_LC7f.transform((-7.5, -2), 26)
# t_LC7f.plot()
# t_LC7f.ploty()
# t_LC7f.plotz()
# t_LC7f.print()


