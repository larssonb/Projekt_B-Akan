#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curve fit DC engine RPM to PWM duty cycle."""


import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, differential_evolution
import numpy as np
from statistics import median


def func(x, a, b, c, d):
    """Curve fit function."""
    return a * np.cos(b * x + c) + d

def inv_func(x, a, b, c, d):
    return (np.arccos((x - d) / a) - c) / b


def rasmus(x):
    return 2300 * (-np.cos(np.pi * x)+1) / 2


xdata = [0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
xflat = xdata * 8
labels = ['top+', 'top-', 'left+', 'left-',
          'bottom+', 'bottom-', 'right+', 'right-']
ydata = [[118, 294, 685, 1065, 1445, 1770, 2070, 2254, 2280, 2290],
         [74, 260, 635, 1025, 1390, 1725, 2000, 2270, 2300, 2280],
         [0, 280, 680, 1075, 1435, 1775, 2040, 2100, 2130, 2165],
         [0, 124, 690, 1110, 1485, 1760, 2030, 2140, 2130, 2100],
         [75, 313, 705, 1070, 1420, 1785, 2125, 2290, 2470, 2465],
         [85, 360, 775, 1150, 1530, 1885, 2150, 2325, 2470, 2450],
         [67, 245, 590, 935, 1240, 1570, 1790, 2000, 2050, 2040],
         [0, 285, 650, 1030, 1310, 1630, 1850, 2010, 2050, 2050]]
yflat = [y for sublist in ydata for y in sublist]
yclean = [median(yv) for yv in map(list, zip(*ydata))]

#for yd in ydata:
#    plt.scatter(xdata, yd, marker='x')
#plt.plot(xdata, yclean, marker='o')
b = [(-max(yclean), np.pi/2, -np.pi, -np.inf), (max(yclean), 3/2 * np.pi, np.pi, np.inf)]
popt, pcov = curve_fit(func, xdata, yclean, bounds=b)
print(popt)

x = np.linspace(0.15, 0.8, 100)

for yd in ydata:
    plt.scatter(yd, xdata, marker='x')
x_inv = np.linspace(70, 2230, 100)
plt.plot(x_inv, inv_func(x_inv, *popt))
plt.show()
