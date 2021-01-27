from Roller_Calc import roller_state, roller_sequence
import numpy as np
import math as m
import matplotlib.pyplot as plt

spin_1 = np.array([0, 0])  # [rpm]
speed_1 = 70  # [km/h]

spin_2 = np.array([2000, 0])
speed_2 = 138

w1 = spin_1*(2*m.pi)/60  # rad/s
w2 = spin_2*(2*m.pi)/60  # rad/s
V = np.array([speed_1, speed_2])/3.6  # m/s

m_r = 0.25*1.0  # [kg]
m_p = 0.056  # [kg]

r_r = 0.1*1.0  # [m]
r_p = 0.0677/2  # [m]
d = 0.25  # [m]

I_r = 1 / 2 * m_r * r_r ** 2

d_t = 1.5 # maximum time between trow 1 and 2 [s]

param = [m_r, m_p, r_r, r_p, d]

w_r1, w_r2 = roller_sequence(V, w1, w2, param)


def plot_all_motor(w_r1, w_r2, I_r, d_t, n_motor, tau_motor):

    n_1 = w_r2.max()*60/(2*m.pi) + 1
    n_2 = 25000
    n_0 = np.linspace(n_1, n_2, 100)

    omega_0 = np.tile((n_0*2*m.pi/60), (w_r1.shape[0], 1))

    w_r1_v = w_r1[np.newaxis]
    w_r2_v = w_r2[np.newaxis]

    # n_motor = n_motor[np.newaxis]
    # tau_motor = tau_motor[np.newaxis]

    w_r1_m = np.tile(w_r1_v.T, (1, omega_0.shape[1]))
    w_r2_m = np.tile(w_r2_v.T, (1, omega_0.shape[1]))

    w_r1_mm = np.tile(w_r1_v.T, (1, n_motor.shape[0]))
    w_r2_mm = np.tile(w_r2_v.T, (1, n_motor.shape[0]))

    n_motor = np.tile(n_motor, (w_r1.shape[0], 1))
    tau_motor = np.tile(tau_motor, (w_r1.shape[0], 1))
    omega_0_motor = n_motor*2*m.pi/60


    tau_0 = - omega_0*I_r/d_t*np.log((w_r2_m - omega_0)/(w_r1_m - omega_0))
    d_t_0 = I_r*(-omega_0_motor/tau_motor)*np.log((w_r2_mm - omega_0_motor)/(w_r1_mm - omega_0_motor))


    plt.plot(n_0, tau_0[0, :], label=f'dt = {d_t:.1f}') # n_motor[0, :], tau_motor[0, :], 'r+'
    plt.xlabel('no-load speed [rpm]')
    plt.ylabel('stall torque [Nm]')
    plt.legend()

    for i, id in enumerate(motor_id):
        x = n_motor[0, i]
        y = tau_motor[0, i]

        plt.scatter(x, y, marker='x', color='red')
        plt.text(x+.03, y+.03, f'motor id: {id} \n dt = {d_t_0[0, i]:.1f}', fontsize=7)

    plt.show()
    print(d_t_0)
    return d_t_0, w_r2_mm, omega_0_motor

n_0_motor = np.array([14600, 21000, 22000, 21000])
tau_0_motor = np.array([508.8, 806.4, 837.3, 705.9])*10**(-3)
motor_id = ['1','2','3','4']
dt_0, w_r2_mm, omega_0_motor = plot_all_motor(w_r1, w_r2, I_r, d_t, n_0_motor, tau_0_motor)
print(w_r2*60/(2*m.pi))