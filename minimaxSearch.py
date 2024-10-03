from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from my_player import  MyPlayer


class minimaxSearch():

    def __init__(self, player:MyPlayer,):
        self.player = player

    def minimaxSearch(self, state: GameState, player: MyPlayer,  isMax:bool):
        if isMax: v, m = self.maxValue(state)
        else: v, m = self.minValue(state)
        return v, m

    def maxValue(self, state: GameState):
        if self.isTerminal(state):
            return #state # score # return something see class notes
        v_star = float('-inf')
        m_star = None
        for action in self.getPossibleActions(state):
            temporary_state = self.transition(state, action)
            v, _ = self.minValue(temporary_state)
            if  v > v_star:
                v_star = v
                m_star = action
        return v_star, m_star

    def minValue(self, state: GameState):
        if self.isTerminal(state):
            return #state # score # return something see class notes
        v_star = float('inf')
        m_star = None
        for action in self.getPossibleActions(state):
            temporary_state = self.transition(state, action)
            v, _ = self.maxValue(temporary_state)
            if  v < v_star:
                v_star = v
                m_star = action
        return v_star, m_star
        
    def isTerminal(self, state: GameState, depth_max: int):
        NotImplementedError()

    def getPossibleActions(self, state: GameState):
        # J'ai mis un fonction dans une functon, car 
        # si jamais on veut changer pour light action
        # on aura qu'à changer le return
        return state.generate_possible_heavy_actions()

    def transition(self, state: GameState, action: Action):
        best_score = action.get_next_game_state().scores[self.player.get_id()] - action.get_next_game_state().scores[opponent_id]

        NotImplementedError()