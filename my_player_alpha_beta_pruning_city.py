import seahorse
from player_divercite import PlayerDivercite
from typing import List, Tuple
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from game_state_divercite import GameStateDivercite
from seahorse.utils.custom_exceptions import MethodNotImplementedError
from seahorse.game.light_action import LightAction
from seahorse.game.game_layout.board import Board, Piece

import random

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


    def compute_action(self, current_state: GameState, remaining_time: int = 1e9, **kwargs) -> Action:
        """
        Use the minimax algorithm to choose the best action based on the heuristic evaluation of game states.

        Args:
            current_state (GameState): The current game state.

        Returns:
            Action: The best action as determined by minimax.
        """

        possible_Divercite_actions = self.get_all_possible_divercities(current_state, self.get_id())
        possible_Divercite_actions = self.sort_divercity(possible_Divercite_actions)

        player_cities = self.get_player_cities(current_state, self.get_id())
        print(f"voici les villes de player {self.get_name()} AVANT LE COUP (ca match avec ce qui ya en haut du separateur):")
        print(player_cities)

        for divercity in possible_Divercite_actions:
            if len(divercity[1]) == 1 : 
                print('boy')
                action = self.do_divercity(current_state, self.get_id(), possible_Divercite_actions)
                if action is not None:
                    return action
                
        action = self.prevent_opponent_divercity(current_state, self.get_id())
        if action is not None:
            return action
        
        action = self.place_cities(current_state)
        if action is not None:
            return action



        isMax = current_state.step%2 == 0

        self.depth_max = self.pick_depth_max(isMax, current_state)
        self.opponent_id = self.get_opponent_id(current_state)

        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        return self.minimaxSearch(current_state, isMax)

################ Minmax part ################

    def minimaxSearch(self, state: GameState, isMax:bool):
        # if isMax: v, m = self.maxValue(state, 0)
        # else: v, m = self.minValue(state, 0)
        v, m = self.maxValue(state, None, 0)
        return m # return v, m


    def maxValue(self, state: GameState, main_action:LightAction, counter:int, alpha = -1000000, beta = 1000000):
        if self.isTerminal(counter):
            return self.evaluation(state, main_action, state.scores[self.get_id()] - state.scores[self.opponent_id]), None
        
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
        return v_star, m_star

    def minValue(self, state: GameState, main_action:LightAction, counter: int, alpha = -1000000, beta = 1000000):
        if self.isTerminal(counter):
            # the best score is reversed because we are the opponent
            return  self.evaluation(state, main_action, state.scores[self.opponent_id] - state.scores[self.get_id()]), None
        
        v_star = 1000000
        m_star = None
        for action in self.getPossibleActions(state):
            temporary_state = self.transition(action, state)
            counter +=1
            v, _ = self.maxValue(temporary_state, action, counter)
            if  v < v_star:
                v_star = v
                m_star = action
                beta = min(v_star, beta)
            counter -= 1
            if v_star <= alpha:
                return v_star, m_star
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
    
    def pick_depth_max(self, isMax:bool, current_state:GameState):
        if current_state.step < 26:
            return 2
        elif current_state.step < 30:
            self.place_cities(current_state)
            return  4 #40 - current_state.step
        else:
           return 40 - current_state.step
    

