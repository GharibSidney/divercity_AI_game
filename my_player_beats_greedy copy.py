from player_divercite import PlayerDivercite
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from game_state_divercite import GameStateDivercite
from seahorse.utils.custom_exceptions import MethodNotImplementedError
import random
import math

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

        #TODO
        # possible_actions = current_state.get_possible_light_actions()
        # # print('possible action', list(possible_actions))
        # return random.choice(list(possible_actions))

        possible_actions = current_state.generate_possible_heavy_actions()
        possible_actions_light = current_state.get_possible_light_actions()
        possible_actions_light = list(possible_actions_light)

        best_action = next(possible_actions)
        ### TODO essayer de juste le faire une fois et pas à chaque coup!
        opponent_id = 0
        for players in current_state.players:
            if players.get_id() != self.get_id():
                opponent_id = players.get_id()
        ### TODO END

        best_score = best_action.get_next_game_state().scores[self.get_id()] - best_action.get_next_game_state().scores[opponent_id]

        if len(possible_actions_light) == 164:
            for action in possible_actions_light:
                print(action.data)
            return possible_actions_light[16]
        
        self.counter += 1
        
        i = 0
        best_action_data = possible_actions_light[0].data

        for action in possible_actions:
            if self.counter == 3 or self.counter == 4:
                print('possible action', possible_actions_light[i].data)

            state = action.get_next_game_state()
            score = state.get_scores().get(self.get_id()) - state.get_scores().get(opponent_id)
            if score > best_score:

                best_action = action
                best_score = score
                best_action_data = possible_actions_light[i].data
            i += 1

        if self.counter == 3 or self.counter == 4:
            print('\n best action ', best_action_data)
            print('\n best_score ', best_score)

        return best_action
        

    def minMax():
        MethodNotImplementedError()


 
