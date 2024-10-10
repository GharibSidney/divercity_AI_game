from player_divercite import PlayerDivercite
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from game_state_divercite import GameStateDivercite
from seahorse.utils.custom_exceptions import MethodNotImplementedError
from minimaxSearch import minimaxSearch

class MyPlayer(PlayerDivercite):
    """
    Player class for Divercite game that makes random moves.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "MyPlayer"):
        """
        Initialize the PlayerDivercite instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name)
        
        # self.isFirstPlayer = isFistPlayer
        print('get init')
        self.isFirstMove = True
        self.counter = 0
        


    def compute_action(self, current_state: GameState, remaining_time: int = 1e9, **kwargs) -> Action:
        """
        Use the minimax algorithm to choose the best action based on the heuristic evaluation of game states.

        Args:
            current_state (GameState): The current game state.

        Returns:
            Action: The best action as determined by minimax.
        """
        #TODO try to initialize the minimaxSearch only once
        self.minimaxSearch = minimaxSearch(self, current_state)
        possible_actions = current_state.generate_possible_heavy_actions()
        possible_actions_light = current_state.get_possible_light_actions()
        possible_actions_light = list(possible_actions_light)
        return self.minimaxSearch.minimaxSearch(current_state, True) #to see if useful
        best_action = next(possible_actions)
        ### TODO essayer de juste le faire une fois et pas à chaque coup!
        opponent_id = self.get_opponent_id()
        ### TODO END
