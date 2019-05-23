# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 00:08:53 2014

@author: Joseph
"""
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button

total_time = 7
def angle():
    t_max = 30.0
    dt = 0.01
    
    t = 0.0
    g = 9.81
    L = 1
    alpha = 0.3
    theta = np.pi
    theta_velocity = 0
    theta_acc = 0
    
    
    #xopt = [0.21168208,  1.14941678, -8.8414959] #Worst 8 sec
    #xopt = [0.37235605,  1.49999999, -0.37768177] #Best1 8 sec
    #xopt = [0.77947428,  1.49194769, -0.24689758] #Best2 8 sec
    xopt = [0.57789297,  1.55282906, -0.43313211] #Best 7 sec
    #xopt = [0.2907024 ,  1.25874185, -9.21011835] #Worst 7 sec
    
    x_acc = xopt[0]
    constant_velocity = xopt[1]
    x_decc = xopt[2]
    
    constant_velocity_start_time = constant_velocity/x_acc
    decceleration_start_time = total_time + constant_velocity/x_decc
    
    displacement =  (0.5*constant_velocity_start_time*constant_velocity +
                            constant_velocity*(decceleration_start_time-constant_velocity_start_time) +
                            0.5*(total_time-decceleration_start_time)*constant_velocity)
    print(displacement)             
    x_velocity = 0
    x_position = 0
    
    x = x_position + L*np.sin(theta)
    y = L*np.cos(theta)
    x_list = [x]
    y_list = [y]
    t_list = [0]
    x_position_list = [0]
    theta_list = []
    stop = False
    while t < t_max:
        
        x_acc = x_acc
        if t >= constant_velocity_start_time and t < decceleration_start_time:
            x_acc = 0
            x_velocity = constant_velocity
        if t >=decceleration_start_time:
            x_acc = x_decc
        if x_velocity < 0:
            stop = True
        if stop:
            x_velocity = 0
            x_acc = 0
            
        x_velocity = x_velocity + x_acc*dt
        x_position = x_position + x_velocity*dt        
        
        theta_acc = (-x_acc*np.cos(theta) + g*np.sin(theta))/(1*L) - alpha*theta_velocity/(1*L**2)
        theta_velocity = theta_velocity + theta_acc*dt
        theta = theta + theta_velocity*dt           
        x = x_position + L*np.sin(theta)
        y = L*np.cos(theta)
        t_list.append(t)
        x_list.append(x)
        y_list.append(y)
        x_position_list.append(x_position)
        theta_list.append(theta)
        t = t + dt
    return x_list, y_list, t_list, x_position_list, theta_list

pause = False
def simData():
    pos_x, pos_y, time, cart_x, theta = angle()    
    count = len(time)-2
    t = 0
    x = cart_x[0] + pos_x[0]
    y = pos_y[0]
    while t < count:
        if not pause:
            x = pos_x[t]
            y = pos_y[t]
            t = t + 2
        yield x, y, cart_x[t], 0, t*0.01

def simPoints(simData):
    x, y = simData[0], simData[1]
    x0, y0 = simData[2], simData[3]
    t0 = simData[4]
    time_text.set_text(time_template%(t0))
    line1.set_data([x0,x],[y0,y])
    line2.set_data([x0],[y0])
    return line1, line2, time_text

fig = plt.figure()
ax = fig.add_subplot(111)
plt.subplots_adjust(left=0.1, bottom=0.2)
line1, = ax.plot([], [],'-o',ms = 9)#, 'bo', ms=10) # I'm still not clear on this stucture...
line2, = ax.plot([], [],'-s',ms = 9, color = 'red')

ax.set_ylim(-1.5, 0.5)
ax.set_xlim(-1, 7)
ax.set_aspect('equal')
ax.spines['top'].set_position('zero')
ax.spines['bottom'].set_color('none')
time_template = 'Time = %.1f s'    # prints running simulation time
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

ani = animation.FuncAnimation(fig, simPoints, simData, blit=False, interval=0,
    repeat=False)
    
    
axcolor = 'lightgoldenrodyellow'
playpause_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(playpause_ax, 'Play/Pause', color=axcolor, hovercolor='0.975')
def playpause(event):
    global pause
    pause ^= True
    
#button.on_clicked(playpause)    
    
plt.show()