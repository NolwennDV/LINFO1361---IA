import random
import time
import math
import sys

def objective_score(board):
    size = 9
    sameNumberLine = [set() for _ in range(size)]
    sameNumberColumn = [set() for _ in range(size)]
    sameNumberSubBoard = [[set() for _ in range(size // 3)] for _ in range(size // 3)]
    nonFilled = 0

    errors = 0

    for i in range(size):
        for j in range(size):
            num = board[i][j]
            if num == 0:
                nonFilled += 1
            else:
                block_row = i // 3
                block_col = j // 3

                if num in sameNumberLine[i]:
                    errors += 1
                else:
                    sameNumberLine[i].add(num)

                if num in sameNumberColumn[j]:
                    errors += 1
                else:
                    sameNumberColumn[j].add(num)

                if num in sameNumberSubBoard[block_row][block_col]:
                    errors += 1
                else:
                    sameNumberSubBoard[block_row][block_col].add(num)

    return errors + nonFilled

def generateFixedList(board):
    fixedList = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                fixedList.append((i, j))
    return fixedList

def simulated_annealing_solver(initial_board):

    """Simulated annealing Sudoku solver."""
    initialAction = True

    neighbor = [row[:] for row in initial_board]
    
    #REMPLIR LA GRILLE DE DEPART
    for i in range(9):
        for j in range(9):
            if neighbor[i][j] == 0:
                nombre_innovant = 0
                while(nombre_innovant == 0 or neighbor.count(nombre_innovant) >= 9): #On continue a itérer pour obtenir un random por le premier cas ou si le nombre est déja suffisemment de fois dans la grille
                    nombre_innovant = random.randint(1,9)
                neighbor[i][j] = nombre_innovant
    
    current_solution = neighbor


    best_solution = current_solution
    
    current_score = objective_score(current_solution)
    best_score = current_score

    temperature = 1.0
    cooling_rate = 0.999#...  #TODO: Adjust this parameter to control the cooling rate
    while temperature > 0.0001:
        

        try:  

            # Generate a neighbor
            neighbor = [row[:] for row in current_solution]

            #Choisir nombre de case qu'on va modifier, on va d'abord en échanger de manière aléatoire et ensuite essayer de régler les conflits
            numberOfChanges = max(int(temperature*current_score//3),1)
            print("Number of changes:", numberOfChanges)
            for i in range(numberOfChanges): #On fait des modifs aléatoires
                i1, j1, i2, j2 = 0, 0, 0, 0
                while(i1 == i2 and j1 == j2):
                    i1, j1 = random.choice(editableList)
                    i2, j2 = random.choice(editableList)
                neighbor[i1][j1], neighbor[i2][j2] = neighbor[i2][j2], neighbor[i1][j1]
            
            #numberOfChanges = max(int(temperature*objective_score(neighbor)),1)
            tries =  max(int(temperature*objective_score(neighbor)),1)  # Limit attempts to avoid infinite loop
            print("Tries:", tries)
            while tries > 0 and objective_score(neighbor) >= current_score:
                i3, j3 = random.choice(editableList)
                k = random.randint(1, 9)
                temp = neighbor[i3][j3]
                neighbor[i3][j3] = k
                if objective_score(neighbor) < current_score:
                    break
                neighbor[i3][j3] = temp
                tries -= 1



            # Evaluate the neighbor
            neighbor_score = objective_score(neighbor)
            print_board(neighbor)
            print("Value(C):", neighbor_score)
            #time.sleep(1)

            # Calculate acceptance probability
            delta = float(current_score - neighbor_score)

            if current_score == 0:

                return current_solution, current_score

            # Accept the neighbor with a probability based on the acceptance probability
            if neighbor_score < current_score or (neighbor_score > 0 and math.exp((delta/temperature)) > random.random()):

                current_solution = neighbor
                current_score = neighbor_score

                if (current_score < best_score):
                    best_solution = current_solution
                    best_score = current_score

            # Cool down the temperature
            temperature *= cooling_rate
        except:

            print("Break asked")
            break
        
    return best_solution, best_score

 
def print_board(board):

    """Print the Sudoku board."""
    print(board)

    for row in board:
        print("".join(map(str, row)))

 

def read_sudoku_from_file(file_path):
    """Read Sudoku puzzle from a text file."""
    
    with open(file_path, 'r') as file:
        sudoku = [[int(num) for num in line.strip()] for line in file]

    return sudoku
 

if __name__ == "__main__":

    # Reading Sudoku from file
    initial_board = read_sudoku_from_file(sys.argv[1])
    fixedList = generateFixedList(initial_board)
    editableList = [(i, j) for i in range(9) for j in range(9) if (i, j) not in fixedList]

    # Solving Sudoku using simulated annealing
    start_timer = time.perf_counter()

    solved_board, current_score = simulated_annealing_solver(initial_board)

    end_timer = time.perf_counter()

    print_board(solved_board)
    print("\nValue(C):", current_score)

    print("\nTime taken:", end_timer - start_timer, "seconds")