####
#
# Relay Race
# Jake Kinsman
# 11/28/2014
#
####

import terrain as Terrain
import state as State
import agent as Agent
import gameworld as Gameworld
import graphics as Graphics

import copy
import random
from collections import defaultdict

class testAgent(Agent.randomAgent):
        def __init__(self, *args):
                super(testAgent, self).__init__()
                self.type = "adp"
#               print self.type

Agent.adpAgent = testAgent
class relayRace(object):
	
	def __init__(self):
		self.world = Gameworld.gameWorld()
		self.highScores = defaultdict(lambda: 0)
		self.tdRaceOrder = list()
		self.adpRaceOrder = list()
		self.randomRaceOrder = list()

		# Every possible (state,action,nextState) tuple
		transitions = []
		for j in range(3):
			for k in range(10):
				for l in range(10):
					curState = State.state((k, l), j)
					curState.setTerrainType(self.world.getTerrainType(curState))
					for action in self.world.getActions(curState):
						for nextState in self.world.getAllPossibleSuccessors(curState, action):
							if nextState.getPosition() != (float("inf"), float("inf")):
								nextState.setTerrainType(self.world.getTerrainType(nextState))
							transitions.append( (curState, action, nextState) )

		for i in range(3):
			# Each team has equal skills (apples to apples comparison)
			skills = { k:(random.random() + .5)  for  k   in  ['water','grass','forest','mountain'] }
			self.world.addAgent(Agent.adpAgent(self.world, transitions), skills)
			self.world.addAgent(Agent.tdAgent((9,0))                   , skills)
			self.world.addAgent(Agent.randomAgent()                    , skills)
	
	#tested
	def trainAgents(self, numIter):
		for index, terrain in enumerate(self.world.terrains):

			for training in range(numIter):
                                print training
				for tdAgent in self.world.tdAgents:
					self.world.setAgentState(tdAgent, self.world.getStartState(index))
					movements = list()
					score = 0
                                        i = 0
					while not self.world.completedRace(self.world.getAgentState(tdAgent), index):
						oldState = self.world.getAgentState(tdAgent)
