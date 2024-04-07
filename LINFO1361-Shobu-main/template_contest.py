from agent import Agent
import random
import time
import heapq
import numpy as np

totalTimeSorting = 0
totalTimeEvaluating = 0
MAX_DEPTH_LIMIT = 5

class AI(Agent):
    """An agent that plays following your algorithm.

    This agent extends the base Agent class, providing an implementation your agent.

    Attributes:
        player (int): The player id this agent represents.
        game (ShobuGame): The game the agent is playing.
    """
    def __init__(self, player, game):
        """Initializes an AlphaBetaAgent instance with a specified player, game, and maximum search depth.

        Args:
            player (int): The player ID this agent represents (0 or 1).
            game (ShobuGame): The Shobu game instance the agent will play on.
            max_depth (int): The maximum depth of the search tree.
        """
        super().__init__(player, game)
        self.max_depth = 3
        self.initial_max_depth = 2
        self.time_budget = None
        self.lastTime = 1.9

    def play(self, state, remaining_time):
        """Determines the best action by applying the alpha-beta pruning algorithm.

        Overrides the play method in the base class.

        Args:
            state (ShobuState): The current state of the game.
            remaining_time (float): The remaining time in seconds that the agent has to make a decision.

        Returns:
            ShobuAction: The action determined to be the best by the alpha-beta algorithm.
        """
        
        if (self.time_budget == None) :
            self.time_budget = remaining_time
        start_search_depth = time.time()
        self.adjust_search_depth(remaining_time, state)
        #print("time to perform depth adjustment = ", time.time() - start_search_depth)
        start = time.time()
        search = self.alpha_beta_search(state)
        end = time.time()
        self.lastTime = end - start
        print("Total time elapsed to compute next action (agentMain) = ", end - start)
        return search
   
    def adjust_search_depth(self, remaining_time, state):
        if self.time_budget is not None:
            # Calculer le temps moyen par mouvement
            time_per_move = remaining_time / max(1, len(state.actions))

            # Si le temps par mouvement est supérieur à un seuil arbitraire
            piecesPlayer, _, totPiecesPlayer, totPiecesOpponent = self.numberOfPiece(state)
            totPieces = totPiecesPlayer + totPiecesOpponent
            print("total pieces = ", totPieces)
            if ((time_per_move > self.time_budget * 0.009 and self.lastTime < 2) or (piecesPlayer < 3 and time_per_move > self.time_budget * 0.005 and self.lastTime < 4)):
                # Augmenter la profondeur si la profondeur maximale n'a pas encore été atteinte
                if self.max_depth < MAX_DEPTH_LIMIT:  # Définir MAX_DEPTH_LIMIT en fonction de vos besoins
                    if((self.max_depth == MAX_DEPTH_LIMIT-2 and totPieces < 22) or (self.max_depth == MAX_DEPTH_LIMIT-1 and totPieces < 16)):
                        self.max_depth += 1
                    elif(self.max_depth < MAX_DEPTH_LIMIT -2):
                        self.max_depth += 1
            elif (((time_per_move < self.time_budget * 0.005 or self.lastTime > 15)) and self.max_depth > self.initial_max_depth):
                # Si le temps par mouvement est inférieur au seuil, revenir à la profondeur initiale
                self.max_depth = self.max_depth-1
        # Autres ajustements basés sur la phase de jeu ou la complexité (facultatif)
        # Vous pouvez ajouter d'autres conditions pour ajuster la profondeur en fonction de certains critères

        print("mainDepth = ", self.max_depth)


    def is_cutoff(self, state, depth):
        """Determines if the search should be cut off at the current depth.

        Args:
            state (ShobuState): The current state of the game.
            depth (int): The current depth in the search tree.

        Returns:
            bool: True if the search should be cut off, False otherwise.
        """
        return (depth >= self.max_depth) or (self.game.is_terminal(state))

    def alpha_beta_search(self, state):
        global totalTimeSorting
        global totalTimeEvaluating
        """Implements the alpha-beta pruning algorithm to find the best action.

        Args:
            state (ShobuState): The current game state.

        Returns:
            ShobuAction: The best action as determined by the alpha-beta algorithm.
        """
        start = time.time()
        _, action = self.max_value(state, -float("inf"), float("inf"), 0)
        end = time.time()
        print("Total time elapsed to compute alpha beta search = ", end - start)
        print("Total time elapsed to sort = ", totalTimeSorting)
        #print("Total time evaluating = ", totalTimeEvaluating)
        #print("Time taken for agent: ", end - start)

        return action
    
    def compute_length(self,state):
        return [len(state.board[0][0]), len(state.board[0][1]), len(state.board[1][0]), len(state.board[1][1]), len(state.board[2][0]), len(state.board[2][1]), len(state.board[3][0]), len(state.board[3][1])]  

    def pushing_Test(self, move, longueurs, state):
        listPlayer = [element for i, element in enumerate(longueurs) if i % 2 == state.to_move]  # indices pairs
        listOpponent = [element for i, element in enumerate(longueurs) if i % 2 != state.to_move]  # indices impairs
        
        score = 0
        central_positions = [5, 6, 9, 10]
        totalPieces = sum(listPlayer)+sum(listOpponent)
        piecesOpponent = min(listOpponent)
        piecesPlayer = min(listPlayer)


        if(piecesOpponent == 1  and totalPieces < 18):
            attack = 10
        else :
            attack = 1

        if(piecesPlayer < 2):
            defense = 20
        else :
            defense = 1


        startOfGameWeight = 1
        if(totalPieces >30):
            startOfGameWeight = 10
        if move.active_stone_id + move.length*move.direction in central_positions:
            score+=startOfGameWeight
        if move.active_stone_id + move.length*move.direction in state.board[move.active_board_id][(state.to_move + 1) % 2]:
            new_opponent_active_stone = move.active_stone_id + (move.length+1) * move.direction
            if new_opponent_active_stone < 0 or new_opponent_active_stone > 15 or abs((move.active_stone_id + move.length * move.direction)%4 - (new_opponent_active_stone)%4) > 1:
                #score+=3
                listOpponent[move.active_board_id] -= 1
                score+= (defense*20*piecesPlayer - 1*attack*piecesPlayer - 4* sum(listOpponent)/attack)**3
                
        return score

    def order_moves_based_on_eval(self, state, isReverse):
        longueurs  = self.compute_length(state)
        myScores = np.array([self.pushing_Test(action,longueurs,state) for action in state.actions])

        indices_tries = np.argsort(myScores)
        if(isReverse == False):
           ordered_moves = [state.actions[i] for i in indices_tries]
        else:
            ordered_moves = [state.actions[i] for i in indices_tries[::-1]]

        return ordered_moves

    def shallow_eval(self, state):
        """Shallow evaluation function for move ordering."""
        # min_pieces_player = 4
        # min_pieces_opponent = 4
        # tot_pieces_player = 0
        # tot_pieces_opponent = 0 
        # for i in range(4):
        #     min_pieces_player = min(min_pieces_player, len(state.board[i][self.player]))
        #     min_pieces_opponent = min(min_pieces_opponent, len(state.board[i][(self.player + 1) % 2]))
        #     tot_pieces_player += len(state.board[i][self.player])
        #     tot_pieces_opponent += len(state.board[i][(self.player + 1) % 2])
        start = time.time()
        piecesPlayer, piecesOpponent, tot_pieces_player, tot_pieces_opponent = self.numberOfPiece(state)
        #piecesOpponentThreatened, totPiecesOpponentThreatened = self.PotentialAttacksToOpponent(state)
        #piecesPlayerThreatened, totPiecesPlayerThreatened = self.PotentialAttacksAgainstMe(state)
        #mobilityAdvantage = self.degreOfMobility(state)
        score = (3*( piecesPlayer - piecesOpponent) + (tot_pieces_player - tot_pieces_opponent))
        stop = time.time()
        global totalTimeEvaluating
        totalTimeEvaluating += stop - start
        #return ((piecesPlayer-piecesOpponent)+(piecesOpponentThreatened - piecesPlayerThreatened)+mobilityAdvantage)
        return score
        #return float(5*min_pieces_player - min_pieces_opponent)**3

    def max_value(self, state, alpha, beta, depth):
        global totalTimeSorting
        """Computes the maximum achievable value for the current player at a given state using the alpha-beta pruning.

        This method recursively explores all possible actions from the current state to find the one that maximizes
        the player's score, pruning branches that cannot possibly affect the final decision.

        Args:
            state (ShobuState): The current state of the game.
            alpha (float): The current alpha value, representing the minimum score that the maximizing player is assured of.
            beta (float): The current beta value, representing the maximum score that the minimizing player is assured of.
            depth (int): The current depth in the search tree.

        Returns:
            tuple: A tuple containing the best value achievable from this state and the action that leads to this value.
                If the state is a terminal state or the depth limit is reached, the action will be None.
        """
        if (self.is_cutoff(state, depth)) :
            return (self.eval_enhanced(state), None)
        
        best_value = -float("inf")
        best_action = None
        startTime = time.time()
        actions = self.order_moves_based_on_eval(state, True)
        endTime = time.time()
        
        totalTimeSorting += endTime - startTime
        for action in actions:  # Ordering moves based on evaluation
            value2, action2 = self.min_value(self.game.result(state, action), alpha, beta, depth + 1)
            if value2 > best_value:
                best_value, best_action = value2, action
                alpha = max(alpha, best_value)
            if best_value >= beta:
                return (best_value, best_action)
        return (best_value, best_action)
            
    def min_value(self, state, alpha, beta, depth):
        global totalTimeSorting
        """Computes the minimum achievable value for the opposing player at a given state using the alpha-beta pruning.

        Similar to max_value, this method recursively explores all possible actions from the current state to find
        the one that minimizes the opponent's score, again using alpha-beta pruning to cut off branches that won't
        affect the outcome.

        Args:
            state (ShobuState): The current state of the game.
            alpha (float): The current alpha value, representing the minimum score that the maximizing player is assured of.
            beta (float): The current beta value, representing the maximum score that the minimizing player is assured of.
            depth (int): The current depth in the search tree.

        Returns:
            tuple: A tuple containing the best value achievable from this state for the opponent and the action that leads to this value.
                If the state is a terminal state or the depth limit is reached, the action will be None.
        """
        if (self.is_cutoff(state, depth)) :
            return (self.eval_enhanced(state), None)
  
        best_value = float("inf")
        best_action = None
        startTime = time.time()
        actions = self.order_moves_based_on_eval(state, False)
        stopTime = time.time()
        totalTimeSorting += stopTime - startTime
        for action in actions:  # Ordering moves based on evaluation
            value2, action2 = self.max_value(self.game.result(state, action), alpha, beta, depth + 1)
            if value2 < best_value:
                best_value, best_action = value2, action
                beta = min(beta, best_value)
            if best_value <= alpha:
                return (best_value, best_action)
        return (best_value, best_action)

    def numberOfPiece (self, state):
        """The score returned is the difference between the minimal number of pieces of the player among all 
        the boards minus the minimal numberof pieces from the opponent among all the boards.
        The evaluation function should be relative to the player id and not to the current player.
        """
        min_pieces_player = 4
        min_pieces_opponent = 4
        tot_pieces_player = 0
        tot_pieces_opponent = 0

        for i in range(4):
            min_pieces_player = min(min_pieces_player, len(state.board[i][self.player]))
            tot_pieces_player += len(state.board[i][self.player])
            min_pieces_opponent = min(min_pieces_opponent, len(state.board[i][(self.player + 1) % 2]))
            tot_pieces_opponent += len(state.board[i][(self.player + 1) % 2])

        return min_pieces_player, min_pieces_opponent, tot_pieces_player, tot_pieces_opponent

    def degreOfMobility (self, state):
        """The score returned is the difference between the number of possible actions of the player minus the number of possible from the opponent.
        The evaluation function should be relative to the player id and not to the current player.
        """

        actions_player = len(self.game.compute_actions(state.board, self.player))
        actions_opponent = len(self.game.compute_actions(state.board, (self.player + 1) % 2))
        
        return (float) (actions_player - actions_opponent)
    
    def evaluate_board_control(self, state):
        """Evaluates the player's control over strategic board positions.
        """
        control_score = 0.0
        central_positions = [5, 6, 9, 10] # Central positions are more strategic
        for board_id in range(4):
            board = state.board[board_id]
            player_positions = board[self.player]
            control_score += sum(1 for pos in central_positions if pos in player_positions)
        return control_score

    def PotentialAttacksToOpponent (self, state):
        """The two scores returned are the number of possible attacks of the player that will eliminate or push the pieces of the opponent.
        The evaluation function should be relative to the player id and not to the current player.
        """

        board = state.board
        threatenedPiecesOpponent = [[] for i in range(4)]
        max_pieces_threatened = 0
        tot_pieces_threatened = 0

        for action in state.actions:
        
            passive_board_id, passive_stone_id, active_board_id, active_stone_id, direction, length = action
            player = self.player
            opponent = (self.player + 1) % 2
            opponent_active_stones = board[active_board_id][opponent]

            for l in range(1, length+1):
                if active_stone_id + l*direction in opponent_active_stones:
                    new_opponent_active_stone = active_stone_id + (length+1) * direction
                    if new_opponent_active_stone < 0 or new_opponent_active_stone > 15 or abs((active_stone_id + length * direction)%4 - (new_opponent_active_stone)%4) > 1:
                        threatenedPiecesOpponent[active_board_id].append(active_stone_id+l*direction)

        for i in range(4):
            max_pieces_threatened = max(max_pieces_threatened, len(threatenedPiecesOpponent[i]))
            tot_pieces_threatened += len(threatenedPiecesOpponent[i])
        
        return max_pieces_threatened, tot_pieces_threatened
    
    def PotentialAttacksAgainstMe (self, state):
        """The two scores returned are the number of possible attacks of the opponent that will eliminate or push the pieces of the player.
        The evaluation function should be relative to the player id and not to the current player.
        """

        board = state.board
        threatenedPiecesPlayer = [[] for i in range(4)]
        max_pieces_threatened = 0
        tot_pieces_threatened = 0

        player = self.player
        opponent = (self.player + 1) % 2

        actions = self.game.compute_actions(board, opponent)

        for action in actions:
        
            passive_board_id, passive_stone_id, active_board_id, active_stone_id, direction, length = action
            player_active_stones = board[active_board_id][player]


            for l in range(1, length+1):
                if active_stone_id + l*direction in player_active_stones:
                    new_player_active_stone = active_stone_id + (length+1) * direction
                    if new_player_active_stone < 0 or new_player_active_stone > 15 or abs((active_stone_id + length * direction)%4 - (new_player_active_stone)%4) > 1:
                        threatenedPiecesPlayer[active_board_id].append(active_stone_id+l*direction)

        for i in range(4):
            max_pieces_threatened = max(max_pieces_threatened, len(threatenedPiecesPlayer[i]))
            tot_pieces_threatened += len(threatenedPiecesPlayer[i])
        
        return max_pieces_threatened, tot_pieces_threatened

    def eval_enhanced_defense(self, state):
        board = state.board
        player = self.player
        opponent = (self.player + 1) % 2


        #Pieces Advantage
        min_pieces_player = 4

        #Opponent mobility
        actions = self.game.compute_actions(board, opponent)
        actions_opponent = len(actions)

        #Potential Attacks Against Me
        threatenedPiecesPlayer = [[] for i in range(4)]
        max_pieces_threatened = 0
        tot_pieces_threatened = 0

        for action in actions:
        
            passive_board_id, passive_stone_id, active_board_id, active_stone_id, direction, length = action
            player_active_stones = board[active_board_id][player]


            for l in range(1, length+1):
                if active_stone_id + l*direction in player_active_stones:
                    new_player_active_stone = active_stone_id + (length+1) * direction
                    if new_player_active_stone < 0 or new_player_active_stone > 15 or abs((active_stone_id + length * direction)%4 - (new_player_active_stone)%4) > 1:
                        threatenedPiecesPlayer[active_board_id].append(active_stone_id+l*direction)

        for i in range(4):
            #Pieces Advantage
            min_pieces_player = min(min_pieces_player, len(state.board[i][self.player]))

            #Potential Attacks Against Me
            max_pieces_threatened = max(max_pieces_threatened, len(threatenedPiecesPlayer[i]))
            tot_pieces_threatened += len(threatenedPiecesPlayer[i])
        
        return min_pieces_player, actions_opponent, max_pieces_threatened, tot_pieces_threatened

    def eval_enhanced_attack(self, state):
        
        board = state.board
        if(state.to_move == self.player):
            isPlayer = 1
        else:
            isPlayer = -1

        player = state.to_move
        opponent = (state.to_move + 1) % 2

        #Pieces Advantage
        totPiecesOpponent  = 0
        totPiecesPlayer = 0
        piecesOpponent = 4
        piecesPlayer = 4

        #Player mobility
        #actions = self.game.compute_actions(board, player)
        actions = state.actions
        actions_player = len(actions) * isPlayer

        #Board Control
        control_score = 0.0
        central_positions = [5, 6, 9, 10] # Central positions are more strategic

        #Potential Attacks To Opponent
        threatenedPiecesOpponent = [[] for i in range(4)]
        max_pieces_threatened = 0
        tot_pieces_threatened = 0

        for action in actions:
        
            passive_board_id, passive_stone_id, active_board_id, active_stone_id, direction, length = action
            opponent_active_stones = board[active_board_id][opponent]

            for l in range(1, length+1):
                if active_stone_id + l*direction in opponent_active_stones:
                    new_opponent_active_stone = active_stone_id + (length+1) * direction
                    if new_opponent_active_stone < 0 or new_opponent_active_stone > 15 or abs((active_stone_id + length * direction)%4 - (new_opponent_active_stone)%4) > 1:
                        threatenedPiecesOpponent[active_board_id].append(active_stone_id+l*direction)

        for i in range(4):
            #Pieces Advantage
            piecesOpponent = min(piecesOpponent, len(state.board[i][(player + 1) % 2]))
            piecesPlayer = min(piecesPlayer, len(state.board[i][player]))

            totPiecesOpponent += len(state.board[i][(player + 1) % 2])
            totPiecesPlayer += len(state.board[i][player])
            


            #Potential Attacks To Opponent

            max_pieces_threatened = max(max_pieces_threatened, len(threatenedPiecesOpponent[i])) * isPlayer
            tot_pieces_threatened += len(threatenedPiecesOpponent[i]) * isPlayer

            #Board Control
            player_positions = board[i][player]
            control_score += sum(1 for pos in central_positions if pos in player_positions)
            
        
        return piecesOpponent, piecesPlayer , actions_player, control_score, max_pieces_threatened, tot_pieces_threatened, totPiecesOpponent, totPiecesPlayer

    def eval_enhanced(self, state):
        pieces1, pieces2, actions_player, control_score, piecesOpponentThreatened, totPiecesOpponentThreatened, totPiecesOpponent, totPiecesPlayer = self.eval_enhanced_attack(state)
        #piecesPlayer, actions_opponent, piecesPlayerThreatened, totPiecesPlayerThreatened = self.eval_enhanced_defense(state)

        if(state.to_move == self.player):
            piecesPlayer = pieces2
            piecesOpponent = pieces1
        else:
            piecesPlayer = pieces1
            piecesOpponent = pieces2

        if(piecesOpponent == 1  and totPiecesOpponent+totPiecesPlayer < 20):
            attack = 20
        else :
            attack = 1

        if(piecesPlayer < 2):
            defense = 20
        else :
            defense = 1

        


        #return 20*defense*(5*piecesPlayer - piecesOpponent) + 0.05*(actions_player-actions_opponent) + 4*(totPiecesOpponentThreatened - defense*totPiecesPlayerThreatened) + 1*control_score + 0.1*(piecesOpponentThreatened - piecesPlayerThreatened)
        return (10*defense*piecesPlayer - 1*attack*piecesOpponent - 4*totPiecesOpponent/attack)**3 + 0.05*(actions_player) + 5*(totPiecesOpponentThreatened ) + 1*control_score + 0.5*(piecesOpponentThreatened)
        
    def eval(self, state):
        """Evaluates the given state and returns a score from the perspective of the agent's player.
        Args:
            state (ShobuState): The game state to evaluate.

        Returns:
            float: The evaluated score of the state.
        """

        piecesPlayer, piecesOpponent, tot_pieces_player, tot_pieces_opponent = self.numberOfPiece(state)
        mobilityAdvantage = self.degreOfMobility(state)
        control_score = self.evaluate_board_control(state)
        piecesOpponentThreatened, totPiecesOpponentThreatened = self.PotentialAttacksToOpponent(state)
        piecesPlayerThreatened, totPiecesPlayerThreatened = self.PotentialAttacksAgainstMe(state)
        #return 10*(5*piecesPlayer - piecesOpponent) + 0.01*mobilityAdvantage + 2*(totPiecesOpponentThreatened - 12*totPiecesPlayerThreatened) + 0.5*control_score CA FONCTIONNE ICIIIIII
        if(piecesOpponent == 1):
            if(piecesPlayer > 1):
                attack = 10
            else:
                attack = 3
                
        elif (piecesOpponent == 2):
            if(piecesPlayer > 2):
                attack = 5
            else:
                attack = 2
        else :
            attack = 1

        if(piecesPlayer < 3):
            defense = 5
        else :
            defense = 1


        return 20*defense*(5*piecesPlayer - piecesOpponent) + 0.05*mobilityAdvantage + 4*(totPiecesOpponentThreatened - defense*totPiecesPlayerThreatened) + 1*control_score + 0.1*(piecesOpponentThreatened - piecesOpponentThreatened)
        #return 20*attack*(tot_pieces_player*piecesPlayer - tot_pieces_opponent*piecesOpponent) + 4*(tot_pieces_player*totPiecesOpponentThreatened - tot_pieces_opponent*totPiecesPlayerThreatened) + 0.05*mobilityAdvantage
  