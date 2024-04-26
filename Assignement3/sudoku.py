import random
import time
import math
import sys
from collections import deque

myQueue = deque()

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
                    #print(f"Doublon dans ligne {i}: {num}")
                    errors += 1
                else:
                    sameNumberLine[i].add(num)

                if num in sameNumberColumn[j]:
                    #print(f"Doublon dans colonne {j}: {num}")
                    errors += 1
                else:
                    sameNumberColumn[j].add(num)

                if num in sameNumberSubBoard[block_row][block_col]:
                    #print(f"Doublon dans bloc {block_row},{block_col}: {num}")
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
                while(nombre_innovant == 0 or sum([neighbor[p].count(nombre_innovant) for p in range (9) ]) >= 9): #On continue a itérer pour obtenir un random por le premier cas ou si le nombre est déja suffisemment de fois dans la grille
                    nombre_innovant = random.randint(1,9)
                neighbor[i][j] = nombre_innovant
    
    current_solution = neighbor


    best_solution = current_solution
    
    current_score = objective_score(current_solution)
    best_score = current_score

    temperature = 1.0
    cooling_rate = 0.9999#...  #TODO: Adjust this parameter to control the cooling rate
    delta = 1
    while temperature > 0.0001:
        

        try:  

            # Generate a neighbor
            neighbor = [row[:] for row in current_solution]

            stuck = True
            #print("Current solution:")
            #print_board(current_solution)
            current_max = int(abs(delta))

            numberOfChanges = max(int(temperature*objective_score(neighbor)//2),current_max)
            #print("Current score:", current_score)
            #print("Number of changes:", numberOfChanges)
            if(delta > 0): numberOfChanges = 0
            elif(meanDelta <= 0): numberOfChanges = 10


            if(1):
                for i in range(numberOfChanges): #On fait des modifs aléatoires
                    i1, j1, i2, j2 = 0, 0, 0, 0
                    while(i1 == i2 and j1 == j2):
                        i1, j1 = random.choice(editableList)
                        i2, j2 = random.choice(editableList)
                    neighbor[i1][j1], neighbor[i2][j2] = neighbor[i2][j2], neighbor[i1][j1]
                
            #Choisir nombre de case qu'on va modifier, on va d'abord en échanger de manière aléatoire et ensuite essayer de régler les conflits
            duplicateList = []
            # #print("Avant fixing")
            for i in range(9):
                for j in range(1, 10, 1):
                    # Trouver les doublons dans les lignes
                    if neighbor[i].count(j) > 1:
                        # Rechercher tous les indices de 'j' dans la ligne 'i'
                        indices = [k for k, x in enumerate(neighbor[i]) if x == j]
                        # Ajouter à duplicateList les indices non fixes
                        for index in indices:
                            if (i, index) not in fixedList and (i, index) not in duplicateList:
                                duplicateList.append((i, index))
                                break  # Ajouter seulement le premier non-fixe

                    # Trouver les doublons dans les colonnes
                    tempoColumns = [neighbor[x][i] for x in range(9)]
                    if tempoColumns.count(j) > 1:
                        indices = [k for k, x in enumerate(tempoColumns) if x == j]
                        for index in indices:
                            if (index, i) not in fixedList and (index, i) not in duplicateList:
                                duplicateList.append((index, i))
                                break  # Ajouter seulement le premier non-fixe

                    # Trouver les doublons dans les blocs 3x3
                    block_start_row = (i // 3) * 3
                    block_start_col = (i % 3) * 3
                    tempoSquare = [neighbor[x][y] for x in range(block_start_row, block_start_row + 3) for y in range(block_start_col, block_start_col + 3)]
                    if tempoSquare.count(j) > 1:
                        indices = [k for k, x in enumerate(tempoSquare) if x == j]
                        for index in indices:
                            row, col = index // 3 + block_start_row, index % 3 + block_start_col
                            if (row, col) not in fixedList and (row, col) not in duplicateList:
                                duplicateList.append((row, col))
                                break  # Ajouter seulement le premier non-fixe




            #PAS TOUCHE 
            
            #print("Number of duplicates:", len(duplicateList))
            #print("Score neighbour:", objective_score(neighbor))
            #print("list before fixing:")
            #print_board(neighbor)
            #print("duplicateList:", duplicateList)
            #print("Number of each number in the board:", [sum([neighbor[i].count(j) for i in range(9)]) for j in range(1, 10, 1)])
            for i in range(len(duplicateList)):
                (i1,j1) = random.choice(duplicateList)
                (i2,j2) = random.choice(duplicateList)
                # #print("indexes:", i1, j1, i2, j2)

                neighbor[i1][j1], neighbor[i2][j2] = neighbor[i2][j2], neighbor[i1][j1] 
            # #print("After fixing")
            
            


            # Evaluate the neighbor
            neighbor_score = objective_score(neighbor)
            #print_board(neighbor)
            #print("Value(C):", neighbor_score)
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