from clause import *

"""
For the n-amazon problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the n-amazons problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Here is an example presenting how to create a clause:
Let's assume that the length/width of the chessboard is 4.
To create a clause X_0_1 OR ~X_1_2 OR X_3_3
you can do:

clause = Clause(4)
clause.add_positive(0, 1)
clause.add_negative(1, 2)
clause.add_positive(3, 3)

The clause must be initialized with the length/width of the chessboard.
The reason is that we use a 2D index for our variables but the format
imposed by MiniSAT requires a 1D index.
The Clause class automatically handle this change of index, but needs to know the
number of column and row in the chessboard.

X_0_0 is the literal representing the top left corner of the chessboard
"""


def get_expression(size: int, placed_amazons: list[(int, int)]) -> list[Clause]:
    """
    Defines the clauses for the N-amazons problem
    :param size: length/width of the chessboard
    :param placed_amazons: a list of the already placed amazons
    :return: a list of clauses
    """

    expression = []

    # Clauses 1 : A amazon should only appear once per row and per column.
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if (k != j) : 
                    clause1 = Clause(size)
                    clause1.add_negative(i,j)
                    clause1.add_negative(i,k)
                    expression.append(clause1)

    for j in range(size):
        for i in range(size):
            for k in range(size):
                if (k != i) : 
                    clause2 = Clause(size)
                    clause2.add_negative(i,j)
                    clause2.add_negative(k,j)
                    expression.append(clause2)

    # Clauses 2 : An amazon should only appear once per diagonal.

    for i in range(size):
        for j in range(size):
            for k in range(size):
                if (k != i) :
                    for l in range(size):
                        if (l != j) : 
                            if (i+j == k+l):
                                clause3 = Clause(size)
                                clause3.add_negative(i,j)
                                clause3.add_negative(k,l)
                                expression.append(clause3)

    for i in range(size):
        for j in range(size):
            for k in range(size):
                if (k != i) :
                    for l in range(size):
                        if (l != j) : 
                            if (i-j == k-l):
                                clause4 = Clause(size)
                                clause4.add_negative(i,j)
                                clause4.add_negative(k,l)
                                expression.append(clause4)

    # Clausses 3 : two amazons cannot move to each other’s positions using a 3-2 move.
    
     for j in range(size):
        for i in range(size):
            N_ij = [(i+3, j+2), (i+3, j-2), (i-3, j+2), (i-3, j-2), (i+2, j+3), (i+2, j-3), (i-2, j+3), (i-2, j-3)]
            for (k, l) in N_ij: 
                if (k>=0 and k<=size-1 and l>=0 and l<= size-1):
                    clause5 = Clause(size)
                    clause5.add_negative(i,j)
                    clause5.add_negative(k,l)
                    expression.append(clause5)
    

    # Clausses 4 : two amazons cannot move to each other’s positions using a 4-1 move.

    for j in range(size):
        for i in range(size):
            N_ij = [(i+4, j+1), (i+4, j-1), (i-4, j+1), (i-4, j-1), (i+1, j+4), (i+1, j-4), (i-1, j+4), (i-1, j-4)]
            for (k, l) in N_ij: 
                if (k>=0 and k<=size-1 and l>=0 and l<= size-1) :
                    clause6 = Clause(size)
                    clause6.add_negative(i,j)
                    clause6.add_negative(k,l)
                    expression.append(clause6)
    
    # Clausses 5 : the already placed amazons Zij must be a solution of Xij.

    for i in range(size):
        for j in range(size):
            if (i, j) in placed_amazons :
                clause7 = Clause(size)
                clause7.add_positive(i,j)
                expression.append(clause7)


    # Clauses 6 : Each line must contain at least one Amazon.
    for i in range(size):
        clause8 = Clause(size)
        for j in range(size):
            clause8.add_positive(i,j)
        expression.append(clause8)

    # Clauses 7 : Each column must contain at least one Amazon
    for j in range(size):
        clause9 = Clause(size)
        for i in range(size):
            clause9.add_positive(i,j)
        expression.append(clause9)


    return expression
