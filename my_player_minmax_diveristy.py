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
        self.depth_max = 2


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
        isMax = current_state.step%2 == 0
        self.depth_max = self.pick_depth_max(isMax)
        possible_actions_light = list(possible_actions_light)
        self.opponent_id = self.get_opponent_id(current_state)
        return self.minimaxSearch(current_state, isMax) #to see if useful
        best_action = next(possible_actions)
        ### TODO essayer de juste le faire une fois et pas à chaque coup!
        opponent_id = self.get_opponent_id()
        ### TODO END


    def minimaxSearch(self, state: GameState, isMax:bool): #player: MyPlayer,
        # self.counter = 0
        if isMax: v, m = self.maxValue(state, 0)
        else: v, m = self.minValue(state, 0)
        return m # return v, m


    def maxValue(self, state: GameState, counter:int):
        if self.isTerminal(counter):
            return  state.scores[self.get_id()] - state.scores[self.opponent_id], None
        
        v_star = -1000000
        m_star = None

        for action in self.getPossibleActions(state):
            temporary_state = self.transition(action)
            # self.counter += 1
            counter += 1
            v, _ = self.minValue(temporary_state, counter)
            if  v > v_star:
                v_star = v
                m_star = action
            counter -= 1
        return v_star, m_star

    def minValue(self, state: GameState, counter):
        if self.isTerminal(counter):
            # the best score is reversed because we are the opponent
            return  state.scores[self.opponent_id]- state.scores[self.id], None
        
        v_star = 1000000
        m_star = None
        for action in self.getPossibleActions(state):
            temporary_state = self.transition(action)
            # self.counter += 1
            counter +=1
            v, _ = self.maxValue(temporary_state, counter)
            if  v < v_star:
                v_star = v
                m_star = action
            counter -=1
        return v_star, m_star
        
    def isTerminal(self, counter):
        return self.depth_max == counter #self.counter

    def getPossibleActions(self, state: GameState):
        # J'ai mis un fonction dans une fonction, car 
        # si jamais on veut changer pour light action
        # on aura qu'à changer le return 
        return state.generate_possible_heavy_actions()

    def transition(self, action: Action):
        
        return action.get_next_game_state()
    
    def get_opponent_id(self, current_state:GameState):
        opponent_id = 0
        for players in current_state.players:
            if players.get_id() != self.get_id():
                opponent_id = players.get_id()
        return opponent_id
    
    def pick_depth_max(self, isMax:bool):
        return 2
    

############### Divercity part ################



    def get_player_cities(self, current_state: GameStateDivercite, player_id: int):
            board = current_state.get_rep().get_env()
            return [(i, j) for (i, j), piece in board.items() if isinstance(piece, Piece) and piece.get_type()[1] == 'C' and piece.get_owner_id() == player_id]
    
    def get_all_possible_divercities(self, current_state: GameStateDivercite, player_id: int):
        player_cities = self.get_player_cities(current_state, player_id)
        all_possible_divercities = []

        for x, y in player_cities:
            if current_state.check_divercite([x, y]):
                continue
            
            neighbours = current_state.get_neighbours(x, y)
            neighbor_colors_count = {"R": 0, "G": 0, "B": 0, "Y": 0}

            for _, (piece, _) in neighbours.items():
                if isinstance(piece, Piece):
                    neighbor_colors_count[piece.get_type()[0]] += 1

            if any(count > 1 for count in neighbor_colors_count.values()):
                continue

            ressource_missings = [color + 'R' for color, count in neighbor_colors_count.items() if count == 0]
            all_possible_divercities.append(((x, y), ressource_missings))

        return all_possible_divercities
    
    def do_divercity(self, current_state: GameStateDivercite, player_id: int, all_possible_divercities: List[Tuple[Tuple[int, int], int]]):
        remaining_pieces = current_state.players_pieces_left.get(player_id, {})

        for (x, y), ressource_missings in all_possible_divercities:
            neighbours = current_state.get_neighbours(x, y)

            for direction, (piece, (nx, ny)) in neighbours.items():
                if piece == 'EMPTY':
                    valid_pieces = [p for p in remaining_pieces if p in ressource_missings and remaining_pieces[p] > 0]

                    if valid_pieces:
                        chosen_piece = random.choice(valid_pieces)
                        action_data = {
                            'player_id': player_id,
                            'piece': chosen_piece,
                            'position': (nx, ny)
                        }
                        return LightAction(action_data)

        return None
    
    def prevent_opponent_divercity(self, current_state: GameStateDivercite, my_player_id: int):
        opponent_id = self.get_opponent_id(current_state)
        my_remaining_pieces = current_state.players_pieces_left.get(my_player_id, {})
        ordered_opponents_all_possible_divercities = sorted(self.get_all_possible_divercities(current_state, opponent_id), key=lambda x: len(x[1]))
        for (x, y), ressource_missings in ordered_opponents_all_possible_divercities:
            neighbours = current_state.get_neighbours(x, y)

            for direction, (piece, (nx, ny)) in neighbours.items():
                if piece == 'EMPTY':
                    valid_pieces_destroy_opponent_divercity = [p for p in my_remaining_pieces if p not in ressource_missings and my_remaining_pieces[p] > 0 and p[1] == 'R']
                    if valid_pieces_destroy_opponent_divercity:
                        chosen_piece = random.choice(valid_pieces_destroy_opponent_divercity)
                        action_data = {
                            'player_id': my_player_id,
                            'piece': chosen_piece,
                            'position': (nx, ny)
                        }
                        return LightAction(action_data)