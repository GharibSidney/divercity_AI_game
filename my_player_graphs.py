from player_divercite import PlayerDivercite
from typing import List, Tuple
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from game_state_divercite import GameStateDivercite
from seahorse.utils.custom_exceptions import MethodNotImplementedError
from seahorse.game.light_action import LightAction
from seahorse.game.game_layout.board import Board, Piece
from collections import OrderedDict
import random
import time

TABLE_MAX_SIZE = 30000000 # 30 million entries to use the 4GB of RAM with small risk to overflow. Max is 51 million entries

class MyPlayer(PlayerDivercite):
    """
    Player class for Divercite game that makes random moves.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "MyPlayer", use_transposition_table: bool = True):
        """
        Initialize the PlayerDivercite instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name)
        self.use_transposition_table = use_transposition_table
        self.time_per_turn = []
        self.depth_dict = {}

        self.board = [
            [ 0,   0,   0,   0,  'R',  0,   0,   0,   0],
            [ 0,   0,   0,  'R', 'C', 'R',  0,   0,   0],
            [ 0,   0,  'R', 'C', 'R', 'C', 'R',  0,   0],
            [ 0,  'R', 'C', 'R', 'C', 'R', 'C', 'R',  0],
            ['R', 'C', 'R', 'C', 'R', 'C', 'R', 'C', 'R'],
            [ 0,  'R', 'C', 'R', 'C', 'R', 'C', 'R',  0],
            [ 0,   0,  'R', 'C', 'R', 'C', 'R',  0,   0],
            [ 0,   0,   0,  'R', 'C', 'R',  0,   0,   0],
            [ 0,   0,   0,   0,  'R',  0,   0,   0,   0]
        ]

        # Key is the hash of a particular state, value is the tuple (v,m) obtained from evaluation function
        self.transposition_table = self.LimitedSizeTable(maxsize=TABLE_MAX_SIZE)

    class LimitedSizeTable(OrderedDict):
        def __init__(self, maxsize: int, *args, **kwargs):
            self.maxsize = maxsize
            super().__init__(*args, **kwargs)

        def __setitem__(self, key, value):
            if len(self) >= self.maxsize:
                self.popitem(last = False)
            super().__setitem__(key, value)

    def compute_action(self, current_state: GameState, remaining_time: int = 1e9, **kwargs) -> Action:
        """
        Use the minimax algorithm to choose the best action based on the heuristic evaluation of game states.

        Args:
            current_state (GameState): The current game state.

        Returns:
            Action: The best action as determined by minimax.
        """
        # start_time = time.time()

        isMax = current_state.step%2 == 0

        self.depth_max = self.pick_depth_max(current_state, remaining_time)
        self.opponent_id = self.get_opponent_id(current_state)
        action = self.minimaxSearch(current_state, isMax)
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # self.time_per_turn.append(elapsed_time)
        # print(f"Temps d'exécution pour ce tour : {elapsed_time:.4f} secondes")
        self.depth_dict[current_state.step] = self.depth_max
        return action 

