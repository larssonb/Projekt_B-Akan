## Launch Motor info


### Rollers

![alt text](https://mathworld.wolfram.com/images/eps-gif/CircleCircleIntersection_1000.gif)

Ref. https://mathworld.wolfram.com/Circle-CircleIntersection.html


![\begin{align*}
a = \frac{1}{d}\sqrt{(-d+r+R)(-d-r+R)(-d+r+R)(d+r+R)}
\end{align*}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cbegin%7Balign%2A%7D%0Aa+%3D+%5Cfrac%7B1%7D%7Bd%7D%5Csqrt%7B%28-d%2Br%2BR%29%28-d-r%2BR%29%28-d%2Br%2BR%29%28d%2Br%2BR%29%7D%0A%5Cend%7Balign%2A%7D%0A)

The angle of the circle segment is derived as:

![\begin{align*}
\Beta = 2\times\arcsin{\frac{a}{2R}}
\end{align*}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cbegin%7Balign%2A%7D%0A%5CBeta+%3D+2%5Ctimes%5Carcsin%7B%5Cfrac%7Ba%7D%7B2R%7D%7D%0A%5Cend%7Balign%2A%7D%0A)

The arc length is then calculated as:

![\begin{align*}
l = r\times\Beta
\end{align*}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cbegin%7Balign%2A%7D%0Al+%3D+r%5Ctimes%5CBeta%0A%5Cend%7Balign%2A%7D%0A)

## Motor Selection
### Initial choice of DC-motor : Transmotec 770-32165-CC https://www.transmotec.se/product/770-32165-CC/
### Roller diameter : 152.6 mm
### Roller mass: 250g
### Inertia: "Disc"
### Roller Selection: https://www.swedewheel.com/en/products/wheel/wheel/pa6-(nylon)/3615040152n-wheel-150x40-pa6--nature

The DC motor operates along a stright line relating torque to angular speed. The relationship os expressed as:

![n(\tau) = k_t\tau + n_0
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+n%28%5Ctau%29+%3D+k_t%5Ctau+%2B+n_0%0A)

![\tau = \frac{n - n_0}{k_t}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ctau+%3D+%5Cfrac%7Bn+-+n_0%7D%7Bk_t%7D%0A)

![\textrm{Where}\: n_0 = \textrm{No-load}\: \textrm{speed}, \tau_0 = \textrm{Stall-torque},\: \textrm{and}\: k_t = -\frac{n_0}{\tau_0}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ctextrm%7BWhere%7D%5C%3A+n_0+%3D+%5Ctextrm%7BNo-load%7D%5C%3A+%5Ctextrm%7Bspeed%7D%2C+%5Ctau_0+%3D+%5Ctextrm%7BStall-torque%7D%2C%5C%3A+%5Ctextrm%7Band%7D%5C%3A+k_t+%3D+-%5Cfrac%7Bn_0%7D%7B%5Ctau_0%7D%0A)

Newton's second law for the roller:

![\tau = I_r\frac{d\omega}{dt}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ctau+%3D+I_r%5Cfrac%7Bd%5Comega%7D%7Bdt%7D%0A)

Using the relation between angular speed and torque for the DC motor(assuming it always opperates accordign to the relation) we obtain a differential equation for the angular speed:

![\omega' - \frac{1}{I_rk_t}\omega + \frac{\omega_0}{I_rk_t} = 0](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega%27+-+%5Cfrac%7B1%7D%7BI_rk_t%7D%5Comega+%2B+%5Cfrac%7B%5Comega_0%7D%7BI_rk_t%7D+%3D+0)

Solution to first order linear diff. equation:

![\omega(t) = Ae^{\frac{t}{I_rk_t}} + \omega_0](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega%28t%29+%3D+Ae%5E%7B%5Cfrac%7Bt%7D%7BI_rk_t%7D%7D+%2B+%5Comega_0)

Consider known angular speeds at t = 0 (w1) and t = delta_t (w2)

![\omega(0) = \omega_1](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega%280%29+%3D+%5Comega_1)

![\omega(\Delta t) = \omega_2](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega%28%5CDelta+t%29+%3D+%5Comega_2%0A)

![A = (\omega_1 - \omega_0)](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+A+%3D+%28%5Comega_1+-+%5Comega_0%29)

Given motor stall torque, no-load speed and two roller angular speeds to go between delta t is expressed as follows:

![\Delta t \geq  I_r k_t \ln \left( \frac{\omega_2 - \omega_0}{\omega_1 - \omega_0} \right)
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5CDelta+t+%5Cgeq++I_r+k_t+%5Cln+%5Cleft%28+%5Cfrac%7B%5Comega_2+-+%5Comega_0%7D%7B%5Comega_1+-+%5Comega_0%7D+%5Cright%29%0A)

If delta t is given a threshold value the motor parameters must fulfill the criteria:


![\tau_0 \geq -\frac{\omega_0 I_r}{\Delta t}\ln \left( \frac{\omega_2 - \omega_0}{\omega_1 - \omega_0} \right)](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ctau_0+%5Cgeq+-%5Cfrac%7B%5Comega_0+I_r%7D%7B%5CDelta+t%7D%5Cln+%5Cleft%28+%5Cfrac%7B%5Comega_2+-+%5Comega_0%7D%7B%5Comega_1+-+%5Comega_0%7D+%5Cright%29)

## Roller Calculations


<img src="https://github.com/larssonb/Projekt_B-Akan/blob/main/In_Progress/Launch_Motor/Roller_Ball_def.png" alt="alt text" width=600>

<img src="https://github.com/larssonb/Projekt_B-Akan/blob/main/In_Progress/Launch_Motor/Roller_Kinematics.png" alt="alt text" width=150>

Assuming the contact points between roller and ball travel at the same velocity at the moment ball and roller lose contact, the angular velocity of the rollers can be written as :

![\omega_{p1}r_r \cos(\theta) + V_p = \omega_1r_r\cos(\theta)
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega_%7Bp1%7Dr_r+%5Ccos%28%5Ctheta%29+%2B+V_p+%3D+%5Comega_1r_r%5Ccos%28%5Ctheta%29%0A)
 
![-\omega_{p1}r_r \cos(\theta) + V_p = \omega_2r_r\cos(\theta)
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+-%5Comega_%7Bp1%7Dr_r+%5Ccos%28%5Ctheta%29+%2B+V_p+%3D+%5Comega_2r_r%5Ccos%28%5Ctheta%29%0A)

![\omega_1 = \omega_{p1}\frac{r_p}{r_r}+\frac{V_p}{r_r}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega_1+%3D+%5Comega_%7Bp1%7D%5Cfrac%7Br_p%7D%7Br_r%7D%2B%5Cfrac%7BV_p%7D%7Br_r%7D%0A)

![\omega_2 = - \omega_{p1}\frac{r_p}{r_r}+\frac{V_p}{r_r}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega_2+%3D+-+%5Comega_%7Bp1%7D%5Cfrac%7Br_p%7D%7Br_r%7D%2B%5Cfrac%7BV_p%7D%7Br_r%7D%0A)

Assumptions: 
*The ratio of angluar velocity between roller 1 and 2 (3 and 4) stays the same right before anad after the throw.
*The horizontal and vertical roller pairs transfer energy to the balls linear kinetic energy equally
*Energy of the rollers and ball is conserved during the throw (no sink or production of energy)

We have:

![\frac{\omega_{10}}{\omega_20} =  \frac{\omega_{1}}{\omega_2} 
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cfrac%7B%5Comega_%7B10%7D%7D%7B%5Comega_20%7D+%3D++%5Cfrac%7B%5Comega_%7B1%7D%7D%7B%5Comega_2%7D+%0A)

![\frac{1}{2}I_r\left(\omega_10^2 + \omega_20^2\right) = \frac{1}{2}I_r\left(\omega_1^2 + \omega_2^2\right) + \frac{1}{4}m_pV_p^2 + \frac{1}{2}I_p\omega_{1p}^2](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cfrac%7B1%7D%7B2%7DI_r%5Cleft%28%5Comega_10%5E2+%2B+%5Comega_20%5E2%5Cright%29+%3D+%5Cfrac%7B1%7D%7B2%7DI_r%5Cleft%28%5Comega_1%5E2+%2B+%5Comega_2%5E2%5Cright%29+%2B+%5Cfrac%7B1%7D%7B4%7Dm_pV_p%5E2+%2B+%5Cfrac%7B1%7D%7B2%7DI_p%5Comega_%7B1p%7D%5E2)

Combining equations:

![\omega_{10} = \sqrt{\frac{\omega_1^2 + \omega_2^2}{1+\left(\frac{\omega_2}{\omega_1}\right)^2} + \frac{1/2*m_pV_p^2 + I_p\omega_{p1}^2}{I_r\left(1+\left(\frac{\omega_2}{\omega_1}\right)^2\right)}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega_%7B10%7D+%3D+%5Csqrt%7B%5Cfrac%7B%5Comega_1%5E2+%2B+%5Comega_2%5E2%7D%7B1%2B%5Cleft%28%5Cfrac%7B%5Comega_2%7D%7B%5Comega_1%7D%5Cright%29%5E2%7D+%2B+%5Cfrac%7B1%2F2%2Am_pV_p%5E2+%2B+I_p%5Comega_%7Bp1%7D%5E2%7D%7BI_r%5Cleft%281%2B%5Cleft%28%5Cfrac%7B%5Comega_2%7D%7B%5Comega_1%7D%5Cright%29%5E2%5Cright%29%7D%7D)

![\omega_{20} = \sqrt{\frac{\omega_1^2 + \omega_2^2}{1+\left(\frac{\omega_1}{\omega_2}\right)^2} + \frac{1/2*m_pV_p^2 + I_p\omega_{p1}^2}{I_r\left(1+\left(\frac{\omega_1}{\omega_2}\right)^2\right)}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega_%7B20%7D+%3D+%5Csqrt%7B%5Cfrac%7B%5Comega_1%5E2+%2B+%5Comega_2%5E2%7D%7B1%2B%5Cleft%28%5Cfrac%7B%5Comega_1%7D%7B%5Comega_2%7D%5Cright%29%5E2%7D+%2B+%5Cfrac%7B1%2F2%2Am_pV_p%5E2+%2B+I_p%5Comega_%7Bp1%7D%5E2%7D%7BI_r%5Cleft%281%2B%5Cleft%28%5Cfrac%7B%5Comega_1%7D%7B%5Comega_2%7D%5Cright%29%5E2%5Cright%29%7D%7D)

## Create Latex in Readme 


https://tex-image-link-generator.herokuapp.com/






