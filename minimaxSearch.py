from seahorse.game.action import Action
from seahorse.game.game_state import GameState
# éventuellement modifier le prochain import
from players.my_player_beats_greedy import  MyPlayer 


class minimaxSearch():

    def __init__(self, player:MyPlayer, state:GameState):
        self.player = player
        self.opponent_id = self.player.get_opponent_id(state)
        self.id = self.player.get_id()
        # max depth of the tree
        self.depth_max = 3
        self.counter = 0

    def minimaxSearch(self, state: GameState, isMax:bool): #player: MyPlayer,
        self.counter = 0
        if isMax: v, m = self.maxValue(state, self.counter)
        else: v, m = self.minValue(state, self.counter)
        return v, m

    def maxValue(self, state: GameState):
        if self.isTerminal():
            return action.get_next_game_state().scores[self.id] - action.get_next_game_state().scores[self.opponent_id], None
        
        v_star = -1000000
        m_star = None

        for action in self.getPossibleActions(state):
            temporary_state = self.transition(state, action)
            self.counter += 1
            v, _ = self.minValue(temporary_state)
            if  v > v_star:
                v_star = v
                m_star = action
        return v_star, m_star

    def minValue(self, state: GameState):
        if self.isTerminal():
            # the best score is reversed because we are the opponent
            return action.get_next_game_state().scores[self.opponent_id] - action.get_next_game_state().scores[self.id], None
        
        v_star = 1000000
        m_star = None
        for action in self.getPossibleActions(state):
            temporary_state = self.transition(state, action)
            self.counter += 1
            v, _ = self.maxValue(temporary_state)
            if  v < v_star:
                v_star = v
                m_star = action
        return v_star, m_star
        
    def isTerminal(self):
        return self.depth_max == self.counter

    def getPossibleActions(self, state: GameState):
        # J'ai mis un fonction dans une fonction, car 
        # si jamais on veut changer pour light action
        # on aura qu'à changer le return 
        return state.generate_possible_heavy_actions()

    def transition(self, action: Action):
        
        return action.get_next_game_state()
