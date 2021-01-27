import math as m
import numpy as np
import pandas as pd


def energy_ball(w, V, m_p, r_p):
    """docstring"""

    I_p = 2 / 3 * m_p * r_p ** 2

    W_p = 1 / 2 * m_p * V ** 2 + 1 / 2 * I_p * w[0] ** 2 + 1 / 2 * I_p * w[1] ** 2

    return W_p


def energy_roller(w, m_r, r_r):
    """docstring"""

    I_r = 1 / 2 * m_r * r_r ** 2

    W_r = 1 / 2 * I_r * w ** 2

    return W_r


def roller_state(V_p, w_p, param, dual=False, quad=False):
    """
    w_p = [wp1, wp2] - angular velocity of ball wp1 (top spin), wp2 (side spin)
    V_p - linear velocity of ball

    param = [m_r,m_p,r_r,r_p,d]
    m_r - mass of roller
    m_p - mass of ball
    r_r - radius of roller
    r_p - radius of ball
    d - distance between roller axes

    dual - Two rollers (wp2 must = 0)
    quad - Four rollers
    """

    m_r = param[0]
    m_p = param[1]
    r_r = param[2]
    r_p = param[3]
    d = param[4]

    I_r = 1 / 2 * m_r * r_r ** 2
    I_p = 2 / 3 * m_p * r_p ** 2

    w = []
    w0 = []
    W_dr = []
    W_0r = []

    theta = m.asin((r_r + r_p) / d)
    if dual:

        n = 1  # n = 4 quad
        c = 1  # c = 1/2
    elif quad:

        n = 4
        c = 1 / 2

    for i in range(0, n, 2):

        if i <= 1:
            j = 0
        else:
            j = 1

        w += [V_p / (r_r * m.cos(theta)) + w_p[j] * r_p / r_r]
        w += [V_p / (r_r * m.cos(theta)) - w_p[j] * r_p / r_r]

        if w_p[j] == 0:
            w_ratio = 1
        else:
            w_ratio = w[i+1]/w[i]

        w0 += [m.sqrt(
            (w[i]**2 + w[i+1]**2) / (1 + (w_ratio)**2) + (c*m_p*V_p**2 + I_p*w_p[j]**2) / (
                        I_r*(1 + (w_ratio)**2)))]
        w0 += [m.sqrt(
            (w[i]**2 + w[i+1]**2) / (1 + (1/w_ratio)**2) + (c*m_p*V_p**2 + I_p*w_p[j]**2) / (
                        I_r*(1 + (1/w_ratio)**2)))]

        for k in range(i, i + 2):
            W_0r += [energy_roller(w0[k], m_r, r_r)]
            W_dr += [energy_roller(w[k], m_r, r_r) - W_0r[k]]

    W_kp = energy_ball(w_p, V_p, m_p, r_p)

    W_dr_array = np.array(W_dr)

    balance = W_dr_array.sum() + W_kp
    print(balance)

    return np.array(w), np.array(w0), np.array(W_dr), np.array(W_0r)

def roller_sequence(V, w1, w2, param):
    """
    Input:

    V = [V1, V2] - linear velocity of throw 1 and 2 [m/s]
    w1 = [w11, w12] - spin of throw 1 around axis 1 and 2 [rad/s]
    w2 = [w21, w22] - spin of throw 2 around axis 1 and 2 [rad/s]

    Output:

    w_r1 = roller angular speed after throw 1 [rad/s]
    w_r2 = roller angular speed before throw 2 [rad/s]
    """

    w_r1, w_pre_1, W_dr_1, W_0r_1 = roller_state(V[0], w1, param, quad=True)
    w_post_2, w_r2, W_dr_2, W_0r_2 = roller_state(V[1], w2, param, quad=True)

    return w_r1, w_r2


def test_roller_calc():

    spin = 500  # [rpm]
    speed = 0  # [km/h]

    w = spin*(2*m.pi)/60  # rad/s
    V = speed/3.6  # m/s

    m_r = 0.25*0.1  # [kg]
    m_p = 0.056  # [kg]

    r_r = 0.1*1.0  # [m]
    r_p = 0.0677/2  # [m]
    d = 0.25  # [m]

    param = [m_r, m_p, r_r, r_p, d]
    w_p = [w, w/2]
    V_p = V

    w, w0, W_dr, W_0r = roller_state(V_p, w_p, param, dual=False, quad=True)

    # Convert to RPM

    w_rmp = w/(2*m.pi)*60
    w0_rpm = w0/(2*m.pi)*60


    Results = pd.DataFrame({'w0': w0_rpm, 'w1': w_rmp, 'Wdr': W_dr, 'W0r': W_0r})

    pd.options.display.float_format = "{:.0f}".format

    print(Results)