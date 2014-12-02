####
#
# Gameworld
# Jake Kinsman
# 11/28/2014
#
####

import terrain as Terrain
import state as State
import agent as Agent
import graphics as Graphics
import copy
import random

class gameWorld(object):
	
	def __init__(self):
		self.terrains = [Terrain.terrain(), Terrain.terrain(), Terrain.terrain()]
		self.livingReward = 0
		self.discount = 0.95
		self.noise = 0
		self.startState = State.state()
		self.transitionalStates = [State.state((9,0), 0), State.state((9,0), 1)]
		self.terminalState = State.state((9,0), 2)
		self.adpAgents = []
		self.adpAgentIndex = 0
		self.adpAgentStates = []
		self.tdAgents = []
		self.tdAgentIndex = 0
		self.tdAgentStates = []
		self.randomAgents = []
		self.randomAgentIndex = 0
		self.randomAgentStates = []
		self.transitionalReward = 1000
		self.terminalReward = 2000

	#tested	
	def getDiscount(self):
		return self.discount

	#tested
	def setDiscount(self, disc):
		self.discount = disc

	#tested
	def setNoise(self, noise):
		self.noise = noise
	
	#tested
	def getNoise(self):
		return self.noise

	#tested
	def setLivingReward(self, lr):
		self.livingReward = lr
	
	#tested
	def getLivingReward(self):
		return self.livingReward
	
	#tested
	def getActions(self, state):
		x, y = state.getPosition()
		actions = list()
		if self.isTransitionalState(state) or self.isTerminalState(state):
			return ['finish']
		else:
			if x != 0:
				actions.append('west')
			if x != 9:
				actions.append('east')
			if y != 0:
				actions.append('north')
			if y != 9:
				actions.append('south')
			return actions
	#tested
	def getWorldAgent(self, agent):
		if agent.type == "adp":
			return self.adpAgents[agent.index]
		elif agent.type == "td":
			return self.tdAgents[agent.index]
		else:
			return self.randomAgents[agent.index]

	#tested
	def getAgentState(self, agent):
		newAgent = self.getWorldAgent(agent)
		if newAgent.type == "adp":
			return self.adpAgentStates[newAgent.index]
		elif newAgent.type == "td":
			return self.tdAgentStates[newAgent.index]
		else:
			return self.randomAgentStates[newAgent.index]

	#tested
	def setAgentState(self, agent, state):
		newAgent = self.getWorldAgent(agent)
		if newAgent.type == "adp":
			self.adpAgentStates[newAgent.index] = state
		elif newAgent.type == "td":
			self.tdAgentStates[newAgent.index] = state
		else:
			self.randomAgentStates[newAgent.index] = state

	#tested, less fallen
	def getReward(self, agent, state):
		newAgent = self.getWorldAgent(agent)
		if self.completedRace(state, 1):
			return self.transitionalReward
		elif self.completedRace(state, 2):
			return self.terminalReward
		else:		
			x, y = state.getPosition()
			terrain = state.getWorld()
			terrainElement = repr(self.terrains[terrain].terrainWorld[x][y])
			if terrainElement == 'grass':
				return self.terrains[terrain].terrainWorld[x][y].getScore() * newAgent.getGrassSkill()
			if terrainElement == 'forest':
				return self.terrains[terrain].terrainWorld[x][y].getScore() * newAgent.getForestSkill()
			if terrainElement == 'water':
				return self.terrains[terrain].terrainWorld[x][y].getScore() * newAgent.getWaterSkill()
			else:
				return self.terrains[terrain].terrainWorld[x][y].getScore() * newAgent.getMountainSkill()

	#tested
	def getStartState(self, terrainNum = 0):
		return State.state((0,9), terrainNum)

	#tested
	def isTransitionalState(self, state):
		return state in self.transitionalStates

	#tested
	def isTerminalState(self, state):
		return state == self.terminalState

	#tested
	def generateNextStates(self, state, action):
		if (self.isTerminalState(state) or self.isTransitionalState(state)) and action is 'finish':
			return State.state((float("inf"), float("inf")), state.getWorld())
		x, y = state.getPosition()
		world = state.getWorld()
		if action is 'east':
			return State.state((x + 1, y), world)
		if action is 'west':
			return State.state((x - 1, y), world)
		if action is 'north':
			return State.state((x, y - 1), world)
		if action is 'south':
			return State.state((x, y + 1), world)
		else:
			raise "Error, invalid action"
	#tested
	def completedRace(self, state, worldNum = 0):
		return state.getPosition() == (float("inf"), float("inf")) and state.getWorld() <= worldNum

	#tested
	def addAgent(self, agent):
		newAgent = copy.deepcopy(agent)
		newAgent.setWaterSkill(random.random() + .5)
		newAgent.setGrassSkill(random.random() + .5)
		newAgent.setForestSkill(random.random() + .5)
		newAgent.setMountainSkill(random.random() + .5)
		
		if newAgent.type is "adp":
			self.adpAgents.append(newAgent)
			self.adpAgentStates.append(State.state())
			agent.setIndex(self.adpAgentIndex)
			newAgent.setIndex(self.adpAgentIndex)
			self.adpAgentIndex += 1
		
		elif newAgent.type is "td":
			self.tdAgents.append(newAgent)
			self.tdAgentStates.append(State.state())
			agent.setIndex(self.tdAgentIndex)
			newAgent.setIndex(self.tdAgentIndex)
			self.tdAgentIndex += 1
		
		else:
			self.randomAgents.append(newAgent)
			self.randomAgentStates.append(State.state())
			agent.setIndex(self.randomAgentIndex)
			newAgent.setIndex(self.randomAgentIndex)
			self.randomAgentIndex += 1
	
	#tested
	def moveAgent(self, agent, state, action):
		newAgent = self.getWorldAgent(agent)
		x, y = state.getPosition()
		terrainElement = repr(self.terrains[state.getWorld()].terrainWorld[x][y])
		chanceToFall = None
		chanceToSlideDown = None
		chanceToSlideLeft = None
		if state in self.transitionalStates or state == self.terminalState:
			self.setAgentState(newAgent, self.generateNextStates(state, action))
		else:
			if terrainElement == 'grass':
				chanceToFall = abs(newAgent.getGrassSkill() - 1) / 4
			elif terrainElement == 'water':
				chanceToFall = abs(newAgent.getWaterSkill() - 1) / 4
			elif terrainElement == 'forest':
				chanceToFall = abs(newAgent.getWaterSkill() - 1) / 4
			else:
				chanceToFall = abs(newAgent.getMountainSkill() - 1) / 2
			x, y = state.getPosition()
			chanceToSlideDown = 0.1 - ((0.1 / 10) * (abs(y -  0)))
			chanceToSlideLeft = 0.1 - ((0.1 / 10) * (abs(x - 9)))
			if random.random() <= chanceToSlideDown:
				self.setAgentState(newAgent, State.state((x, min([9, y + 1])), state.getWorld()))
			elif random.random() <= chanceToSlideLeft:
				self.setAgentState(newAgent, State.state((max([x - 1, 0]), y), state.getWorld()))
			elif random.random() <= chanceToFall:
				self.setAgentState(newAgent, State.state((max([x - 1, 0]), min([9, y + 1])), state.getWorld()))
			else:
				self.setAgentState(newAgent, self.generateNextStates(state, action))

	#tested
	def getTerrainType(self, state):
		x, y = state.getPosition()
		return repr(self.terrains[state.getWorld()].terrainWorld[x][y])

