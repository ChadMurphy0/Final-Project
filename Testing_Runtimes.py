# In this file, I will test the runtimes in different dimmensions

# Firstly, I would like to define a function that generates random objective functions, contraint matrices and RHS values

import random
import numpy as np
import time
import matplotlib.pyplot as plt
from Linear_Programming_Final_Project import *

def generate_random_constraints(num_vars, num_constraints):
    """
    This function will create random objective functions, constraints, and RHS values

    Inputs:
    num_values (integer): The number of variables that will be in the objective function
    num_constraints (nteger): The number of constraints in the problem

    Outputs:
    c (numpy array): Random objective function coefficients
    A (numpy array): Random constraint matrix
    b (numpy array): Random right hand side values
    
    """

    # The positive values make sure that the function is feasible and the region is bounded by x = 0
    c = np.random.rand(num_vars) * 10
    A = np.random.rand(num_constraints, num_vars) * 10
    b = np.random.rand(num_constraints) * 50 + 10

    return c, A, b

def time_simplex(dimensions_list):
    """
    This function will calculate the runtime of the Simplex algorithm with varying dimensions

    Inputs: 
    dimensions_list (list of floats): A list of numbers that will indicate which dimensions to test

    Outputs:
    simplex_times (list of floats): A list of runtimes for each of the dimensions tested
    
    """

    # Empty list that will store the values
    simplex_times = []

    for dim in dimensions_list:
        # This will call the function that we defined above, iterating through each inputted dimension to generate an objective function with constraints in dim dimensions
        c, A, b = generate_random_constraints(dim, dim)

        # This is how we tracked the time in the pi project
        start_time = time.perf_counter() # This defines the start time
        Simplex(c, A, b)
        elapsed_time = time.perf_counter() - start_time # This will output the total time taken

        simplex_times.append(elapsed_time) # Adds each of the runtimes to the list

    return simplex_times

dimensions = [5, 10, 20, 40, 80, 160, 320]
simplex_runtimes = time_simplex(dimensions) # These are the dimensions I will be testing in terms of runtime
plt.plot(dimensions, simplex_runtimes)
plt.xlabel("Number of dimensions (variables and constraints)")
plt.ylabel("Runtime in seconds")
plt.title("Runtime for Simplex algorithm dimensions comparison")
plt.grid(True)
plt.show()