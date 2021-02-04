from Roller_Calc import roller_state, roller_sequence, roller_envelope
import numpy as np
import pandas as pd
import math as m
import matplotlib.pyplot as plt

def plot_all_motor(w_r1, w_r2, r_id, title, ax, I_r, d_t, n_motor, tau_motor, n_nom_motor):
    """
    Plot motor requirements for given sequence of trows
    NOTE: at the moment the program only plots the requirements for the first motor in the quad configuration

    w_r1 - roller angular velocity after throw 1 and
    w_r2 - roller angular velocity before throw 2 and

    r_id - which roller to plot

    I_r - moment of inertia roller (all four are identical)
    d_t - required time between throw 1 and 2

    n_motor - no-load speeds for reference motors
    tau_motor - stall torque for reference motors
    n_nom_motor - nominal speed for reference motors

    Comment: See markdown file for launch motors on github for explanation of calculations
    """

    n_1 = w_r2.max()*60/(2*m.pi) + 1
    n_2 = 25000
    n_0 = np.linspace(n_1, n_2, 100)

    omega_0 = np.tile((n_0*2*m.pi/60), (w_r1.shape[0], 1))

    w_r1_v = w_r1[np.newaxis]
    w_r2_v = w_r2[np.newaxis]

    n_r1 = w_r1*60/(2*m.pi)
    n_r2 = w_r2*60/(2*m.pi)

    w_r1_m = np.tile(w_r1_v.T, (1, omega_0.shape[1]))
    w_r2_m = np.tile(w_r2_v.T, (1, omega_0.shape[1]))

    w_r1_mm = np.tile(w_r1_v.T, (1, n_motor.shape[0]))
    w_r2_mm = np.tile(w_r2_v.T, (1, n_motor.shape[0]))

    n_motor = np.tile(n_motor, (w_r1.shape[0], 1))
    tau_motor = np.tile(tau_motor, (w_r1.shape[0], 1))
    omega_0_motor = n_motor*2*m.pi/60

    # Calculate curve for minimum stall torque
    tau_0 = - omega_0*I_r/d_t*np.log((w_r2_m - omega_0)/(w_r1_m - omega_0))

    # Calculate minimum d_t_0 for selected motors
    d_t_0 = I_r*(-omega_0_motor/tau_motor)*np.log((w_r2_mm - omega_0_motor)/(w_r1_mm - omega_0_motor))

    ax.title.set_text(title)
    textstr = f'max n: {np.max(n_r2):.0f} \n' \
              f'min n: {np.min(n_r2):.0f}'

    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=7,
             verticalalignment='top')

    ax.plot(n_0, tau_0[r_id, :], label=f'dt = {d_t:.1f} \n'
                                     f'n1: {n_r1[r_id]:.0f} \n'
                                     f'n2: {n_r2[r_id]:.0f}')  # n_motor[0, :], tau_motor[0, :], 'r+'
    ax.set_xlabel('no-load speed [rpm]')
    ax.set_ylabel('stall torque [Nm]')
    ax.legend()
    x_offset = [0, 0, 2500, 0]
    y_offset = [0.0, 0.0, 0, 0.0]

    for i, id in enumerate(motor_id):
        x = n_motor[r_id, i]
        y = tau_motor[r_id, i]

        ax.scatter(x, y, marker='x', color='red')
        text = f'motor id: {id} \n dt = {d_t_0[r_id, i]:.1f} \n nominal rpm: {n_nom_motor[i]}'

        ax.annotate(text, (x, y),
                     xytext=(x - x_offset[i],
                     y + y_offset[i]),
                     size=7,
                     arrowprops=dict(arrowstyle="->",
                                     connectionstyle="angle3,angleA=0,angleB=-90"))

    return d_t_0, w_r2_mm, omega_0_motor


# Input throw 1
spin_1 = np.array([0, 0])  # [rpm]
speed_1 = 0  # [km/h]

# Input throw 2
spin_2 = np.array([3000, 0])
speed_2 = 138

# Unit conversion
w1 = spin_1*(2*m.pi)/60  # rad/s
w2 = spin_2*(2*m.pi)/60  # rad/s
V = np.array([speed_1, speed_2])/3.6  # m/s

# Roller and ball parameters
m_r = 0.25*1.0  # [kg]
m_p = 0.056  # [kg]

r_r = 0.1*1.0  # [m]
r_p = 0.0677/2  # [m]
d = 0.25  # [m]

I_r_ex = 1 / 2 * m_r * r_r ** 2

d_t_ex = [5, 1.5, 1.5]  # maximum time between trow 1 and 2 [s]

param = [m_r, m_p, r_r, r_p, d]

# Get roller angular velocity after throw 1 and before throw 2
w_r1_start, w_r2_start = roller_sequence(V, w1, w2, param)
w_r1_start = np.array(w_r1_start)
w_r2_start = np.array(w_r2_start)

r_id_start = 0

df_lc, df_lc_cmb = roller_envelope()

df_max = df_lc_cmb[df_lc_cmb.d_w_max == df_lc_cmb.d_w_max.max()]
w_r1_dmax = df_max['w_r1'].iloc[0]
w_r2_dmax = df_max['w_r2'].iloc[0]
r_id_dmax = df_max['r_id'].iloc[0]

df_cont = df_lc_cmb[df_lc_cmb.lc1 == df_lc_cmb.lc2]
df_cont_max = df_cont[df_cont.d_w_max == df_cont.d_w_max.max()]
# w_r1_cont = df_cont_max['w_r1'].iloc[0]
# w_r2_cont = df_cont_max['w_r2'].iloc[0]
# r_id = df_cont_max['r_id'].iloc[0]

w_r1_cont = df_cont['w_r1'].loc[680]
w_r2_cont = df_cont['w_r2'].loc[680]
r_id_cont = df_cont['r_id'].loc[680]

w1 = [w_r1_start, w_r1_dmax, w_r1_cont]
w2 = [w_r2_start, w_r2_dmax, w_r2_cont]
r_id = [r_id_start, r_id_dmax, r_id_cont]
titles = ['start', 'max_diff', 'normal']

#  Motor examples to plot
n_0_ex = np.array([16700, 10000, 8900, 4800])
n_nom_ex = np.array([14000, 8400, 7400, 3900])
tau_0_ex = np.array([635.3, 319.4, 301.9, 183.3])*10**(-3)
motor_id = ['1', '2', '3', '4']

fig, axs = plt.subplots(1, 3, figsize=(9, 3))
for i, title in enumerate(titles):
    plot_all_motor(w1[i], w2[i], r_id[i], title, axs[i], I_r_ex, d_t_ex[i], n_0_ex, tau_0_ex, n_nom_ex)

plt.show()
# 755 series
# n_0_ex = np.array([16700, 10000, 8900, 4800])
# n_nom_ex = np.array([14000, 8400, 7400, 3900])
# tau_0_ex = np.array([635.3, 319.4, 301.9, 183.3])*10**(-3)

# 770 series
# n_0_ex = np.array([16700, 10000, 8900, 4800])
# n_nom_ex = np.array([14000, 8400, 7400, 3900])
# tau_0_ex = np.array([635.3, 319.4, 301.9, 183.3])*10**(-3)
