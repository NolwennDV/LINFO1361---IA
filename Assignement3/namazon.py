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
        self.initial = State(N)

    def is_safe(self, row, col, amazons, n):
        # Check for Queen's moves: rows, columns, and diagonals
        for c in range(col):
            r = amazons[c]
            if r != -1:  # There's an Amazon in this column
                if r == row or abs(r - row) == abs(c - col):
                    return False

        # Check for extended Knight's moves
        knight_moves = [(4, 1), (4, -1), (-4, 1), (-4, -1),
                        (1, 4), (1, -4), (-1, 4), (-1, -4),
                        (3, 2), (3, -2), (-3, 2), (-3, -2),
                        (2, 3), (2, -3), (-2, 3), (-2, -3)]
        for dr, dc in knight_moves:
            knight_row, knight_col = row + dr, col + dc
            if 0 <= knight_row < n and 0 <= knight_col < col:  # Check within bounds and before the current column
                if amazons[knight_col] == knight_row:
                    return False

        return True

    def actions(self, state):
        actions = []
        print("amazons : ", state.amazons)
        col = state.amazons.index(-1)
        print("col: " + str(col))
        
        for row in range(state.n):
            if self.is_safe(row, col, state.amazons, state.n):
                actions.append(row)

        print("actions :", actions)
        return actions

    def result(self, state, row):
        
        print("amazons : ", state.amazons)
        column = state.amazons.index(-1)
        print("col: " + str(column))

        new_amazons = state.amazons[:]
        new_amazons[column] = row

        new_grid = [row[:] for row in state.grid]
        new_grid[row][column] = "A"

        if (state.nMoves == "Init"):
            new_nMoves = 1
        else :
            new_nMoves = state.nMoves + 1

        new_state = State(state.n, new_grid, new_amazons, new_nMoves)
        print("end")
        return new_state

    def goal_test(self, state):
        print(state.amazons.count(-1))
        return state.amazons.count(-1) == 0

    def h(self, node):
        h = node.state.amazons.count(-1)

        return h   

#################
# class State #
################# 
class State:

    def __init__(self, n, grid=None, amazons=None, nMoves="Init"):
        self.n = n
        if (grid == None):
            self.grid = [["#" for _ in range(n)] for _ in range(n)] 
        else :
            self.grid = grid
        if (amazons == None):
            self.amazons = [-1 for _ in range(n)]
        else :
            self.amazons = amazons
        self.nMoves = nMoves


    def __str__(self):
        s = ""
        for line in self.grid:
            s += "".join(line) + "\n"
        return s

    def __eq__(self, other):
        return (isinstance(other, State) and self.grid == other.grid and self.amazons == other.amazons and self.nMoves == other.nMoves)

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __hash__(self):
        return hash(str(self.nMoves))

#####################
# Launch the search #
#####################

problem = NAmazonsProblem(int(sys.argv[1]))

start_timer = time.perf_counter()

node = breadth_first_tree_search(problem)

end_timer = time.perf_counter()


# example of print
path = node.path()

print('Number of moves: ', str(node.depth))

for n in path:

    print(n.state)  # assuming that the _str_ function of state outputs the correct format

    print()
    
print("Time: ", end_timer - start_timer)