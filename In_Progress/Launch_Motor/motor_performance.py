import matplotlib.pyplot as plt
import math as m
import numpy as np

def motor_performance(no_load_RPM = 5000.0, stall_torque = 200.0):
    """Plot the performance curves of a given Brushed DC Motor.

     Keyword arguments:
     no_load_speed -- The no load speed of motor (default 5000 rpm)
     imag -- The stall torque of the motor (default 200.0 mNm)
     """

    # Convert to SI-units
    no_load_speed = ((2*m.pi)/60)*no_load_RPM
    stall_torque = stall_torque/1000

    # calculate torque constant
    kt = -no_load_speed/stall_torque

    # Calculate speed as a function of torque omega(tau)
    torque = np.linspace(0, stall_torque, 50)
    speed = kt*torque + no_load_speed
    speed_rpm = speed*60/(2*m.pi)

    power = -(stall_torque/no_load_speed)*speed**2\
            + stall_torque*speed

    fig, ax = plt.subplots()
    ax.plot(torque, speed_rpm, 'r-', label='Speed vs. Torque')
    ax.set_xlabel(r'$\tau$ [Nm]', fontsize=12)
    ax.set_ylabel('Speed [RPM]', color="red", fontsize=12)

    ax2 = ax.twinx()
    ax2.plot(torque, power, 'b-', label='Power vs. Torque')
    ax2.set_ylabel('Power [watt]', color="blue", fontsize=12)

    plt.title('Speed and Power Vs. Torque')
    fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)
    plt.show()

motor_performance(10000, 319.4)




