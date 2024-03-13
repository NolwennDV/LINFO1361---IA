from agent import Agent

class AlphaBetaAgent(Agent):
    """An agent that uses the alpha-beta pruning algorithm to determine the best move.

    This agent extends the base Agent class, providing an implementation of the play
    method that utilizes the alpha-beta pruning technique to make decisions more efficiently.

    Attributes:
        max_depth (int): The maximum depth the search algorithm will explore.
    """

    def __init__(self, player, game, max_depth):
        """Initializes an AlphaBetaAgent instance with a specified player, game, and maximum search depth.

        Args:
            player (int): The player ID this agent represents (0 or 1).
            game (ShobuGame): The Shobu game instance the agent will play on.
            max_depth (int): The maximum depth of the search tree.
        """
        super().__init__(player, game)
        self.max_depth = max_depth

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
        return depth >= self.max_depth or self.game.is_terminal(state)

    
    def eval(self, state):
        """Evaluates the given state and returns a score from the perspective of the agent's player.
        Reminder : the score of the state is the difference between the minimal number of pieces of the player among all 
        the boards minus the minimal numberof pieces from the opponent among all the boards.
        Remember that the evaluation function should be relative to the player id and not to the current player.

        Args:
            state (ShobuState): The game state to evaluate.

        Returns:
            float: The evaluated score of the state.
        """
        min_pieces_player = 4
        min_pieces_opponent = 4

        for i in range(4):
            min_pieces_player = min(min_pieces_player, len(state.boards[i][self.player]))
            min_pieces_opponent = min(min_pieces_opponent, len(state.boards[i][(self.player + 1) % 2]))

        return min_pieces_player - min_pieces_opponent

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
        if (self.is_cutoff(state)) :
            return (self.eval(state), None)
        
        best_value = -float("inf")
        
        for action in self.actions(state):
            value2, action2 = self.min_value(self.result(state, action), alpha, beta, depth + 1)
            if value > best_value:
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

        for action in state.actions():
            value2, action2 = self.max_value(self.result(state, action), alpha, beta, depth + 1)
            if value2 < best_value:
                best_value, best_action = value2, action
                beta = min(beta, best_value)
            if best_value <= alpha:
                return (best_value, best_action)
        return (best_value, best_action)