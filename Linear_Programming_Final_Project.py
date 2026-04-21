import numpy as np

# We are going to implement a tolerance, so that we can avoid rounding errors (this is similar to what we've done in class)
TOL = 1e-10

def standardform(c, A, b, constrain_types = None):
    """"
    This funciton will convert the linear program into standard form, by using slack variables
    
    Inputs: 
    c (list or numpy array): The coefficients of the objective function.
    A (list of list or numpy array): The coefficients of the contraints (represented as a matrix)
    b (list or numpy array): The values on the right side of the matrix
    constrain_types (list of strings): The inequalities for each of the constraints (<=, >=, =). If none, assumes <= for all.

    Outputs:
    c_std (numpy array): Standardized objective function coefficients
    A_std (numpy array): Standardized constraint matrix (with slack variables added)
    b_std (numpy array): Standardized right side values
    
    """

    # This will convert all of the inputs to float arrays. The reason we do this, is because it is easier to do mathematical operations
    c = np.array(c, dtype = float)
    A = np.array(A, dtype = float)
    b_std = np.array(b, dtype = float)

    # This defines the number of constraints (because the number of constraints is just how many elements in b_std)
    num_constraints = len(b_std)

    # We want to append an identity matrix onto A. This will act as the slack variables that do not affect profit.
    # np.hstack is a function used to link together arrays side by side
    # np.eye is the funciton for the identity matrix
    A_std = np.hstack((A, np.eye(num_constraints)))


    # This pads the objective vector with zeros because the slack variables do not affect profit
    # np.concatenate joins arrays
    # np.zeros creates a vector of only zeros with size num_constraints
    c_std = np.concatenate((c, np.zeros(num_constraints)))

    return b_std, A_std, c_std


    