################ Divercity part ################



    def get_player_cities(self, current_state: GameStateDivercite, player_id: int):
            board = current_state.get_rep().get_env()
            return [(i, j) for (i, j), piece in board.items() if isinstance(piece, Piece) and piece.get_type()[1] == 'C' and piece.get_owner_id() == player_id]
    
    def get_player_cities_with_piece(self, current_state: GameStateDivercite, player_id: int):
        board = current_state.get_rep().get_env()
        return [[(i, j),piece] for (i, j), piece in board.items() if isinstance(piece, Piece) and piece.get_type()[1] == 'C' and piece.get_owner_id() == player_id]
    
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

            resources_missing = [color + 'R' for color, count in neighbor_colors_count.items() if count == 0]
            all_possible_divercities.append (((x, y), resources_missing))

        return all_possible_divercities
    
    def do_divercity(self, current_state: GameStateDivercite, player_id: int, all_possible_divercities: List[Tuple[Tuple[int, int], int]]):
        remaining_pieces = current_state.players_pieces_left.get(player_id, {})

        for (x, y), resources_missing in all_possible_divercities:
            neighbours = current_state.get_neighbours(x, y)

            for direction, (piece, (nx, ny)) in neighbours.items():
                if piece == 'EMPTY':
                    valid_pieces = [p for p in remaining_pieces if p in resources_missing and remaining_pieces[p] > 0]

                    if valid_pieces:
                        chosen_piece = random.choice(valid_pieces) #TODO to change to make sure to pick most available resource
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
        # TODO No need for sorting because I only need to prevent the opponent from getting a divercity when a single resource missing
        ordered_opponents_all_possible_divercities = self.get_all_possible_divercities(current_state, opponent_id) #sorted(self.get_all_possible_divercities(current_state, opponent_id), key=lambda x: len(x[1]))
        single_resource_left_divercities = [divercity for divercity in ordered_opponents_all_possible_divercities if len(divercity[1]) == 1]
        # I only need to prevent the opponent from getting a divercity when a single resource missing
        for (x, y), resources_missing in single_resource_left_divercities:

            neighbours = current_state.get_neighbours(x, y)

            for direction, (piece, (nx, ny)) in neighbours.items():
                if piece == 'EMPTY':
                    valid_pieces_destroy_opponent_divercity = [p for p in my_remaining_pieces if p not in resources_missing and my_remaining_pieces[p] > 0 and p[1] == 'R']
                    if valid_pieces_destroy_opponent_divercity:
                        chosen_piece = random.choice(valid_pieces_destroy_opponent_divercity) #TODO to change to make sure not to give a point to the opponent
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

    def evaluation(self, state:GameStateDivercite, action: LightAction, score:int) -> int:
        return score + 2 * self.is_city_placement(action) + self.max_available_resource(state, action) + self.resource_placement(state, action)

    def resource_placement(self, state:GameStateDivercite, action: LightAction):
        # Mettre une pièce de sorte à maximiser nos points et empêcher une éventuelle diversité de l'adversaire où il lui manque 2 pièces et nous on met une pièce qu'il avait pas, et qu'il fait juste mettre la dernière ressource 
        if self.is_resource_placement(action):
            # TRES IMPORTANT: n'oublie pas que le state que tu vois ne concordes pas avec le state ici, car ici c'est un state vraiment avance en raison d'un depth plus profond avec minmax
            neighbours = state.get_neighbours(action.data["position"][0], action.data["position"][1])
            opponent_neighbours_cities = []
            for _, (piece, coords) in neighbours.items():
                if isinstance(piece, Piece) and piece.piece_type[1] == 'C' and piece.get_owner_id() == self.opponent_id:
                    opponent_neighbours_cities.append((piece, coords))

            all_opponent_divercity = self.get_all_possible_divercities(state, self.opponent_id)
            opponent_cities_and_their_resources_missings_near_placed_resource = []

            for city in opponent_neighbours_cities:
                if len(all_opponent_divercity) > 0 and city[1] in all_opponent_divercity[0][0]:
                    opponent_cities_and_their_resources_missings_near_placed_resource.append((city, all_opponent_divercity[0][1]))
            
            player_stub = myPlayerStub(self.get_id(), self.get_piece_type())
            piece_type = action.data["piece"] + player_stub.get_color()
            # Place de facon fictive la resource que tu voulais mettre ici pour voir si tu donnes une divercité à l'adversaire avec ton mouvement
            state.rep.env[action.data["position"][0], action.data["position"][1]] = Piece(piece_type, player_stub)

            all_opponent_divercity_future_state = self.get_all_possible_divercities(state, self.opponent_id)
            opponent_cities_and_their_resources_missings_near_placed_resource_future_state = []

            for city in opponent_neighbours_cities:
                if len(all_opponent_divercity_future_state) > 0 and city[1] in all_opponent_divercity_future_state[0][0]:
                    opponent_cities_and_their_resources_missings_near_placed_resource_future_state.append((city, all_opponent_divercity_future_state[0][1]))

            for _, resources_missing_future_state in opponent_cities_and_their_resources_missings_near_placed_resource_future_state:
                for _, ressources_missings in opponent_cities_and_their_resources_missings_near_placed_resource:
                    if len(resources_missing_future_state) == 1 and len(resources_missing_future_state) < len(ressources_missings):
                        return 0

            return 1
            #TODO: # Place de facon fictive la resource que tu voulais mettre ici pour voir si tu donnes un point a l'adversaire
            
        else:
            return 0

    def is_city_placement(self, action: LightAction):
        # if city then return True else False
        return action.data['piece'][1] == 'C'
    
    def is_resource_placement(self, action: LightAction):
        # if resource then return True else False
        return action.data['piece'][1] == 'R'
    
    def max_available_resource(self, state:GameStateDivercite, action: LightAction):
        if action.data['piece'][1] == 'R':
            remaining_pieces = state.players_pieces_left.get(self.get_id(), {})
            for resource in remaining_pieces:
                # print(action.data['piece'][:2])
                if action.data['piece'][:2] == resource:
                    # print(remaining_pieces[resource])
                    return remaining_pieces[resource]
        else:
            return 0
    

################# Helper functions #################

    def unique_pieces_and_city_count(self, current_state: GameStateDivercite):
        # I need to know how many different type  pieces I have left and how many different pieces my opponent has left
        # I need to know how many different type cities I have and how many cities my opponent has
        count_my_pieces_left = 0
        count_opponent_pieces_left = 0

        my_remaining_pieces = current_state.players_pieces_left.get(self.get_id(), {})
        for p in my_remaining_pieces:
            print(p, my_remaining_pieces[p])
            if my_remaining_pieces[p] > 0:
                count_my_pieces_left += 1
        opponent_remaining_pieces = current_state.players_pieces_left.get(self.opponent_id, {})

        for p in opponent_remaining_pieces:
            print(p, opponent_remaining_pieces[p])
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
                print(self.board[new_col][new_row])
                if self.board[new_col][new_row] == 'C':
                    neighbors.append((new_col,new_row))
        
        return neighbors
    
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
                neighbours = self.get_neighboring_cities(x, y) #TODO try to put cities near the middle
                for (nx, ny) in neighbours:
                    for action in self.getPossibleActions(current_state):
                        # I had to flip the x and y because the position is in (y, x) and not (x, y)
                        if (ny, nx) == action.data['position'] and action.data['piece'] == city_color:
                            return action
        
        if already_place_city:
            for (x, y), city in already_place_city: #city.piece_type = 'RCW'
                city_color = city.piece_type[:2]
                if remaining_pieces[city_color] == 1:
                    neighbours = self.get_neighboring_cities(x, y) #TODO to fix
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

class myPlayerStub:
    def __init__(self, player_id, player_color):
        self.player_id = player_id
        self.color = player_color

    def get_id(self):
        return self.player_id
    
    def get_color(self):
        return self.color