################ Minmax part ################

    def minimaxSearch(self, state: GameState, isMax:bool):
        # if isMax: v, m = self.maxValue(state, 0)
        # else: v, m = self.minValue(state, 0)
        v, m = self.maxValue(state, None, 0)
        return m # return v, m


    def maxValue(self, state: GameState, main_action:LightAction, counter:int, alpha = -1000000, beta = 1000000):
        # We use transposition table to avoid redundant calculations here
        state_hash = None
        if self.use_transposition_table:
            state_hash = self.hash_state(state)
            if state_hash in self.transposition_table:
                #We return the already calculated value of that state from the transposition table
                return self.transposition_table[state_hash]

        if self.isTerminal(counter):
            result = self.evaluation(state, main_action, state.scores[self.get_id()] - state.scores[self.opponent_id]), None #, all_actions_divercity
            if self.use_transposition_table:
                # We store the result in the transposition table
                self.transposition_table[state_hash] = result
            return result
        
        v_star = -1000000
        m_star = None

        for action in self.getPossibleActions(state):
            temporary_state = self.transition(action, state)
            counter += 1
            v, _ = self.minValue(temporary_state, action, counter, alpha, beta)
            if  v > v_star:
                v_star = v
                m_star = action
                alpha = max(v_star, alpha)
            if alpha >= beta:
                return v_star, m_star
            counter -= 1
        
        if self.use_transposition_table:
            # It was not an already calculated state, so we store the result in the transposition table
            self.transposition_table[state_hash] = (v_star, m_star)
        return v_star, m_star


    def minValue(self, state: GameState, main_action:LightAction, counter: int, alpha = -1000000, beta = 1000000):
        # We use transposition table to avoid redundant calculations here
        state_hash = None
        if self.use_transposition_table:   
            state_hash = self.hash_state(state)
            if state_hash in self.transposition_table:
                return self.transposition_table[state_hash]

        if self.isTerminal(counter):
            result = self.evaluation(state, main_action, state.scores[self.get_id()] - state.scores[self.opponent_id]), None #, all_actions_divercity
            if self.use_transposition_table:
                # We store the result in the transposition table
                self.transposition_table[state_hash] = result
            return result
        
        v_star = 1000000
        m_star = None
        for action in self.getPossibleActions(state):
            temporary_state = self.transition(action, state)
            counter += 1
            v, _ = self.maxValue(temporary_state, action, counter)
            if  v < v_star:
                v_star = v
                m_star = action
                beta = min(v_star, beta)
            counter -= 1
            if v_star <= alpha:
                return v_star, m_star
                    
        if self.use_transposition_table:
            # It was not an already calculated state, so we store the result in the transposition table
            self.transposition_table[state_hash] = (v_star, m_star)
        return v_star, m_star
        
    def isTerminal(self, counter):
        return self.depth_max == counter #self.counter

    def getPossibleActions(self, state: GameState):
        # J'ai mis un fonction dans une fonction, car 
        # si jamais on veut changer pour light action
        # on aura qu'à changer le return 
        return state.generate_possible_light_actions()

    def transition(self, action: Action, state: GameState):
        
        return action.get_heavy_action(state).get_next_game_state()
    
    def get_opponent_id(self, current_state:GameState):
        opponent_id = 0
        for players in current_state.players:
            if players.get_id() != self.get_id():
                opponent_id = players.get_id()
        return opponent_id
    
    def pick_depth_max(self, current_state:GameState, remaining_time:int):
        if remaining_time < 20:
            return 2
        if current_state.step < 28:
            return 2
        elif current_state.step < 31: 
            return 4
        # if current_state.step < 28:
        #     return 3
        # elif current_state.step < 30:
        #     return  4 #40 - current_state.step
        # elif current_state.step < 34:
        #     return  5
        else:
           return 40 - current_state.step
    

