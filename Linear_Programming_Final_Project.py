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


    
def createTableau(c_std, A_std, b_std):
    """
    This function will create the tableau matrix that will be used for the Simplex algorithm.

    Inputs:
    c_std (numpy array): Standardized objective function coefficients
    A_std (numpy array): Standardized constraint matrix (with slack variables added)
    b_std (numpy array): Standardized right side values

    Outputs:
    tableau (numpy array): A 2D matrix that represents the initial Simplex state
    
    """

    # This defines the variables num_constraints and num_vars based on the number of rows and columns in A_std
    num_constraints, num_vars = A_std.shape

    # We want to pre-allocate the size of the tableau.
    # Rows will equal the number of constraints + 1 for the objective funciton
    # Columns will equal the number of variables (including the slack variables) + 1 for the RHS values
    tableau = np.zeros((num_constraints + 1, num_vars + 1))

    # Now we want to replace parts of the tableau
    # We will start by inserting standard forms into the upper portion of the tableau

    # This appends A_std to the top rows of the matrix from 0 to constraints and left most columns from 0 to vars
    tableau[:num_constraints, :num_vars] = A_std 
    # This selects the top rows from 0 to constraints and the column furthest on the right and inserts b_std
    tableau[:num_constraints, -1] = b_std

    # The objective funciton will go in the bottom row of the tableau (this will be negative to find the most negative)
    tableau[-1, num_vars] = -c_std # Very bottom row

    return tableau

def findpivcol(tableau):
    """
    This function will identify the pivot column with the most negative coefficient so as to increase profits the most

    Input:
    Tableau (numpy array): The current Simplex matrix (found above)

    Output:
    col_index (integer): The index of the chosen pivot column, or -1 if it is already optimal
    
    """

    # This will look at the objective row (the very last row), excluding the RHS values
    obj_row = tableau[-1, :-1]
    # np.argmin returns the index of the smallest element in the array
    col_index = np.argmin(obj_row)

    # If we already have the optimal solution, the most negative value is basically 0
    if obj_row[col_index] >= -TOL:
        return -1
    
    # This will return the integer value of the index
    return int(col_index)


