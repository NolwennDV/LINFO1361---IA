from search import *
import time

#################
# Problem class #
#################

class NAmazonsProblem(Problem):
    """The problem of placing N amazons on an NxN board with none attacking
    each other. A state is represented as an N-element array, where
    a value of r in the c-th entry means there is an empress at column c,
    row r, and a value of -1 means that the c-th column has not been
    filled in yet. We fill in columns left to right.
    """
    def __init__(self, N):
        super().__init__(tuple([-1] * N))
        self.N = N

    def actions(self, state):
        """In the leftmost empty column, try all non-conflicting rows."""
        if state[-1] != -1:
            return []  # All columns filled; no successors
        else:
            col = state.index(-1)
            return [row for row in range(self.N)
                    if not self.conflicted(state, row, col)]

    def result(self, state, row):
        """Place the next amazon at the given row."""
        col = state.index(-1)
        new = list(state[:])
        new[col] = row
        return tuple(new)

    def conflicted(self, state, row, col):
        """Would placing a amazon at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two amazons in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2 or  # same / diagonal
                (abs(row2-row1) == 4) & (abs(col2-col1) == 1) or 
                (abs(row2-row1) == 1) & (abs(col2-col1) == 4) or
                (abs(row2-row1) == 3) & (abs(col2-col1) == 2) or 
                (abs(row2-row1) == 2) & (abs(col2-col1) == 3))


    def goal_test(self, state):
        """Check if all columns filled, no conflicts."""
        if state[-1] == -1:
            return False
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

    def h(self, node):
        """Return number of conflicting amazon for a given node"""
        num_conflicts = 0
        for (r1, c1) in enumerate(node.state):
            for (r2, c2) in enumerate(node.state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)

        return num_conflicts 

#####################
# Launch the search #
#####################

problem = NAmazonsProblem(int(sys.argv[1]))
start_timer = time.perf_counter()
node, nb_explored, remaining_nodes = depth_first_graph_search(problem)
end_timer = time.perf_counter()


# example of print
path = node.path()

print('Number of moves: ', str(node.depth))
i=0

grid = [["#" for _ in range(node.depth)] for _ in range(node.depth)]
amazon = node.state

for n in path:
    s = "" 
    for line in grid: 
        s += "".join(line) + "\n" 
    print(s.rstrip("\n") )
    #print(i)

    if (i<node.depth) : 
        grid[amazon[i]][i] = "A"
        print()

    i+=1
    
print("* Execution time:\t", str(end_timer - start_timer))
print("* #Nodes explored:\t", nb_explored)
print('Number of moves: ', str(node.depth))