################ Divercity part ################
    def get_player_cities(self, current_state: GameStateDivercite, player_id: int):
            board = current_state.get_rep().get_env()
            return [(i, j) for (i, j), piece in board.items() if isinstance(piece, Piece) and piece.get_type()[1] == 'C' and piece.get_owner_id() == player_id]
    
    def get_player_cities_with_piece(self, current_state: GameStateDivercite, player_id: int):
        board = current_state.get_rep().get_env()
        return [[(i, j), piece] for (i, j), piece in board.items() if isinstance(piece, Piece) and piece.get_type()[1] == 'C' and piece.get_owner_id() == player_id]
    
    def get_all_possible_divercities(self, current_state: GameStateDivercite, player_id: int):
        player_cities = self.get_player_cities_with_piece(current_state, player_id)
        all_possible_divercities = []

        for (x, y), city_piece in player_cities:
            if current_state.check_divercite([x, y]):
                continue
            
            neighbours = current_state.get_neighbours(x, y)
            neighbor_colors_count = {"R": 0, "G": 0, "B": 0, "Y": 0}

            for _, (piece, _) in neighbours.items():
                if isinstance(piece, Piece):
                    neighbor_colors_count[piece.get_type()[0]] += 1

            if any(count > 1 for count in neighbor_colors_count.values()):
                continue

            resources_missing = [color + 'R' for color, count in neighbor_colors_count.items() if count == 0]
            all_possible_divercities.append(((x, y), resources_missing, city_piece))
            
        return all_possible_divercities
    
    def do_divercity(self, current_state: GameStateDivercite, player_id: int, all_possible_divercities: List[Tuple[Tuple[int, int], int, any]]):
        remaining_pieces = current_state.players_pieces_left.get(player_id, {})

        for (x, y), resources_missing, _ in all_possible_divercities:
            neighbours = current_state.get_neighbours(x, y)

            for direction, (piece, (nx, ny)) in neighbours.items():
                if piece == 'EMPTY':
                    valid_pieces = [p for p in remaining_pieces if p in resources_missing and remaining_pieces[p] > 0]

                    if valid_pieces:
                        chosen_piece = self.chose_most_available_resource(current_state, valid_pieces)
                        if chosen_piece is None:
                            chosen_piece = random.choice(valid_pieces)
                        action_data = {
                            'player_id': player_id,
                            'piece': chosen_piece,
                            'position': (nx, ny)
                        }
                        return LightAction(action_data)

        return None
    
    def all_action_divercity(self, current_state: GameStateDivercite, player_id: int, all_possible_divercities: List[Tuple[Tuple[int, int], int, any]]):
        remaining_pieces = current_state.players_pieces_left.get(player_id, {})
        all_actions_divercity = []

        for (x, y), resources_missing, _ in all_possible_divercities:
            neighbours = current_state.get_neighbours(x, y)

            for direction, (piece, (nx, ny)) in neighbours.items():
                if piece == 'EMPTY':
                    valid_pieces = [p for p in remaining_pieces if p in resources_missing and remaining_pieces[p] > 0]

                    if valid_pieces:
                        chosen_piece = self.chose_most_available_resource(current_state, valid_pieces)
                        if chosen_piece is None:
                            chosen_piece = random.choice(valid_pieces)
                        action_data = {
                            'player_id': player_id,
                            'piece': chosen_piece,
                            'position': (nx, ny)
                        }
                        all_actions_divercity.append(LightAction(action_data))
                        # return LightAction(action_data)

        return all_actions_divercity
    
    def prevent_opponent_divercity(self, current_state: GameStateDivercite, my_player_id: int):
        opponent_id = self.get_opponent_id(current_state)
        my_remaining_pieces = current_state.players_pieces_left.get(my_player_id, {})
        ordered_opponents_all_possible_divercities = self.get_all_possible_divercities(current_state, opponent_id) #sorted(self.get_all_possible_divercities(current_state, opponent_id), key=lambda x: len(x[1]))
        single_resource_left_divercities = [divercity for divercity in ordered_opponents_all_possible_divercities if len(divercity[1]) == 1]
        # I only need to prevent the opponent from getting a divercity when a single resource missing
        for (x, y), resources_missing, city_piece in single_resource_left_divercities:

            neighbours = current_state.get_neighbours(x, y)

            for direction, (piece, (nx, ny)) in neighbours.items():
                if piece == 'EMPTY':
                    valid_pieces_destroy_opponent_divercity = [p for p in my_remaining_pieces if p not in resources_missing and my_remaining_pieces[p] > 0 and p[1] == 'R']
                    if valid_pieces_destroy_opponent_divercity:
                        chosen_piece = self.choose_most_available_resource_and_no_points(current_state, valid_pieces_destroy_opponent_divercity, city_piece)
                        if chosen_piece is None:
                            chosen_piece = random.choice(valid_pieces_destroy_opponent_divercity)
                        action_data = {
                            'player_id': my_player_id,
                            'piece': chosen_piece,
                            'position': (nx, ny)
                        }
                        return LightAction(action_data)
        return None
                    
    def sort_divercity(self, divercities: List[Tuple[Tuple[int, int], int]]) -> List[Tuple[Tuple[int, int], int]]:
        # Sort by the number of missing resources (ascending)
        return sorted(divercities, key=lambda x: x[1])


