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

##Motor Selection

Given motor stall torque, no-load speed and two roller angular speeds to go between delta t is expressed as follows:

![\Delta t \geq  I_r k_t \ln \left( \frac{\omega_2 - \omega_0}{\omega_1 - \omega_0} \right)
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5CDelta+t+%5Cgeq++I_r+k_t+%5Cln+%5Cleft%28+%5Cfrac%7B%5Comega_2+-+%5Comega_0%7D%7B%5Comega_1+-+%5Comega_0%7D+%5Cright%29%0A)

If delta t is given a threshold value the motor parameters must fulfill the criteria:


![\tau_0 \geq -\frac{\omega_0 I_r}{\Delta t}\ln \left( \frac{\omega_2 - \omega_0}{\omega_1 - \omega_0} \right)](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ctau_0+%5Cgeq+-%5Cfrac%7B%5Comega_0+I_r%7D%7B%5CDelta+t%7D%5Cln+%5Cleft%28+%5Cfrac%7B%5Comega_2+-+%5Comega_0%7D%7B%5Comega_1+-+%5Comega_0%7D+%5Cright%29)



## Create Latex in Readme 


https://tex-image-link-generator.herokuapp.com/






