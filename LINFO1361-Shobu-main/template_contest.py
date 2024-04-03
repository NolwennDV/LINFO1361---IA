from agent import Agent
import random

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
        self.max_depth = 2

    def play(self, state, remaining_time):
        """Determines the best action by applying the alpha-beta pruning algorithm.

        Overrides the play method in the base class.

        Args:
            state (ShobuState): The current state of the game.
            remaining_time (float): The remaining time in seconds that the agent has to make a decision.

        Returns:
            ShobuAction: The action determined to be the best by the alpha-beta algorithm.
        """
        return self.alpha_beta_search(state)
    
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
        """Implements the alpha-beta pruning algorithm to find the best action.

        Args:
            state (ShobuState): The current game state.

        Returns:
            ShobuAction: The best action as determined by the alpha-beta algorithm.
        """
        _, action = self.max_value(state, -float("inf"), float("inf"), 0)
        return action

    def max_value(self, state, alpha, beta, depth):
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
            return (self.eval(state), None)
        
        best_value = -float("inf")
        
        for action in state.actions :
            value2, action2 = self.min_value(self.game.result(state, action), alpha, beta, depth + 1)
            if value2 > best_value:
                best_value, best_action = value2, action
                alpha = max(alpha, best_value)
            if best_value >= beta:
                return (best_value, best_action)
        return (best_value, best_action)
    


    def min_value(self, state, alpha, beta, depth):
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
            return (self.eval(state), None)
  
        best_value = float("inf")

        for action in state.actions :
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

        for i in range(4):
            min_pieces_player = min(min_pieces_player, len(state.board[i][self.player]))
            min_pieces_opponent = min(min_pieces_opponent, len(state.board[i][(self.player + 1) % 2]))

        return min_pieces_player, min_pieces_opponent

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
        # Central positions are more strategic
        central_positions = [5, 6, 9, 10]
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
        elimitingAttacks = 0
        pushingAttacks = 0
        threatenedPiecesOpponent = [[] for i in range(4)]
        max_pieces_threatened = 0
        tot_pieces_threatened = 0

        for action in state.actions:
        
            passive_board_id, passive_stone_id, active_board_id, active_stone_id, direction, length = action
            player = self.player
            opponent = (self.player + 1) % 2
            opponent_active_stones = board[active_board_id][opponent]

            pushing = False
            opponent_active_stone = -1
            for l in range(1, length+1):
                if active_stone_id + l*direction in opponent_active_stones:
                    pushing = True
                    pushingAttacks += 1
                    break

            if pushing:
                new_opponent_active_stone = active_stone_id + (length+1) * direction
                if new_opponent_active_stone < 0 or new_opponent_active_stone > 15 or abs((active_stone_id + length * direction)%4 - (new_opponent_active_stone)%4) > 1:
                    elimitingAttacks += 1
                    pushingAttacks -= 1
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
        elimitingAttacks = 0
        pushingAttacks = 0
        threatenedPiecesPlayer = [[] for i in range(4)]
        max_pieces_threatened = 0
        tot_pieces_threatened = 0

        player = self.player
        opponent = (self.player + 1) % 2

        actions = self.game.compute_actions(board, opponent)

        for action in actions:
        
            passive_board_id, passive_stone_id, active_board_id, active_stone_id, direction, length = action
            
            player_active_stones = board[active_board_id][player]

            pushing = False
            player_active_stone = -1
            for l in range(1, length+1):
                if active_stone_id + l*direction in player_active_stones:
                    pushing = True
                    pushingAttacks += 1
                    break

            if pushing:
                new_player_active_stone = active_stone_id + (length+1) * direction
                if new_player_active_stone < 0 or new_player_active_stone > 15 or abs((active_stone_id + length * direction)%4 - (new_player_active_stone)%4) > 1:
                    elimitingAttacks += 1
                    pushingAttacks -= 1
                    threatenedPiecesPlayer[active_board_id].append(active_stone_id+l*direction)

        for i in range(4):
            max_pieces_threatened = max(max_pieces_threatened, len(threatenedPiecesPlayer[i]))
            tot_pieces_threatened += len(threatenedPiecesPlayer[i])
        
        return max_pieces_threatened, tot_pieces_threatened

    def eval(self, state):
        """Evaluates the given state and returns a score from the perspective of the agent's player.
        Args:
            state (ShobuState): The game state to evaluate.

        Returns:
            float: The evaluated score of the state.
        """

        piecesPlayer, piecesOpponent = self.numberOfPiece(state)
        mobilityAdvantage = self.degreOfMobility(state)
        control_score = self.evaluate_board_control(state)
        piecesOpponentThreatened, totPiecesOpponentThreatened = self.PotentialAttacksToOpponent(state)
        piecesPlayerThreatened, totPiecesPlayerThreatened = self.PotentialAttacksAgainstMe(state)

        # Attack and defense adaptive weights : they will take into account the number of pieces of the player threatened by the opponent 
        # and the number of pieces of the opponent threatened by the player

        defenseTactic = totPiecesPlayerThreatened
        attackTactic = totPiecesOpponentThreatened

        return 10*(piecesPlayer - piecesOpponent) + 0.5*mobilityAdvantage + 2*(totPiecesOpponentThreatened) + 1.5*control_score

    