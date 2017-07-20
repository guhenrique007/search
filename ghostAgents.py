# ghostAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
  def __init__( self, index ):
    self.index = index

  def getAction( self, state ):
    dist = self.getDistribution(state)
    if len(dist) == 0: 
      return Directions.STOP
    else:
      return util.chooseFromDistribution( dist )
    
  def getDistribution(self, state):
    "Returns a Counter encoding a distribution over actions from the provided state."
   # from util import PriorityQueue, Counter, manhattanDistance
   # 
   # estadoFantasma = state.getGhostState(self.index)
   # acoesLegais = state.getLegalActions(self.index)
   # isAssustado = estadoFantasma.scaredTimer > 0
   # posicaoPacman = state.getPacmanPosition()
   # dist = Counter()

   # if not isAssustado:
   #   heap = PriorityQueue()
   #   expandidos = set()
   #   heap.push((state,[]),0)

   #   for posicao in state.getGhostPositions():
        

class RandomGhost( GhostAgent ):
  "A ghost that chooses a legal action uniformly at random."
  def getDistribution( self, state ):
    dist = util.Counter()
    for a in state.getLegalActions( self.index ): dist[a] = 1.0
    dist.normalize()
    return dist

class MeuGhost( GhostAgent ):
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee
  
  def getGhostSuccessors(self, legalActions, state):
    return [(state.generateSuccessor(self.index, action), action, state.generateSuccessor(self.index, action).getGhostPosition(self.index)) for action in legalActions]
      
  def getDistribution( self, state ):
    # Read variables from state
    from util import PriorityQueue, Counter
    ghostState = state.getGhostState( self.index )
    legalActions = state.getLegalActions( self.index )
    pos = state.getGhostPosition( self.index )
    isScared = ghostState.scaredTimer > 0
    
    posicoesFantasmas = set()
    dist = Counter()

    for posicao in state.getGhostPositions():
      if posicao != state.getGhostPosition(self.index):
        posicoesFantasmas.add(posicao)

    speed = 1
    if isScared: speed = 0.5
    
    actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
    newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
    pacmanPosition = state.getPacmanPosition()

    # Select best actions given the state
    #distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
    distancesToPacman = []
    for pos in newPositions:
      if pos in posicoesFantasmas:
        distancesToPacman.append(manhattanDistance(pos, pacmanPosition)*2)
      else:
        distancesToPacman.append(manhattanDistance(pos, pacmanPosition))

    if isScared:
      bestScore = max( distancesToPacman )
      bestProb = self.prob_scaredFlee
    
    else:
      heap = PriorityQueue()
      for proxEstado, proxAcao, proxPos in self.getGhostSuccessors(
        state.getLegalActions(self.index),state):
        prioridade = manhattanDistance(proxPos, pacmanPosition) + 1
        if proxPos in posicoesFantasmas:
          prioridade *= 2 
        heap.push((proxEstado, proxAcao, 1), prioridade)
      
      while not (heap.isEmpty()): 
        estadoAtual, primAcao, numAcoes  = heap.pop()
        if estadoAtual.getGhostPosition(self.index) == pacmanPosition:
          dist[primAcao] = 1
          return dist
        for proxEstado, proxAcao, proxPos in self.getGhostSuccessors(
            estadoAtual.getLegalActions(self.index), estadoAtual):
          
            if not proxEstado.getGhostPosition(self.index) in posicoesFantasmas:
              numAcoes += 1
              heuristica = manhattanDistance(proxPos, pacmanPosition)
              heap.push((proxEstado, primAcao, numAcoes)
                  ,numAcoes + heuristica)
              posicoesFantasmas.add(proxPos)

class DirectionalGhost( GhostAgent ):
  "A ghost that prefers to rush Pacman, or flee when scared."
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee
  
  def getGhostSuccessors(self, legalActions, state):
    return [(state.generateSuccessor(self.index, action), action, state.generateSuccessor(self.index, action).getGhostPosition(self.index)) for action in legalActions]
      
  def getDistribution( self, state ):
    # Read variables from state
    from util import PriorityQueue, Counter
    ghostState = state.getGhostState( self.index )
    legalActions = state.getLegalActions( self.index )
    pos = state.getGhostPosition( self.index )
    isScared = ghostState.scaredTimer > 0
    
    posicoesFantasmas = set()
    dist = Counter()

    for posicao in state.getGhostPositions():
      if posicao != state.getGhostPosition(self.index):
        posicoesFantasmas.add(posicao)

    speed = 1
    if isScared: speed = 0.5
    
    actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
    newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
    pacmanPosition = state.getPacmanPosition()

    # Select best actions given the state
    #distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
    distancesToPacman = []
    for pos in newPositions:
      if pos in posicoesFantasmas:
        distancesToPacman.append(manhattanDistance(pos, pacmanPosition)*2)
      else:
        distancesToPacman.append(manhattanDistance(pos, pacmanPosition))

    if isScared:
      bestScore = max( distancesToPacman )
      bestProb = self.prob_scaredFlee
    
    else:
      heap = PriorityQueue()
      for proxEstado, proxAcao, proxPos in self.getGhostSuccessors(
        state.getLegalActions(self.index),state):
        prioridade = manhattanDistance(proxPos, pacmanPosition) + 1
        if proxPos in posicoesFantasmas:
          prioridade *= 2 
        heap.push((proxEstado, proxAcao, 1), prioridade)
      
      while not (heap.isEmpty()): 
        estadoAtual, primAcao, numAcoes  = heap.pop()
        if estadoAtual.getGhostPosition(self.index) == pacmanPosition:
          dist[primAcao] = 1
          return dist
        for proxEstado, proxAcao, proxPos in self.getGhostSuccessors(
            estadoAtual.getLegalActions(self.index), estadoAtual):
          
            if not proxEstado.getGhostPosition(self.index) in posicoesFantasmas:
              numAcoes += 1
              heuristica = manhattanDistance(proxPos, pacmanPosition)
              heap.push((proxEstado, primAcao, numAcoes)
                  ,numAcoes + heuristica)
              posicoesFantasmas.add(proxPos)
