from typing import List, Tuple
from player_divercite import PlayerDivercite
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from game_state_divercite import GameStateDivercite
from seahorse.utils.custom_exceptions import MethodNotImplementedError
from seahorse.game.game_layout.board import Board, Piece
import random
import math
from seahorse.game.light_action import LightAction

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
        possible_actions = current_state.generate_possible_heavy_actions()
        possible_actions_light = current_state.get_possible_light_actions()
        possible_actions_light = list(possible_actions_light)


        player_cities = self.get_player_cities(current_state, self.get_id())
        print(f"voici les villes de player {self.get_name()} AVANT LE COUP (ca match avec ce qui ya en haut du separateur):")
        print(player_cities)


        allPossibleDivercities = self.allPossibleDivercities(current_state, self.get_id())
        print(f"voici les divercities possibles de player {self.get_name()} AVANT LE COUP (ca match avec ce qui ya en haut du separateur):")
        print(allPossibleDivercities)

        divercity_action = self.doDivercity(current_state, self.get_id(), allPossibleDivercities)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

        best_action = next(possible_actions)
        return divercity_action if divercity_action is not None else best_action
        

    def minMax():
        MethodNotImplementedError()


    def get_player_cities(self, current_state: GameStateDivercite, player_id: int):
        player_cities = []
        board = current_state.get_rep()
        dimensions = board.get_dimensions()

        for i in range(dimensions[0]):
            for j in range(dimensions[1]):
                piece = board.get_env().get((i, j))
                if piece and isinstance(piece, Piece):
                    if piece.get_type()[1] == 'C' and piece.get_owner_id() == player_id:
                        player_cities.append((i, j))
        
        return player_cities
    
    def allPossibleDivercities(self, current_state: GameStateDivercite, player_id: int):
        player_cities = self.get_player_cities(current_state, player_id)
        all_possible_divercities = []
        
        for city in player_cities:
            x, y = city
            coords = [x,y]
            if current_state.check_divercite(coords):
                continue
                #HERE


            neighbours = current_state.get_neighbours(x, y)

            neighbor_colors_count = {"R": 0, "G": 0, "B": 0, "Y": 0}

            for direction, (piece, (nx, ny)) in neighbours.items():
                if isinstance(piece, Piece):
                    piece_color = piece.get_type()[0]
                    neighbor_colors_count[piece_color] += 1
            
            repeated_colors = False
            for key in neighbor_colors_count:
                if neighbor_colors_count[key] > 1:
                    repeated_colors = True
                    break
            
            if not repeated_colors:
                # ressource_missing = 4 - sum(neighbor_colors_count.values())
                ressource_missings = [key + 'R' for key, value in neighbor_colors_count.items() if value == 0]
                all_possible_divercities.append((city, ressource_missings))

        return all_possible_divercities
    
    def doDivercity(self, current_state: GameStateDivercite, player_id: int, all_possible_divercities: List[Tuple[Tuple[int, int], int]]):
        remaining_pieces = current_state.players_pieces_left.get(player_id, {})
        for coordinates, ressource_missings in all_possible_divercities:
            x, y = coordinates
            neighbours = current_state.get_neighbours(x, y)
            for direction, (piece, (nx, ny)) in neighbours.items():
                if piece == 'EMPTY':
                    chosen_piece = random.choice([piece for piece in remaining_pieces if piece in ressource_missings and remaining_pieces[piece] > 0])
                    action_data = {
                        'player_id': player_id,
                        'piece': chosen_piece,
                        'position': (nx, ny)
                    }
                    print(LightAction(action_data))
                    return LightAction(action_data)
        return None
            










 
