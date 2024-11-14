import random
from collections import defaultdict
from player_divercite import PlayerDivercite
from typing import List, Tuple
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from game_state_divercite import GameStateDivercite
from seahorse.utils.custom_exceptions import MethodNotImplementedError
from seahorse.game.light_action import LightAction
from seahorse.game.game_layout.board import Board, Piece

class MyPlayer(PlayerDivercite):
    def __init__(self, piece_type: str, name: str = "MyPlayer", alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 0.1):
        super().__init__(piece_type, name)
        self.q_table = defaultdict(float)  # Q-table for storing (state, action) values
        self.alpha = alpha                 # Learning rate
        self.gamma = gamma                 # Discount factor
        self.epsilon = epsilon             # Exploration rate
    
    def compute_action(self, current_state: GameState, remaining_time: int = 1e9, **kwargs) -> Action:
        state_representation = self.get_state_representation(current_state)
        possible_actions = list(current_state.generate_possible_light_actions())
        
        if random.uniform(0, 1) < self.epsilon and possible_actions:
            action = random.choice(possible_actions)  # Explore
        else:
            action = self.get_best_action(current_state)  # Exploit
        
        # Execute action and get next state and reward
        next_state = self.transition(action, current_state)
        next_state_representation = self.get_state_representation(next_state)
        reward = self.evaluate_reward(next_state, action)
        
        # Update Q-value
        next_best_action = self.get_best_action(next_state)  # Pass GameState here
        self.q_table[(state_representation, action)] += self.alpha * (
            reward + self.gamma * self.q_table[(next_state_representation, next_best_action)] 
            - self.q_table[(state_representation, action)]
        )
        
        return action

    def get_best_action(self, state: GameState) -> Action:
        # Get the action with the highest Q-value for a given GameState
        possible_actions = list(state.generate_possible_light_actions())
        if not possible_actions:
            return None
        best_action = max(possible_actions, key=lambda action: self.q_table[(self.get_state_representation(state), action)])
        return best_action


    
    def get_state_representation(self, state: GameState):
        # Convert GameState to a unique hashable representation
        # Example: could be based on positions of pieces, scores, etc.
        return tuple(state.scores)  # Simplify this as needed for your game
    
    
    def evaluate_reward(self, state: GameState, action: Action) -> float:
        # Define reward based on the state and action; for example:
        return state.scores[self.get_id()] - state.scores[self.get_opponent_id(state)]
    
    def transition(self, action: Action, current_state: GameState) -> GameState:
        """
        Simulates taking the given action in the current state and returns the resulting game state.
        """
        # If the framework provides a way to apply actions to the game state, use it:
        # e.g., return current_state.apply_action(action)
        
        # If no such method exists, this function must be implemented to modify
        # current_state manually to reflect the result of `action`.
        # Example (pseudocode):
        return current_state.apply_action(action)    # Apply action to simulate the new state


        
    def get_opponent_id(self, current_state:GameState):
        opponent_id = 0
        for players in current_state.players:
            if players.get_id() != self.get_id():
                opponent_id = players.get_id()
        return opponent_id