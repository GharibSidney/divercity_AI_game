from seahorse.game.action import Action
from seahorse.game.game_state import GameState

# state: GameState
def minimaxSearch(state: GameState, isMax):
    if isMax: v, m = maxValue(state)
    else: v, m = minValue(state)
    return v, m

def maxValue(state: GameState):
    if isTerminal(state):
        return #state # score # return something see class notes
    v_star = float('-inf')
    m_star = None
    for action in getPossibleActions(state):
        temporary_state = transition(state, action)
        v, _ = minValue(temporary_state)
        if  v > v_star:
            v_star = v
            m_star = action
    return v_star, m_star

def minValue(state: GameState):
    if isTerminal(state):
        return #state # score # return something see class notes
    v_star = float('inf')
    m_star = None
    for action in getPossibleActions(state):
        temporary_state = transition(state, action)
        v, _ = maxValue(temporary_state)
        if  v < v_star:
            v_star = v
            m_star = action
    return v_star, m_star
    
def isTerminal(state: GameState, depth_max: int):
    NotImplementedError()

def getPossibleActions(state: GameState):
    # J'ai mis un fonction dans une functon, car 
    # si jamais on veut changer pour light action
    # on aura qu'à changer le return
    return state.generate_possible_heavy_actions()

def transition(state: GameState, action: Action):
    best_score = action.get_next_game_state().scores[self.get_id()] - action.get_next_game_state().scores[opponent_id]

    NotImplementedError()