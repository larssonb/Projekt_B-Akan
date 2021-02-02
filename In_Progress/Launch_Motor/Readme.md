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


<img src="https://github.com/larssonb/Projekt_B-Akan/blob/main/In_Progress/Launch_Motor/Rollers.jpg" alt="alt text" width=300>
<img src="https://github.com/larssonb/Projekt_B-Akan/blob/main/In_Progress/Launch_Motor/Ball.jpg" alt="alt text" width=300>



## Create Latex in Readme 


https://tex-image-link-generator.herokuapp.com/






