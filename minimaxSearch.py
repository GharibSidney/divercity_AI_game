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
    
def isTerminal(state: GameState):
    NotImplementedError()

def getPossibleActions(state: GameState):
    NotImplementedError()
def transition(state: GameState, action: Action):
    NotImplementedError()