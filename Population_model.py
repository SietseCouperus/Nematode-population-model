# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 21:41:50 2020

@author: Sietse
"""

import numpy as np
import matplotlib.pyplot as plt

default_parameters = [330000, 4000000, 0.5, 200, 0.00826, 0.00128, 0.05, 0.05, 0.0099, 0.00215, 0.0099]

#I give the population model the optional arguments of the parameters so you do not need to add all the parameters each time you want to make the model
#You only specify the parameter that is different from the default settings
def population_model(eggs_initial, dt, Ws = default_parameters[0], K = default_parameters[1], b = default_parameters[2], eggs_per_cyst = default_parameters[3], Rae = default_parameters[4], Res = default_parameters[5], Rsc = default_parameters[6], Rcp = default_parameters[7], Ds = default_parameters[8], Rpa = default_parameters[9], Da = default_parameters[10]):
    E = eggs_initial
    S = 0
    C = 0
    P = 0
    A = 0
    X = 0
    data_points = [[0],[E],[S],[C],[P],[A],[X]]
    

    total_time = int(150/dt)
    for i in range(total_time):
        t = round((i + 1) * dt, 1) #i ranges from 0 to total_time - 1 so I add 1, round is done to reduce the number to one decimal place
        T = 12 + 7 * np.sin(0.006 * np.pi * t)
        #Define the differential equations 
        dX = 0.3 * Ws * (A + b * P)/K
        dE = eggs_per_cyst * Rae * T * A - Res * T * E * (1 - X) - 0.02 * E
        dS = Res * E * (1 - X) - Ds * S - Rsc * T * S 
        dC = Rsc * T * S - Rcp * T * C * (1 - X) - Ds * C
        dP = Rcp * T * C * (1 - X) - Rpa * T * P * (1 - X)
        dA = 0.5 * Rpa * T * P * (1 - X) - Da * A - Rae * T * A
        #Update values of the state variables
        if X >= 1:
            X = 1 #If the entire plant is infected up to carrying capacity it is dead --> X = 1
        else:
            X += dX * dt
        E += dE * dt
        S += dS * dt
        C += dC * dt
        P += dP * dt
        A += dA * dt
        

        new_data = [t, E, S, C, P, A, X]
        #append the new data to the 2D list for graphing later
        for j in range(7):
            data_points[j].append(new_data[j]) #7 columns: t, E, S, P, A, X
        
        
    return data_points
    
#print(population_model(1, 0.1)[0])

def plot_dataset(x_values, y_values, x_label, y_label):
    plt.plot(x_values, y_values)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
    
# plot_dataset(population_model(0.1, 0.1)[0], population_model(0.1, 0.1)[1], 'Time', 'Eggs')

#This function compares initial egg densities to final egg densities to compare our model with Ward (1985)
def final_vs_initial(start_range, end_range, steps):
    data_points = [[],[]]
    for i in np.arange(start_range, end_range, steps):
        new_data = [i, (population_model(i, 0.1)[1][1500])]
        data_points[0].append(new_data[0])
        data_points[1].append(new_data[1])
            
    return data_points

plot_dataset(final_vs_initial(0, 100, 1)[0], final_vs_initial(0, 100, 1)[1], 'Initial', 'Final')
            
def test_parameter_influence(parameter, start_range, end_range, steps):
    data_points = [[],[]]
    for i in np.arange(start_range, end_range, steps):
        new_data = [i, population_model(1, 0.1, parameter = i)[1][1500]]
        data_points[0].append(new_data[0])
        data_points[1].append(new_data[1])
        
    return data_points
#plot_dataset(population_model(10,0.1)[0],population_model(10,0.1)[5],'x','y')
#plot_dataset(test_parameter_influence(b, 0, 1, 0.1)[0], test_parameter_influence(b, 0, 1, 0.1)[1], 'b', 'E')
    