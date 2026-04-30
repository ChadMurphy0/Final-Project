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


