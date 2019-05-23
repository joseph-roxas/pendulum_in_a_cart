# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 17:53:59 2014

@author: Joseph
"""

from __future__ import division
import numpy as np
from scipy.optimize import minimize

total_time = 7

def angle(xy):
    t_max = 30.0
    dt = 0.01
    
    t = 0.0
    g = 9.81
    L = 1
    alpha = 0.3
    theta = np.pi
    theta_velocity = 0
    theta_acc = 0
    
    x_acc = xy[0]
    constant_velocity = xy[1]
    x_decc = xy[2]
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
        if t >= total_time:        
            theta_list.append(abs(theta-np.pi))
        t = t + dt
        
    area = 0
    for i in range(len(theta_list)-1):
        area += 0.5*(theta_list[i]+theta_list[i+1])*dt
    return area #1/area to get the worst and area to get the best

cons = ({'type': 'ineq', 'fun': lambda x: x[0]},
        {'type': 'ineq', 'fun': lambda x: x[1]},
        {'type': 'ineq', 'fun': lambda x: -x[2]},
        {'type': 'ineq', 'fun': lambda x: total_time+x[1]/x[2]-x[1]/x[0]},
        {'type': 'eq', 'fun': lambda x: total_time*x[1] - 0.5*(1/x[0]-1/x[2])*x[1]**2-6})

x0 = [ 0.57797363,  1.55240926, -0.43313443]
#x0 = [accelleration, constant velocity, decelleration]

xopt = minimize(angle, x0, method="SLSQP",constraints=cons, options={'disp': True})

print("[{}, {}, {}]".format(xopt.x[0], xopt.x[1], xopt.x[2]))