#                                                if not i % 5000:
#                                                        print i, oldState.getPosition()
                                                i += 1
						terrainType = self.world.getTerrainType(oldState)
						oldState.setTerrainType(terrainType)
						actions = self.world.getActions(self.world.getAgentState(tdAgent))
						action = tdAgent.chooseAction(actions, oldState, terrainType)
						self.world.moveAgent(tdAgent, self.world.getAgentState(tdAgent), action)
						newState = self.world.getAgentState(tdAgent)
						if newState.getPosition() != (float("inf"), float("inf")):
							newState.setTerrainType(self.world.getTerrainType(newState))
						reward = self.world.getReward(tdAgent, oldState)
						movements.append(self.world.getAgentState(tdAgent))
                                                nextActions = self.world.getActions(self.world.getAgentState(tdAgent))
						tdAgent.update(oldState, terrainType, action, newState, reward, nextActions)
					for ind, state in enumerate(movements):
						if self.world.completedRace(state, 0):
							score += (self.world.transitionalReward * (self.world.discount ** ind))
						elif self.world.completedRace(state, 2):
							score += (self.world.terminalReward * (self.world.discount ** ind))
						else:
							score += (self.world.getReward(tdAgent, state) * (self.world.discount ** ind))
                                        #print score
					if score > self.highScores[(tdAgent.type, tdAgent.index, index)]:
						self.highScores[(tdAgent.type, tdAgent.index, index)] = score

				for adpAgent in self.world.adpAgents:
                                        continue
					self.world.setAgentState(adpAgent, self.world.getStartState(index))
					movements = list()
					score = 0
					while not self.world.completedRace(self.world.getAgentState(adpAgent), index):
						oldState = self.world.getAgentState(adpAgent)
						terrainType = self.world.getTerrainType(oldState)
						oldState.setTerrainType(terrainType)
						actions = self.world.getActions(self.world.getAgentState(adpAgent))
						action = adpAgent.chooseAction(oldState)
						self.world.moveAgent(adpAgent, self.world.getAgentState(adpAgent), action)
						newState = self.world.getAgentState(adpAgent)
						if newState.getPosition() != (float("inf"), float("inf")):
							newState.setTerrainType(self.world.getTerrainType(newState))
						reward = self.world.getReward(adpAgent, oldState)
						movements.append(self.world.getAgentState(adpAgent))
						adpAgent.update(oldState, terrainType, action, newState, reward)
					for ind, state in enumerate(movements):
						if self.world.completedRace(state, 0):
							score += (self.world.transitionalReward * (self.world.discount ** ind))
						elif self.world.completedRace(state, 2):
							score += (self.world.terminalReward * (self.world.discount ** ind))
						else:
							score += (self.world.getReward(adpAgent, state) * (self.world.discount ** ind))
					if score > self.highScores[(adpAgent.type, adpAgent.index, index)]:
						self.highScores[(adpAgent.type, adpAgent.index, index)] = score

				for randomAgent in self.world.randomAgents:
					self.world.setAgentState(randomAgent, self.world.getStartState(index))
					movements = list()
					score = 0
					while not self.world.completedRace(self.world.getAgentState(randomAgent), index):
						actions = self.world.getActions(self.world.getAgentState(randomAgent))
						action = randomAgent.chooseAction(actions)
						self.world.moveAgent(randomAgent, self.world.getAgentState(randomAgent), action)
						movements.append(self.world.getAgentState(randomAgent))
						randomAgent.update()
					for ind, state in enumerate(movements):
						if self.world.completedRace(state, 0):
							score += (self.world.transitionalReward * (self.world.discount ** ind))
						elif self.world.completedRace(state, 2):
							score += (self.world.terminalReward * (self.world.discount ** ind))
						else:
							score += (self.world.getReward(randomAgent, state) * (self.world.discount ** ind))
					#print score
					if score > self.highScores[(randomAgent.type, randomAgent.index, index)]:
						self.highScores[(randomAgent.type, randomAgent.index, index)] = score
	#tested
	def arrangeTeam(self):
		
		adpHighScore, adpArrangement = 0, list()
		tdHighScore, tdArrangement = 0, list()
		randomHighScore, randomArrangement = 0, list()

		for i, agentI in enumerate(self.world.adpAgents):
			for j, agentJ in enumerate(self.world.adpAgents):
				for k, agentK in enumerate(self.world.adpAgents):
					####
					if i != j and j != k and i != k:
						agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
						agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
						agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
						score = agentIScore + agentJScore + agentKScore
						if score > adpHighScore:
							adpHighScore = score
							adpArrangement = [i, j, k]

                print adpHighScore
		for i, agentI in enumerate(self.world.tdAgents):
			for j, agentJ in enumerate(self.world.tdAgents):
				for k, agentK in enumerate(self.world.tdAgents):
					####
					if i != j and j != k and i != k:
						agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
						agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
						agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
						score = agentIScore + agentJScore + agentKScore
						if score > tdHighScore:
							tdHighScore = score
							tdArrangement = [i, j, k]

		
		for i, agentI in enumerate(self.world.randomAgents):
			for j, agentJ in enumerate(self.world.randomAgents):
				for k, agentK in enumerate(self.world.randomAgents):
					####
					if i != j and j != k and i != k:
						agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
						agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
						agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
						score = agentIScore + agentJScore + agentKScore
						if score > randomHighScore:
							randomHighScore = score
							randomArrangement = [i, j, k]
		
		self.adpRaceOrder = adpArrangement
		self.tdRaceOrder = tdArrangement
		self.randomRaceOrder = randomArrangement
		print "adp: ", adpArrangement, adpHighScore
		print "td: ", tdArrangement, tdHighScore
		print "random: ", randomArrangement, randomHighScore

	#tested
	def race(self):
		
		randomStates = list()
		adpStates = list()
		tdStates = list()
		randomScores = list()
		adpScores = list()
		tdScores = list()
		
		#Race Random Agents
		for index, agentRef in enumerate(self.randomRaceOrder):
                        print "hi"
			racingAgentMovements = list()
			racingAgent = self.world.getWorldAgent(self.world.randomAgents[agentRef])
			self.world.setAgentState(racingAgent, self.world.getStartState(index))
			while not self.world.completedRace(self.world.getAgentState(racingAgent), index):
				oldState = self.world.getAgentState(racingAgent)
				terrainType = self.world.getTerrainType(oldState)
				oldState.setTerrainType(terrainType)
				actions = self.world.getActions(self.world.getAgentState(racingAgent))
				action = racingAgent.chooseAction(actions)
				self.world.moveAgent(racingAgent, self.world.getAgentState(racingAgent), action)
				racingAgentMovements.append(self.world.getAgentState(racingAgent))
			randomStates.append(racingAgentMovements)
			score = 0
			for ind, state in enumerate(racingAgentMovements):
				if self.world.completedRace(state, 0):
					score += (self.world.transitionalReward * (self.world.discount ** ind))
				elif self.world.completedRace(state, 2):
					score += (self.world.terminalReward * (self.world.discount ** ind))
				else:
					score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
			randomScores.append(score)

		#Race ADP Agents
		for index, agentRef in enumerate(self.adpRaceOrder):
                        print "hi3"
			racingAgentMovements = list()
			racingAgent = self.world.getWorldAgent(self.world.adpAgents[agentRef])
			racingAgent.setEpsilon(0.001)
			self.world.setAgentState(racingAgent, self.world.getStartState(index))
			while not self.world.completedRace(self.world.getAgentState(racingAgent), index):
				oldState = self.world.getAgentState(racingAgent)
				terrainType = self.world.getTerrainType(oldState)
				oldState.setTerrainType(terrainType)
				actions = self.world.getActions(self.world.getAgentState(racingAgent))
				action = racingAgent.chooseAction(oldState)
				#print oldState, '\t', action
				self.world.moveAgent(racingAgent, self.world.getAgentState(racingAgent), action)
				racingAgentMovements.append(self.world.getAgentState(racingAgent))
			adpStates.append(racingAgentMovements)
			score = 0
			for ind, state in enumerate(racingAgentMovements):
				if self.world.completedRace(state, 0):
					score += (self.world.transitionalReward * (self.world.discount ** ind))
				elif self.world.completedRace(state, 2):
					score += (self.world.terminalReward * (self.world.discount ** ind))
				else:
					score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
			adpScores.append(score)

		#Race TD Agents
		for index, agentRef in enumerate(self.tdRaceOrder):
                        print "hi2"
			racingAgentMovements = list()
			racingAgent = self.world.getWorldAgent(self.world.tdAgents[agentRef])
			self.world.setAgentState(racingAgent, self.world.getStartState(index))
			while not self.world.completedRace(self.world.getAgentState(racingAgent), index):
				oldState = self.world.getAgentState(racingAgent)
				terrainType = self.world.getTerrainType(oldState)
				oldState.setTerrainType(terrainType)
				actions = self.world.getActions(self.world.getAgentState(racingAgent))
				action = racingAgent.chooseAction(actions, oldState, terrainType)
				self.world.moveAgent(racingAgent, self.world.getAgentState(racingAgent), action)
				racingAgentMovements.append(self.world.getAgentState(racingAgent))
			tdStates.append(racingAgentMovements)
			score = 0
			for ind, state in enumerate(racingAgentMovements):
				if self.world.completedRace(state, 0):
					score += (self.world.transitionalReward * (self.world.discount ** ind))
				elif self.world.completedRace(state, 2):
					score += (self.world.terminalReward * (self.world.discount ** ind))
				else:
					score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
			tdScores.append(score)

		return [randomStates, adpStates, tdStates, randomScores, adpScores, tdScores], self