# test = gameWorld()
# for world in test.terrains:
# 	world.showTerrain()

# print "noise: ", test.getNoise()
# test.setNoise(1)
# print "noise is now 1: ", test.getNoise()

# print "livingReward: ", test.getLivingReward()
# test.setLivingReward(0)
# print "livingReward is now 0: ", test.getLivingReward()

# print "discount: ", test.getDiscount()
# test.setDiscount(0)
# print "discount is now 0: ", test.getDiscount()
# print "\n"
# print "startState: ", test.getStartState()
# print "\n"
# print "TransitionalState? ", test.isTransitionalState(test.getStartState())
# print "TerminalState? ", test.isTerminalState(test.getStartState())
# print "\n"

# print "Actions from start state: ", test.getActions(test.getStartState())

# for action in test.getActions(test.getStartState()):
# 	print "going " + action + " from " + str(test.getStartState()) + " puts us " + str(test.generateNextStates(test.getStartState(), action))
# print "\n"
# print "Terminal Actions: ", test.getActions(State.state((9,0), 2))
# print "\n"
# print "All actions: ", test.getActions(State.state((4,5), 0))
# print "\n"
# print "In the sky: ", test.generateNextStates(State.state((9,0), 0), "finish")
# print "\n"
# print "Completed? ", test.completedRace(test.generateNextStates(State.state((9,0), 0), "finish"))
# print "Not Completed?", test.completedRace(test.getStartState())
# print "\n"
# print "grass==grass? ", Terrain.grass() == Terrain.grass()
# print "grass==mountain? ", Terrain.grass() == Terrain.mountain() 
# print "\n"
# print "No ADP Agents!"
# print "Adding ADP Agent!"
# test.addAgent(Agent.adpAgent(test))
# print test.adpAgentIndex, " ADP Agents!"
# print "adpAgent.waterScore:", test.adpAgents[0].getWaterSkill()
# print "adpAgent.grassScore:", test.adpAgents[0].getGrassSkill()
# print "adpAgent.forestScore:", test.adpAgents[0].getForestSkill()
# print "adpAgent.mountainScore:", test.adpAgents[0].getMountainSkill()
# print "adpAgent State: ", test.getAgentState(test.adpAgents[0])
# print "\n"
# print "No TD Agents!"
# print "Adding TD Agent!"
# test.addAgent(Agent.tdAgent())
# print test.tdAgentIndex, " TD Agents!"
# print "tdAgent.waterScore:", test.tdAgents[0].getWaterSkill()
# print "tdAgent.grassScore:", test.tdAgents[0].getGrassSkill()
# print "tdAgent.forestScore:", test.tdAgents[0].getForestSkill()
# print "tdAgent.mountainScore:", test.tdAgents[0].getMountainSkill()
# print "tdAgent State: ", test.getAgentState(test.tdAgents[0])
# print "\n"
# print "Testing getReward():"
# print "transitionalReward: ", test.getReward(test.adpAgents[0], State.state((float("inf"), float("inf")), 0))
# print "terminalReward: ", test.getReward(test.adpAgents[0], State.state((float("inf"), float("inf")), 2))
# print "not fallen", test.getReward(test.adpAgents[0], test.getAgentState(test.adpAgents[0]))
# print "terrain was: ", test.terrains[0].terrainWorld[0][9]
# print "\n"
# print "Create testAgent"
# testAgent = Agent.tdAgent()
# test.addAgent(testAgent)
# print "getting testAgent State: ", test.getAgentState(testAgent)
# print "Settings testAgent State to (5,4), terrain #1: ", 
# test.setAgentState(testAgent, State.state((5,4), 1))
# print "testAgent State: ", test.getAgentState(testAgent)
# print "moving testAgent: "
# test.moveAgent(testAgent, test.getAgentState(testAgent), 'east')
# print test.getAgentState(testAgent)
# print ""
# print "Test get terrain type: ", test.getTerrainType(State.state((0, 9), 0))

