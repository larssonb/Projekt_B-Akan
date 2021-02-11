from Roller_Calc import roller_state, roller_sequence, roller_envelope, inertia_roller
import numpy as np
import pandas as pd
import math as m
import matplotlib.pyplot as plt


def plot_all_motor(w_r1, w_r2, r_id, title, ax, I_r, d_t, n_motor, tau_motor, n_nom_motor):
    """
    Plot motor requirements for given sequence of throws

    w_r1 - roller angular velocity after throw 1 and
    w_r2 - roller angular velocity before throw 2 and

    r_id - which roller to plot
    title - title of plots
    ax - axis handle for subplots

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

    return d_t_0  # , w_r2_mm, omega_0_motor


def plot_all_loads(param, n_nom_motor, df_lc):

    r_r = param[2]
    r_p = param[3]
    d = param[4]

    n_0 = np.linspace(0, 5000, 5)
    omega_0 = n_0*2*m.pi/60
    vsurf_0 = omega_0*r_p
    omega_nom = n_nom_motor*2*m.pi/60

    Vp_max = -omega_0*r_p*d/(2*(r_p + r_r)) + omega_nom*r_r*d/(2*(r_p + r_r))
    Vp_min = omega_0*r_p*d/(2*(r_p + r_r))

    plt.figure('All_Loads')
    plt.plot(vsurf_0, Vp_max, label=f'Vp_max')
    plt.plot(vsurf_0, Vp_min, label=f'Vp_min')

    plt.xlabel('spin angular speed [rpm]')
    plt.ylabel('linear velocity [m/s]')
    plt.legend()
    plt.grid(True)

    for index, row in df_lc.iterrows():
        x = row[['vspinz', 'vspiny']].abs().max()
        y = row['v0']
        lc_id = row['LC']

        plt.scatter(x, y, marker='x', color='red')
        text = f'lc id: {lc_id}'

        plt.annotate(text, (x, y), xytext=(x, y), size=7)


def plot_efficiency(mark_speed, no_load_speed, efficiency, df_lc_roller):

    # calculate efficiency constant
    k_eff_1 = efficiency/mark_speed
    k_eff_2 = -efficiency/(no_load_speed - mark_speed)

    m_2 = -k_eff_2*no_load_speed

    x0 = np.array([0, mark_speed, no_load_speed])
    y0 = np.array([0, efficiency, 0])

    fig, axs = plt.subplots(1, 2, figsize=(9, 3))

    axs[0].title.set_text('efficiency max speed roller')
    axs[1].title.set_text('efficiency min speed roller')

    for ax in axs:
        ax.plot(x0, y0)
        ax.grid(True)

        ax.set_xlabel('spin angular speed of roller [rpm]')
        ax.set_ylabel('efficiency [-]')

    for index, row in df_lc_roller.iterrows():
        x_max = np.max(row['w_r0']/2/m.pi*60)
        x_min = np.min(row['w_r0']/2/m.pi*60)

        if x_max <= mark_speed:
            y_max = k_eff_1*x_max
        else:
            y_max = k_eff_2*x_max + m_2

        if x_min <= mark_speed:
            y_min = k_eff_1 * x_min
        else:
            y_min = k_eff_2 * x_min + m_2
        a = np.stack((x_max, x_min))
        b = np.stack((y_max, y_min))

        ind = np.unravel_index(np.argmin(b, axis=0), b.shape)

        x = a[ind]
        y = b[ind]

        lc_id = row['lc']
        text = f'lc id: {lc_id}'

        axs[0].scatter(x_max, y_max, marker='x', color='red')
        axs[0].annotate(text, (x_max, y_max), xytext=(x_max, y_max), size=7)

        axs[1].scatter(x_min, y_min, marker='x', color='red')
        axs[1].annotate(text, (x_min, y_min), xytext=(x_min, y_min), size=7)


# Input throw 1
spin_1 = np.array([0, 0])  # [rpm]
speed_1 = 0  # [km/h]

# Input throw 2
spin_2 = np.array([0, 0])
speed_2 = 117

# Unit conversion
w1 = spin_1*(2*m.pi)/60  # rad/s
w2 = spin_2*(2*m.pi)/60  # rad/s
V = np.array([speed_1, speed_2])/3.6  # m/s

# Roller and ball parameters
m_r = 0.25*1.0  # [kg]
m_p = 0.056  # [kg]

r_r = 0.0763*1.0  # [m] 0.079
r_p = 0.0677/2  # [m]
d = 2*r_r + 2*0.75*r_p  # [m]

I_r_ex = inertia_roller(m_r, r_r)

d_t_ex = [5, 1.5, 1.5]  # maximum time between trow 1 and 2 [s]

param = [m_r, m_p, r_r, r_p, d]

# Get roller angular velocity after throw 1 and before throw 2
w_r1_start, w_r2_start = roller_sequence(V, w1, w2, param)
w_r1_start = np.array(w_r1_start)
w_r2_start = np.array(w_r2_start)

r_id_start = 0

df_lc, df_lc_cmb, df_lc_roller = roller_envelope(param)

df_max = df_lc_cmb[df_lc_cmb.d_w_max == df_lc_cmb.d_w_max.max()]
w_r1_dmax = df_max['w_r1'].iloc[0]
w_r2_dmax = df_max['w_r2'].iloc[0]
r_id_dmax = df_max['r_id'].iloc[0]

df_cont = df_lc_cmb[df_lc_cmb.lc1 == df_lc_cmb.lc2]
df_cont_max = df_cont[df_cont.d_w_max == df_cont.d_w_max.max()]
w_r1_cont = df_cont_max['w_r1'].iloc[0]
w_r2_cont = df_cont_max['w_r2'].iloc[0]
r_id_cont = df_cont_max['r_id'].iloc[0]

# w_r1_cont = df_cont['w_r1'].loc[9]
# w_r2_cont = df_cont['w_r2'].loc[680]
# r_id_cont = df_cont['r_id'].loc[680]

w1 = [w_r1_start, w_r1_dmax, w_r1_cont]
w2 = [w_r2_start, w_r2_dmax, w_r2_cont]
r_id = [r_id_start, r_id_dmax, r_id_cont]
titles = ['start', 'max_diff', 'normal']

#  Motor examples to plot
n_0_ex = np.array([4800, 4650])
n_nom_ex = np.array([3900, 3900])
tau_0_ex = np.array([183.3, 397.1])*10**(-3)
motor_id = ['755', '770']

fig, axs = plt.subplots(1, 3, figsize=(9, 3))
for i, title in enumerate(titles):
    plot_all_motor(w1[i], w2[i], r_id[i], title, axs[i], I_r_ex, d_t_ex[i], n_0_ex, tau_0_ex, n_nom_ex)

plot_all_loads(param, 4406, df_lc)
plot_efficiency(3900, 4650, 0.74, df_lc_roller)
plt.show()
# 755 series
# n_0_ex = np.array([16700, 10000, 8900, 4800])
# n_nom_ex = np.array([14000, 8400, 7400, 3900])
# tau_0_ex = np.array([635.3, 319.4, 301.9, 183.3])*10**(-3)

# 770 series
# n_0_ex = np.array([4550, 9700, 16000, 4550])
# n_nom_ex = np.array([3500, 8400, 13500, 3900])
# tau_0_ex = np.array([334.1, 595.7, 587.9, 397.1])*10**(-3)

# 987 series OVERSIZE
# n_0_ex = np.array([5050, 10800, 13100, 11000])
# n_nom_ex = np.array([4000, 9000, 11100, 9700])
# tau_0_ex = np.array([417.6, 787.3, 676.4, 857.5])*10**(-3)

# N3_SFN series
# n_0_ex = np.array([6200, 6700, 12000, 17600])
# n_nom_ex = np.array([5400, 5800, 10700, 15800])
# tau_0_ex = np.array([297.5, 287.0, 446.8, 527.5])*10**(-3)

# GR series UNDERSIZE
# n_0_ex = np.array([6400, 6200, 6200, 6200])
# n_nom_ex = np.array([5000, 5100, 5100, 5000])
# tau_0_ex = np.array([24.5, 31.4, 33.3, 31.4])*10**(-3)

# Selection
# n_0_ex = np.array([10000, 4650])
# n_nom_ex = np.array([8400, 3900])
# tau_0_ex = np.array([319.4, 397.1])*10**(-3)
# motor_id = ['755', '770']
