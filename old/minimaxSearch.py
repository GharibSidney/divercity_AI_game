from seahorse.game.action import Action
from seahorse.game.game_state import GameState
# éventuellement modifier le prochain import
from my_player_base import  MyPlayer 


class minimaxSearch():

    def __init__(self, player:MyPlayer, state:GameState):
        self.player = player
        self.opponent_id = self.get_opponent_id(state)
        self.id = self.player.get_id()
        # max depth of the tree
        self.depth_max = 1
        # self.counter = 0

    def minimaxSearch(self, state: GameState, isMax:bool): #player: MyPlayer,
        # self.counter = 0
        if isMax: v, m = self.maxValue(state, 0)
        else: v, m = self.minValue(state, 0)
        return m #        return v, m


    def maxValue(self, state: GameState, counter:int):
        if self.isTerminal(counter):
            return state.get_next_game_state().scores[self.id] - state.get_next_game_state().scores[self.opponent_id], None
        
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
            return state.scores[self.opponent_id] - state.scores[self.id], None
        
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
            if players.get_id() != self.player.get_id():
                opponent_id = players.get_id()
        return opponent_id