################ Heuristic part ################

    def evaluation(self, state:GameStateDivercite, action: LightAction, score:int, ) -> int:
        # city_score = -100000 * self.is_city_placement(action)
        min_available_resource = 3*self.get_minimum_unique_resource(state)
        potential_divercities = 2* self.get_one_ressource_divercity( state, self.get_id())
        my_divercities = self.get_amount_divercity(state, self.get_id())
        block_score = 2*self.get_block_opponent_divercity_potential(state)
        heuristic = 1.5*self.heuristic(state)
        eval = score + min_available_resource + potential_divercities + my_divercities + block_score #heuristic + 

        return eval

    def is_city_placement(self, action: LightAction):
        # if city then return True else False
        if (action.data['piece'][1] == 'C'):
            return 1
        return 0
    
    def max_available_resource(self, state:GameStateDivercite, action: LightAction):
        if action.data['piece'][1] == 'R':
            remaining_pieces = state.players_pieces_left.get(self.get_id(), {})
            for resource in remaining_pieces:
                # if the resource is the same as the action piece
                if action.data['piece'][:2] == resource:
                    # return the number of remaining pieces for that resource
                    return remaining_pieces[resource]
        else:
            return 0
        
    def is_divercity(self, all_actions_divercity: List[LightAction], action: LightAction):
        # if the action is a divercity then return True else False
        if action in all_actions_divercity:
            return 1
        return 0
    
    def get_minimum_unique_resource(self, current_state: GameStateDivercite):
        # Counting the number of unique resources left for the player
        my_remaining_pieces =  current_state.players_pieces_left.get(self.get_id(), {})
        minimum_amount_left = 3
        for resource in my_remaining_pieces:
            if resource[0] == 'R' and my_remaining_pieces[resource] < minimum_amount_left:
                minimum_amount_left = my_remaining_pieces[resource]
        return minimum_amount_left
    

    
    def get_amount_divercity(self, state: GameStateDivercite, player_id: int):
        # Counting the number of divercities left for the player
        player_cities = self.get_player_cities(state, player_id)
        divercities = 0
        for (x, y) in player_cities:
            if not state.check_divercite([x, y]):
                divercities += 1
        return divercities
    
    def get_one_ressource_divercity(self, state: GameStateDivercite, player_id: int):
        # Counting the number of divercities left for the player with only one resource missing
        player_cities = self.get_player_cities_with_piece(state, player_id)
        number_of_divercities = 0
        for (x, y), city_piece in player_cities:
            if not state.check_divercite([x, y]):
                neighbours = state.get_neighbours(x, y)
                neighbor_colors_count = {"R": 0, "G": 0, "B": 0, "Y": 0}
                for _, (piece, _) in neighbours.items():
                    if isinstance(piece, Piece):
                        neighbor_colors_count[piece.get_type()[0]] += 1
                if any(count > 1 for count in neighbor_colors_count.values()):
                    continue
                if len([color for color, count in neighbor_colors_count.items() if count == 0]) == 1:
                    number_of_divercities += 1
        return number_of_divercities
    

    def heuristic(self, state: GameState) -> float:
        """
        Calculate the heuristic score for a given game state based on the current player's cities.
        
        Args:
            state (GameState): The current state of the game.
        
        Returns:
            float: Heuristic score for the state.
        """
        score = 0
        diversity_points = 5
        tie_breaker_weight = 0.1
        
        for city in self.get_player_cities_with_piece(state, self.get_id()):
            surrounding_resources = self.get_surrounding_resources(city[0], state)
            unique_resources = set(surrounding_resources)
            
            # Check for Divercité configuration (4 unique resources around city)
            if len(unique_resources) == 4:
                score += diversity_points
            else:
                # Score based on identical resources if not all unique
                same_color_count = surrounding_resources.count(city[1].piece_type[0])
                score += same_color_count  # 1 point per identical resource
            
                # Tie-breaker score: count cities with majority identical colors around them
                if same_color_count >= 3:
                    score += tie_breaker_weight * same_color_count

        return score
    

    def get_block_opponent_divercity_potential(self, state: GameStateDivercite) -> int:
        opponent_cities = self.get_player_cities_with_piece(state, self.get_opponent_id(state))
        block_score = 0
        for city in opponent_cities:
            surrounding_resources = self.get_surrounding_resources(city[0], state)
            unique_resources_needed = 4 - len(set(surrounding_resources))
            if unique_resources_needed > 0:
                block_score += unique_resources_needed  # Increase block score based on the number of resources needed to disrupt
        return block_score