a = relayRace()
print ""
print "TRAINING AGENTS..."
print ""
a.trainAgents(100)


'''
# display Policy
for i in range(3):
    print 'agent: ', i
    for j in range(3):

        for k in range(10):
            for l in range(10):
                print '%7s' % a.world.adpAgents[i].solver.getAction(State.state((l,k),j)),
            print
        print '\n\n'
    print '\n\n\n'
'''


a.arrangeTeam()



'''
# display Terrain
for i in range(3):
    for j in range(10):
        for k in range(10):
            print '%10s' % a.world.getTerrainType(State.state((k,j),i)),
        print
    print '\n\n'
'''

'''
# display Skills
print 'tdAgents'
for world in a.tdRaceOrder:
    print '\t', a.world.tdAgents[world].skillLevels
print

print 'adpAgents'
for world in a.adpRaceOrder:
    print '\t', a.world.adpAgents[world].skillLevels
print

print 'randomAgents'
for world in a.randomRaceOrder:
    print '\t', a.world.randomAgents[world].skillLevels
print

#exit()
'''

print "\nRACING AGENTS..."
print ""
results, race = a.race()
print "First RAND AGENT: \t", results[0][0][len(results[0][0]) - 1], "\t", results[3][0]
print "Second RAND AGENT: \t", results[0][1][len(results[0][1]) - 1], "\t", results[3][1]
print "Third RAND AGENT: \t", results[0][2][len(results[0][2]) - 1], "\t", results[3][2]
print ""
print "First ADP AGENT: \t", results[1][0][len(results[1][0]) - 1], "\t", results[4][0]
print "Second ADP AGENT: \t", results[1][1][len(results[1][1]) - 1], "\t", results[4][1]
print "Third ADP AGENT: \t", results[1][2][len(results[1][2]) - 1], "\t", results[4][2]
print ""
print "First TD AGENT: \t", results[2][0][len(results[2][0]) - 1], "\t", results[5][0]
print "Second TD AGENT: \t", results[2][1][len(results[2][1]) - 1], "\t", results[5][1]
print "Third TD AGENT: \t", results[2][2][len(results[2][2]) - 1], "\t", results[5][2]
print ""
print "BEGINNING SIMULATION:"
print ""
Graphics.simulation(results, race)
