import numpy as np

# We are going to implement a tolerance, so that we can avoid rounding errors (this is similar to what we've done in class)
TOL = 1e-10

def standardform(c, A, b, constraint_types = None):
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
    tableau[-1, :num_vars] = -c_std # Very bottom row

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

def findpivrow(tableau, col_index):
    """
    This function will perform the minimum ratio test. This means that it will divide the right side constants by the positive coefficients in the pivot column
    This tells us which constraint becomes the "bottleneck" first

    Inputs:
    tableau (numpy array): The current Simplex matrix
    col_index (integer): The pivot column we found in the previous function

    Output:
    row_index (integer): The index of the pivot row
    
    """

    # This will define our RHS values and our column values (from the pivot column)
    rhs = tableau[:-1, -1]
    col_vals = tableau[:-1, col_index]

    # This makes sure that values are only divided if they are positive
    valid = col_vals > TOL

    # If there are no positive values, then it will return a value error
    # np.any tests if there is any value in the array meets a certain condition
    if not np.any(valid):
        raise ValueError("The problem does not have bounds")

    # We will initialize all ratios with infinity in the list, so when we pick the minimum, they won't effect it
    ratios = np.full(len(rhs), np.inf)

    # Compute the ratio (RHS / column value) for valid rows
    ratios[valid] = rhs[valid] / col_vals[valid]

    # Find the one with the smallest positive ratio, or the "bottleneck"
    row_index = np.argmin(ratios)

    # Makes the row_index value an integer
    return int(row_index)

def pivot(tableau, row_index, col_index):
    """
    This will perform the row operations to zero out the pivot column

    Inputs:
    tableau (numpy array): The current Simplex matrix
    row_index (integer): The pivot row we found
    col_index (integer): The pivot colum we found

    Output:
    tableau (numpy array): The updated Simplex matrix after row operations

    """

    # We first want to normalize the pivot row, so that the pivot number becomes 1
    tableau[row_index, :] = tableau[row_index, :] / tableau[row_index, col_index] # We are dividing all of the elements in the row

    # Next we want to subtract the multiples of the pivot row from all of the other rows
    factors = tableau[:, col_index].copy() # This creates a copy of the object
    factors[row_index] = 0 # Set the pivot row's factor to 0 so we don't subtract it from itself

    # The np.newaxis will transform flat 1D lists into 2D column vectors. Then, we multiply this vector by the horizontal pivot row. This does matrix math for us. 
    tableau = tableau - factors[:, np.newaxis] * tableau[row_index, :]

    return tableau

def Simplex(c, A, b, constraint_types = None):
    """
    This function will perform the Simplex algorithm, combing all of the functions we have defined above
    
    Inputs:
    c (list or numpy array): The objective function coefficients.
    A (list of list or numpy array): The constraint matrix.
    b (list or numpy array): The RHS constraint values
    constrain_types (list of strings): The inequalities for each of the constraints (<=, >=, =). If none, assumes <= for all.
    
    Ouputs:
    x (numpy array): The optimal solution vector for the original variables
    max_profit (float): The maximum profit given the optimal solution

    """

    # Standardize our equations
    b_std, A_std, c_std = standardform(c, A, b, constraint_types)

    # Create the initial tableau
    tableau = createTableau(c_std, A_std, b_std)

    # We will want to continually pivot until we have our optimal solution
    # Therefore, we want a loop. This loop will continually run until col_index = 1.
    while True:
        col_index = findpivcol(tableau)
        if col_index == -1: # This is what we have designated as finding the optimal solution
            break

        # Here, we are simply calling our functions of finding the pivot row and performing the row operations.
        row_index = findpivrow(tableau, col_index)
        tableau = pivot(tableau, row_index, col_index)

    # Extract out the optimal solution vector x
    num_original_vars = len(c)

    # This will make all of the elements 0 based on the length
    x = np.zeros(num_original_vars)

    # We will now check each column belonging to the original variables
    for j in range(num_original_vars):
        col = tableau[:-1, j]
        
        # A basic variable will have the entry of 1 (since row operations will make this the case)
        # We will use the TOL that we defined early on to account for some of the float inaccuracies

        # This one line of code will add up all of the numbers in the column (which should be many 0s and one 1) and then subtracts by the largest number (which should be 1)
        # This will produce 0, which should be less than TOL
        # This also checks to make sure the largest number is 1. 
        if np.sum(np.abs(col)) - np.max(np.abs(col)) < TOL and np.abs(np.max(col) - 1.0) < TOL:

            # This will locate the index that the 1 is located in
            row_index = np.argmax(np.abs(col))

            # We then look at the RHS value of this column, and put that number in x
            x[j] = tableau[row_index, -1]

    # The max profit is in the bottom right corner of the tableau, as this is essentially a running total (every pivot this will update with the profit)
    max_profit = tableau[-1, -1]

    return x, max_profit

