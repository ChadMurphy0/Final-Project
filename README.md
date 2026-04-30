# Final-Project
Linear Programming Final Project

## (1) Description

In this project, I was faced with the problem of linear programming. Given an objective function (a function that I would like to maximiaze) and a certain amount of constraints, can I create a program that would output the most optimal answer? For example, I want the largest amount of profit, given the restraints of producing a certain amount of goods. 


(2) Vocabulary

Objective function: The profit function of producing two goods
Constraints: The restrictive functions on what goods can be produced
Feasible Region: The region where all constraints are met - there will be an edge case where the objective function is maximized
Vertex: The solution to our problem will be on the edge of the constraints (or the vertex). This will eventually be the output of our function. 


(3) Background

Visually, we can graph all of the constraints on the cartesian plane (for a 2D problem). Once we have done that, we will be able to see a visual representation of the feasibility region. We can then plot our profit function at certain c values (where c is a constant that represents profit). There will be an edge case where we continually move up the profit maximization function until the very border of the constraints on the graph. This will need to be coded so that given any linear constraints and any linear profit maximization function, there will be an output with the optimal profit as well as the amount of each good to be produced. The code must also be able to sense if the constraints are too loose or too tight (no solution or a solution that is infinitely large). 

This visualization from above is all in a 2d example, with only two goods being produced. However, there are infinitely many goods that a company could produce. This function should be able to give an answer given infinite inputs. 




## ()

File breakdown (for clarity):

Linear_Programming_Main_Code.py: This is the meat of the code for the project. This file defines my whole created algorithm. It iterates through 6 different functions that eventually culminate in the final function (Simplex). There is nothing to be printed in this file, but rather for it to be run first so all other files can draw on the code.

Profit_Max_Problem.py:
This file implements the application of the code. For a given profit function, good 1 constraint, good 2 constraint, combined constarint, and RHS values, it will output the maximum profit as well as the allocation of each good. The user can change the inputs (c, A, b). C is the profit function, A is the constraint matrix, and b has the RHS values. Currently, they are based on the word problem as described in the comment at the beginning. This is then compared to the SciPi linear programming function. Since they are the same, our algorithm is correct!

Testing_Runtimes.py:
This file does two things.
(1) It compares the runtime as we increase the dimmensions of our created Simplex function. The user can change the dimmensions list to input the dimmensions they would like to test. It then graphs these runtimes as a function of dimmensions vs. runtime. 

(2) This function graphs the runtime of the SciPi linear programming function in the same dimmensions. This means we can compare how the runtimes differ between our created function and the SciPi function.
