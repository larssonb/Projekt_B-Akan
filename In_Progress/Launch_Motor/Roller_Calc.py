import math as m
import numpy as np
import pandas as pd
import scipy.optimize as scopt


def inertia_roller(m_r, r_r):
    """docstring"""
    
    I_r = 1/2*m_r*r_r**2
    
    return I_r
 
  
def energy_ball(w, V, m_p, r_p):
    """docstring"""

    I_p = 2 / 3 * m_p * r_p ** 2

    W_p = 1 / 2 * m_p * V ** 2 + 1 / 2 * I_p * w[0] ** 2 + 1 / 2 * I_p * w[1] ** 2

    return W_p


def energy_roller(w, m_r, r_r):
    """docstring"""

    I_r = inertia_roller(m_r, r_r)

    W_r = 1 / 2 * I_r * w ** 2

    return W_r


def roller_state(V_p, w_p, param, n=4):
    """
    w_p = [wp1, wp2] - angular velocity of ball wp1 (top spin), wp2 (side spin)   [rad/s]
    V_p - linear velocity of ball  [m/s]

    param = [m_r,m_p,r_r,r_p,d]
    m_r - mass of roller     [kg]
    m_p - mass of ball       [kg]
    r_r - radius of roller   [m]
    r_p - radius of ball     [m]
    d - distance between roller axes [m]

    n - number of rollers (2 or 4)

    Comment: See markdown file for launch motors on github for explanation of calculations
    """

    global p
    m_r = param[0]
    m_p = param[1]
    r_r = param[2]
    r_p = param[3]
    d = param[4]

    I_r = inertia_roller(m_r, r_r)
    I_p = 2 / 3 * m_p * r_p ** 2

    w = []
    w0 = []
    W_dr = []
    W_0r = []

    theta = m.acos(d/(2*(r_r + r_p)))
    
    if n == 2:
        p = 1  # n = 4 quad
        c = 2/n  # c = 1/2

    elif n == 4:
        p = 4
        c = 2/n

    for i in range(0, p, 2):

        if i <= 1:
            j = 0
        else:
            j = 1
        # Calculate angular velocity of rollers when ball leaves rollers
        w += [V_p / (r_r * m.cos(theta)) + w_p[j] * r_p / r_r]
        w += [V_p / (r_r * m.cos(theta)) - w_p[j] * r_p / r_r]

        if w_p[j] == 0:
            w_ratio = 1
        else:
            w_ratio = w[i+1]/w[i]
        # Calculate angular velocity of rollers right before ball enters rollers
        w0 += [m.sqrt(
            (w[i]**2 + w[i+1]**2) / (1 + w_ratio**2) + (c*m_p*V_p**2 + I_p*w_p[j]**2) / (
                        I_r*(1 + w_ratio**2)))]
        w0 += [m.sqrt(
            (w[i]**2 + w[i+1]**2) / (1 + (1/w_ratio)**2) + (c*m_p*V_p**2 + I_p*w_p[j]**2) / (
                        I_r*(1 + (1/w_ratio)**2)))]

        for k in range(i, i + 2):
            W_0r += [energy_roller(w0[k], m_r, r_r)]
            W_dr += [energy_roller(w[k], m_r, r_r) - W_0r[k]]

    W_kp = energy_ball(w_p, V_p, m_p, r_p)

    W_dr_array = np.array(W_dr)

    balance = W_dr_array.sum() + W_kp
    #print(balance)

    return [w, w0, W_dr, W_0r]


def roller_sequence(V, w_p1, w_p2, param):
    """
    Input:

    V = [V1, V2] - linear velocity of throw 1 and 2 [m/s]
    w_p1 = [w11, w12] - spin of throw 1 around y-axis (1) and z-axis(2) [rad/s]
    w_p2 = [w21, w22] - spin of throw 2 around y-axis (1) and z-axis(2) [rad/s]

    Output:

    w_r1 = roller angular speed after throw 1 [rad/s]
    w_r2 = roller angular speed before throw 2 [rad/s]
    """

    w_r1, w_pre_1, W_dr_1, W_0r_1 = roller_state(V[0], w_p1, param, n=4)
    w_post_2, w_r2, W_dr_2, W_0r_2 = roller_state(V[1], w_p2, param, n=4)

    return w_r1, w_r2


def test_roller_calc(inp_speed, inp_spin):

    spin = inp_spin/0.033/2/m.pi*60  # [rpm]
    speed = inp_speed*3.6  # [km/h]

    w = spin*(2*m.pi)/60  # rad/s
    V = speed/3.6  # m/s

    m_r = 0.25*0.1  # [kg]
    m_p = 0.056  # [kg]

    r_r = 0.1*1.0  # [m]
    r_p = 0.0677/2  # [m]
    d = 0.25  # [m]

    param = [m_r, m_p, r_r, r_p, d]
    w_p = [w, 0]
    V_p = V

    w, w0, W_dr, W_0r = roller_state(V_p, w_p, param, n=4)

    # Convert to RPM

    w_rpm = np.array(w)/(2*m.pi)*60
    w0_rpm = np.array(w0)/(2*m.pi)*60

    results = pd.DataFrame({'w0': w0_rpm, 'w1': w_rpm, 'Wdr': W_dr, 'W0r': W_0r})

    pd.options.display.float_format = "{:.0f}".format

    print(results)


def roller_envelope(param, path=r"C:\Users\knutn\Documents\Combitech\B_Akan\Final\LCs_mod.xlsx"):

    # path = '/Users/BjornLarsson/github/Projekt_B-Akan/Final/LCs.xlsx'

    # Read excel into dataframe
    df_lc = pd.read_excel(path)
    
    r_p = param[3]

    df_lc_cmb = pd.DataFrame(columns=['lc1', 'lc2', 'w_r1', 'w_r2', 'd_w_max', 'r_id'])
    df_lc_roller = pd.DataFrame(columns=['lc', 'w_r0', 'w_r1'])

    for index1, row1 in df_lc.iterrows():
        w_p1 = [row1['vspinz'] / r_p, -row1['vspiny'] / r_p]
        V1 = row1['v0']

        w_r11, w_r01, _, _ = roller_state(V1, w_p1, param)

        w_r11 = np.array(w_r11)
        w_r01 = np.array(w_r01)

        df_lc_roller = df_lc_roller.append({'lc': row1['LC'], 'w_r0': w_r01, 'w_r1': w_r11}, ignore_index=True)

        for index2, row2 in df_lc.loc[index1:].iterrows():

            w_p2 = [row2['vspinz'] / r_p, -row2['vspiny'] / r_p]
            V2 = row2['v0']

            w_r12, w_r02, _, _ = roller_state(V2, w_p2, param)

            w_r1 = w_r11
            w_r2 = np.array(w_r02)

            i_max = np.argmax(w_r2 - w_r1)

            d_w_max = (w_r2 - w_r1)[i_max]

            df_lc_cmb = df_lc_cmb.append({'lc1': row1['LC'], 'lc2': row2['LC'],
                                          'w_r1': w_r1, 'w_r2': w_r2,
                                          'd_w_max': d_w_max, 'r_id': i_max}, ignore_index=True)

    return df_lc, df_lc_cmb, df_lc_roller


def roller_opt(Vp, wp, w_nom, r_p):
    """Calculate roller radius for ball speed/spin and nominal speed of motor"""
    def opt_func(x):

        y = (2*x + 2*0.75*r_p)/(2*(x + r_p))*(x - wp*r_p/w_nom) - Vp/w_nom

        return y

    r_r_opt = scopt.fsolve(opt_func, 0.1)

    return r_r_opt