################# Helper functions #################

    def unique_pieces_and_city_count(self, current_state: GameStateDivercite):
        # I need to know how many different type  pieces I have left and how many different pieces my opponent has left
        # I need to know how many different type cities I have and how many cities my opponent has
        count_my_pieces_left = 0
        count_opponent_pieces_left = 0

        my_remaining_pieces = current_state.players_pieces_left.get(self.get_id(), {})
        for p in my_remaining_pieces:
            if my_remaining_pieces[p] > 0:
                count_my_pieces_left += 1

        opponent_remaining_pieces = current_state.players_pieces_left.get(self.opponent_id, {})
        for p in opponent_remaining_pieces:
            if opponent_remaining_pieces[p] > 0:
                count_opponent_pieces_left += 1
        return count_my_pieces_left, count_opponent_pieces_left
    

    def get_neighboring_cities(self, row, col):
        # Define the possible moves (up, down, left, right)
        moves = [(1, 1),(-1, -1), (-1, 1), (1, -1)]
        neighbors = []
        
        # Check each move to see if it leads to a city
        for move in moves:
            new_col, new_row  = col + move[0], row + move[1]
            # Ensure the new position is within the board boundaries
            if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                # Check if the cell is a city ('C')
                if self.board[new_col][new_row] == 'C':
                    neighbors.append((new_col,new_row))
        
        return neighbors
    
    def choose_most_available_resource_and_no_points(self, current_state: GameStateDivercite, valid_pieces_destroy_opponent_divercity: List[str], city_piece: Piece):
        # I want to prioritize the resource that is most available and that will not give a point to the opponent
        my_remaining_pieces = current_state.players_pieces_left.get(self.get_id(), {})
        city_color = city_piece.piece_type[:1]
        # Initialize the resource to choose and the amount left
        resource_to_choose = None
        amount_left = 0

        for resource in valid_pieces_destroy_opponent_divercity:
            # it will prevent a diverity and it will not give a point to the opponent
            if resource != city_color + 'R' and my_remaining_pieces[resource] > amount_left:
                amount_left = my_remaining_pieces[resource]
                resource_to_choose = resource
        return resource_to_choose
    
    def chose_most_available_resource(self, current_state: GameStateDivercite, valid_pieces : List[str]):
        # I want to prioritize the resource that is most available
        my_remaining_pieces = current_state.players_pieces_left.get(self.get_id(), {})
        resource_to_choose = None
        amount_left = 0

        for resource in valid_pieces:
            if my_remaining_pieces[resource] > amount_left:
                amount_left = my_remaining_pieces[resource]
                resource_to_choose = resource
        return resource_to_choose
    
    def get_surrounding_resources(self, city: Tuple[int, int], state: GameStateDivercite) -> List[str]:
        # Get the resources surrounding a city
        resources = []
        for direction in state.get_neighbours(city[0], city[1]):
            piece, _ = state.get_neighbours(city[0], city[1])[direction]
            if isinstance(piece, Piece):
                resources.append(piece.piece_type)
        return resources
    
################# Table of actions #################
    #ULTIMATE TODO prioritize city close to each other, opponent cities
    def place_cities(self, current_state: GameStateDivercite):
        # Focuses on placing same color cities next to each others
        already_place_city = self.get_player_cities_with_piece(current_state, self.get_id())
        remaining_pieces = current_state.players_pieces_left.get(self.get_id(), {}) 
                          
        if len(already_place_city) == 8:
            # all cities are placed
            return None
        opponent_cities = self.get_player_cities_with_piece(current_state, self.get_opponent_id(current_state))
        
        if opponent_cities:
            for (x, y), city in opponent_cities:
                city_color = city.piece_type[:2]
                neighbours = self.get_neighboring_cities(x, y)
                for (nx, ny) in neighbours:
                    for action in self.getPossibleActions(current_state):
                        # I had to flip the x and y because the position is in (y, x) and not (x, y)
                        if (ny, nx) == action.data['position'] and action.data['piece'] == city_color:
                            return action
        
        if already_place_city:
            for (x, y), city in already_place_city: #city.piece_type = 'RCW'
                city_color = city.piece_type[:2]
                if remaining_pieces[city_color] == 1:
                    neighbours = self.get_neighboring_cities(x, y)
                    for (nx, ny) in neighbours:
                        for action in self.getPossibleActions(current_state):
                            # I had to flip the x and y because the position is in (y, x) and not (x, y)
                            if (ny, nx) == action.data['position'] and action.data['piece'] == city_color:
                                return action
        
        #TODO place a city in the middle
        place_city_in_middle = [(4, 3), (3, 4), (4, 5), (5, 4), (5, 5)]
        for action in self.getPossibleActions(current_state):
            for (x, y) in place_city_in_middle:
                if action.data['position'] == (x, y) and action.data['piece'][1] == 'C':
                    return action
                
        for action in self.getPossibleActions(current_state):
            if action.data['piece'][1] == 'C':
                return action
            
        return None
    
    def divercity_priority(self, current_state:GameState):
        possible_Divercite_actions = self.get_all_possible_divercities(current_state, self.get_id())
        possible_Divercite_actions = self.sort_divercity(possible_Divercite_actions)

        for divercity in possible_Divercite_actions:
            if len(divercity[1]) == 1 : 
                action = self.do_divercity(current_state, self.get_id(), possible_Divercite_actions)
                current_score = current_state.scores[self.get_id()] - current_state.scores[self.opponent_id]
                next_state = current_state.apply_action(action)
                # Don't do a divercity if opponent also gets a divercity
                # if score difference is not higher than current score
                # this means the opponent will also get a divercity
                if next_state.scores[self.get_id()] - next_state.scores[self.opponent_id] > current_score:
                    return action
    
################# Transposition table #################

    def hash_state(self, state: GameState):
        board_state = str(state.get_rep().get_env())
        return f"{board_state}"
