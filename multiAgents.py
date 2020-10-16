# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        (x,y) = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        for ghost in newGhostStates:
          (gx,gy) = ghost.getPosition()
          if abs(gx - x) + abs(gy - y) < 1 and newScaredTimes[0] is 0:
            return -float(1e9+7)
        
        mindist = 10000007
        for (mx,my) in newFood.asList(): 
          mindist = min(mindist, abs(mx - x) + abs(my - y))
        if len(newFood.asList()) is 0 : 
          mindist = 0
        extra = len(currentGameState.getFood().asList()) - len(newFood.asList())
        if action is 'Stop':
          extra = extra - 10;
        "*** YOUR CODE HERE ***"
        return successorGameState.getScore() + extra * 10 - mindist

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.layer(gameState,self.depth*gameState.getNumAgents()-1,0)[1];
        

    def layer(self, gameState, depth, agent):
      if agent is gameState.getNumAgents():
        agent = 0
      if depth is 0 or gameState.isWin() or gameState.isLose():
        scores = []
        for action in gameState.getLegalActions(agent):
          scores.append((self.evaluationFunction(gameState.generateSuccessor(agent,action)),action))
        if len(scores) is 0:
          return self.evaluationFunction(gameState),'Done'
        else:
          if agent is 0:
            maxScore = max(scores)
            pos = [i for i, j in enumerate(scores) if j == maxScore]
            return scores[random.choice(pos)]
          else:
            minScore = min(scores)
            pos = [i for i, j in enumerate(scores) if j == minScore]
            return scores[random.choice(pos)]
      if agent is 0:
        scores = []
        for action in gameState.getLegalActions(agent):
            score = self.layer(gameState.generateSuccessor(agent,action),depth - 1,agent + 1)[0]
            if action is 'Stop':
                score = score - 1000
            scores.append((score,action));
        maxScore = max(scores)
        pos = [i for i, j in enumerate(scores) if j == maxScore]
        return scores[random.choice(pos)]
      if agent is not 0:
        scores = []
        for action in gameState.getLegalActions(agent):
            score = self.layer(gameState.generateSuccessor(agent,action),depth - 1,agent + 1)[0]
            scores.append((score,action))
        minScore = min(scores)
        pos = [i for i, j in enumerate(scores) if j == minScore]
        return scores[random.choice(pos)]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action = self.AlphaBeta(gameState,-int(1e9+7),+int(1e9+7),self.depth * gameState.getNumAgents() - 1,0)[1]

        return action
        util.raiseNotDefined()

    def AlphaBeta(self,gameState, alpha, beta, depth, agent):
        


        if agent is gameState.getNumAgents():
            agent = 0


        scores = []
        if depth is 0 or gameState.isWin() or gameState.isLose():
            
            for action in gameState.getLegalActions(agent):
                score = self.evaluationFunction(gameState.generateSuccessor(agent,action))                
                scores.append(score)
                if agent is 0:
                    if score > beta:
                        return (score,action)
                    else :
                        alpha = max(alpha,score)
                if agent is not 0:
                    if score < alpha:
                        return (score,action)
                    else:
                        beta = min(beta,score)
            if len(scores) is 0:
                return (self.evaluationFunction(gameState),'End')
            else:
                if agent is 0:
                    maxScore = max(scores)
                    pos = [i for i, j in enumerate(scores) if j == maxScore]
                    return (maxScore,gameState.getLegalActions(agent)[random.choice(pos)])
                else:
                    minScore = min(scores)
                    pos = [i for i, j in enumerate(scores) if j == minScore]
                    return (minScore,gameState.getLegalActions(agent)[random.choice(pos)])

        for action in gameState.getLegalActions(agent):
            score = self.AlphaBeta(gameState.generateSuccessor(agent,action),alpha,beta,depth - 1, agent + 1)[0]
            scores.append(score)
            if agent is 0:
                if score > beta:
                    return (score,action)
                else:
                    alpha = max(alpha,score)
            else:
                if score < alpha:
                    return (score,action)
                else:
                    beta = min(beta,score)
        
        if len(scores) is 0:
            return self.evaluationFunction(gameState)

        if agent is 0:
            maxScore = max(scores)
            pos = [i for i, j in enumerate(scores) if j == maxScore]
            choice = random.choice(pos)
            return (maxScore,gameState.getLegalActions(agent)[choice])
        else:
            minScore = min(scores)
            pos = [i for i, j in enumerate(scores) if j == minScore]
            choice = random.choice(pos)
            return (minScore,gameState.getLegalActions(agent)[choice])

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.Expectimax(gameState,self.depth * gameState.getNumAgents() - 1, 0)[1]



    def Expectimax(self, gameState, depth, agent):
        if agent is gameState.getNumAgents() :
            agent = 0
        if depth is 0 or gameState.isWin() or gameState.isLose():
            scores = []
            for action in gameState.getLegalActions(agent):
                scores.append(self.evaluationFunction(gameState.generateSuccessor(agent,action)))
            if len(scores) is 0:
                return (self.evaluationFunction(gameState),'End')
            if agent is 0:
                return (max(scores),'End')
            else:
                return (float(sum(scores))/float(len(scores)),'End')

        scores = []
        scoresrec = []

        for action in gameState.getLegalActions(agent):
            score = self.Expectimax(gameState.generateSuccessor(agent,action),depth - 1,agent + 1)[0]
            if action is 'Stop':
                score = score - 10
            scores.append((score,action))
            scoresrec.append(score)
        if agent is 0:
            maxScore = max(scores)
            pos = [i for i, j in enumerate(scores) if j == maxScore]
            return scores[pos[0]]
        else:
            return (float(sum(scoresrec))/float(len(scoresrec)),'Random')


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    (x,y) = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    ghostCount = currentGameState.getNumAgents() - 1
    score = currentGameState.getScore()

    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = score - len(foodList.asList())
    hunt = False
    for ghost in ghostStates:
        (gx,gy) = ghost.getPosition()
        if newScaredTimes[0] is not 0:
            hunt = True
            score = score + 100 - (abs(gx - x) + abs(gy - y))
        else:
            hunt = False
            if abs(gx - x) + abs(gy - y) < 2:
                return -float(1e9+7)
    minDist = int(1e9+7)
    for (fx,fy) in foodList.asList():
        minDist = min(abs(x - fx) + abs(y - fy), minDist)

    if len(foodList.asList()) is 0:
        score = score + 10;
    else:
        score = score - minDist - len(foodList.asList()) * 15

    return score 

# Abbreviation
better = betterEvaluationFunction

