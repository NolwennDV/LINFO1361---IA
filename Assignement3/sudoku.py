import random
import time
import math
import sys

 



def objective_score(board):
    #---|---|---#
    #---|---|---#
    #---|---|---#
    #_____________
    #---|---|---#
    #---|---|---#
    #---|---|---#
    #_____________
    #---|---|---#
    #---|---|---#
    #---|---|---#
    sameNumberLine = 0
    sameNumberColumn = 0
    sameNumerSubBoard = 0
    nonFilled = 0
    for i in range(9):
        for j in range(9):
            if(board[i][j] == 0):
                nonFilled += 1
            subBoardNumber1 = (i // 3) * 3 + (j // 3)

            for k in range(9):
                subBoardNumer2 = (i // 3) * 3 + (k // 3)
                if board[i][j] == board[i][k] and j != k and board[i][j] != 0: #0 is when not filled
                    sameNumberLine += 1
                if( board[j][i] == board[k][i] and j != k and board[j][i] != 0):
                    sameNumberColumn += 1
                if(subBoardNumber1 == subBoardNumer2 and board[i][j] == board[i][k] and j != k and board[i][j] != 0):
                    sameNumerSubBoard += 1
    return (sameNumberLine + sameNumberColumn + sameNumerSubBoard)//2 + nonFilled


def generateFixedList(board):
    editionList = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                editionList.append((i,j))
    return editionList


def simulated_annealing_solver(initial_board):

    """Simulated annealing Sudoku solver."""
    initialAction = True

    current_solution = [row[:] for row in initial_board]
    best_solution = current_solution
    
    current_score = objective_score(current_solution)
    best_score = current_score

    temperature = 1.0
    cooling_rate = 0.9999#...  #TODO: Adjust this parameter to control the cooling rate
    neighbor = current_solution
    while temperature > 0.0001:

        try:  

            # TODO: Generate a neighbor (Don't forget to skip non-zeros tiles in the initial board ! It will be verified on Inginious.)
            ...
            if(initialAction):
                initialAction = False
                for i in range(9):
                    for j in range(9):
                        if neighbor[i][j] == 0:
                            nombre_innovant = None
                            while(nombre_innovant == None or nombre_innovant in neighbor[i]):
                                nombre_innovant = random.randint(1,9)
                            neighbor[i][j] = nombre_innovant
            scorePerLine = [0,0,0,0,0,0,0,0,0] #List of numbers of duplicatas per line
            duplicatas = [[],[],[],[],[],[],[],[],[]] #List of duplicatas for each line
            scorePerColumn = [0,0,0,0,0,0,0,0,0] #List of numbers of duplicatas per line
            for i in range(9):
                for j in range(1,10,1):
                    tempoCountLine = neighbor[i].count(j)
                    tempoCountColumn = neighbor[:][i].count(j)
                    if(tempoCountLine >1):
                        scorePerLine[i] += neighbor[i].count(j)
                        duplicatas[i].append(j)
                    if(tempoCountColumn >1):
                        scorePerColumn[i] += neighbor[:][i].count(j)
            
            # Get the indices of the three maximum values in scorePerLine
            if(sum(scorePerLine) != 0):
                max_indices_line = sorted(range(len(scorePerLine)), key=lambda k: scorePerLine[k], reverse=True)[:3]
                for i in max_indices_line[0:2]:
                    #for x in neighbor[i]:
                    for j in range(9):
                        if neighbor[i][j] not in duplicatas[i]:
                            pass
                        else :
                            duplicatas[i].remove(neighbor[i][j])
                            nombre_innovant = None
                            while(nombre_innovant == None or nombre_innovant in neighbor[i]):
                                nombre_innovant = random.randint(1,9)
                            neighbor[i][j] = nombre_innovant
            else:
                max_indice_column = sorted(range(len(scorePerLine)), key=lambda k: scorePerLine[k], reverse=True)[0]
                nombre_plus_represente = max(set(neighbor[:][max_indice_column]), key=neighbor[:][max_indice_column].count)

                # Obtenir les indices de l'élément le plus représenté dans la liste
                indice_row = [i for i, x in enumerate(neighbor[:][max_indice_column]) if x == nombre_plus_represente][0] #indice de la ligne ou se trouve le numéro qui casse la colonne
                #random.shuffle(neighbor[indices_row[0]])
                nombre_innovant = None
                while(nombre_innovant == None or nombre_innovant == indice_row):
                    nombre_innovant = random.randint(0,8)
                tempoValue = neighbor[indice_row][nombre_innovant]
                neighbor[indice_row][nombre_innovant] = neighbor[indice_row][max_indice_column] #on échange le nombre avec une autre colonne aléatoire d'indice nombre innovant 
                neighbor[indice_row][max_indice_column] = tempoValue
            
                

            
           

            # Evaluate the neighbor
            neighbor_score = objective_score(neighbor)

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

    # Solving Sudoku using simulated annealing
    start_timer = time.perf_counter()

    solved_board, current_score = simulated_annealing_solver(initial_board)

    end_timer = time.perf_counter()

    print_board(solved_board)
    print("\nValue(C):", current_score)

    print("\nTime taken:", end_timer - start_timer, "seconds")