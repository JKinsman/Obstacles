####
#
# Graphics
# Jake Kinsman
# 11/28/2014
#
####

import pygame, sys
from pygame.locals import *
import state as State
victors = list()
victorPositions = list()

def simulation(results, race):
	randomAgentMovements = results[0]
	adpAgentMovements = results[1]
	tdAgentMovements = results[2]
	randomAgentScores = results[3]
	adpAgentScores = results[4]
	tdAgentScores = results[5]

	pygame.init()
	pygame.time.set_timer(USEREVENT + 1, 500)
	completedRace = False
	surface = pygame.display.set_mode((1440, 850), 0, 32)
	pygame.display.set_caption('Relay Race')
	for i in range(3):
		drawEnvironment(surface, race, i, results)
def drawEnvironment(windowSurface, race, worldNum, results):
	tdAgent = getAgentImage('td', race.tdRaceOrder[worldNum])
	randomAgent = getAgentImage('random', race.randomRaceOrder[worldNum])
	adpAgent = getAgentImage('adp', race.adpRaceOrder[worldNum])
	grass = pygame.image.load("grass.png")
	grass = pygame.transform.scale(grass, (144, 70))
	water = pygame.image.load("water.png")
	water = pygame.transform.scale(water, (144, 70))
	mountain = pygame.image.load("mountain.jpg")
	mountain = pygame.transform.scale(mountain, (144, 70))
	forest = pygame.image.load("forest.png")
	forest = pygame.transform.scale(forest, (144, 70))
	sky = pygame.image.load("background.jpg")
	sky = pygame.transform.scale(sky, (1440, 850))
	platform = pygame.image.load("platform.tiff")
	platform = pygame.transform.scale(platform, (100, 50))
	font = pygame.font.SysFont("monospace", 25, True, False)
	start = font.render("START", 1, (0,0,0), (255, 255, 255))
	finish = font.render("FINISH", 1, (0,0,0), (255, 255, 255))
	move = 0
	while not(move > len(results[0][worldNum]) and move > len(results[1][worldNum]) and move > len(results[2][worldNum])):
	    randomAgentState = results[0][worldNum][min([move, len(results[0][worldNum]) - 1])]
	    adpAgentState = results[1][worldNum][min([move, len(results[1][worldNum]) - 1])]
	    tdAgentState = results[2][worldNum][min([move, len(results[2][worldNum]) - 1])]
	    for event in pygame.event.get():
	        if event.type == QUIT:
	            pygame.quit()
	            sys.exit()
	        windowSurface.blit(sky, (0,0))
	    	if event.type == USEREVENT + 1:
	    		for i in range(len(race.world.terrains[worldNum].terrainWorld)):
	        		for j in range(len(race.world.terrains[worldNum].terrainWorld)):
	        			position = ((144 * j), ((70 * i) + 150))
	        			if repr(race.world.terrains[worldNum].terrainWorld[i][j]) == 'grass':
	        				windowSurface.blit(grass, position)
	        			elif repr(race.world.terrains[worldNum].terrainWorld[i][j]) == 'water':
	        				windowSurface.blit(water, position)
	        			elif repr(race.world.terrains[worldNum].terrainWorld[i][j]) == 'forest':
	        				windowSurface.blit(forest, position)
	        			else:
	        				windowSurface.blit(mountain, position)        
	    		windowSurface.blit(platform, (0, 60))
	    		windowSurface.blit(platform, (100, 60))
	    		windowSurface.blit(platform, (200, 60))
	    		windowSurface.blit(platform, (570, 60))
	    		windowSurface.blit(platform, (670, 60))
	    		windowSurface.blit(platform, (770, 60))
	    		windowSurface.blit(platform, (1140, 60))
	    		windowSurface.blit(platform, (1240, 60))
	    		windowSurface.blit(platform, (1340, 60))
	    		windowSurface.blit(tdAgent, stateToCoordinates(tdAgentState ,'td', worldNum))
	    		windowSurface.blit(adpAgent, stateToCoordinates(adpAgentState ,'adp', worldNum))
	    		windowSurface.blit(randomAgent, stateToCoordinates(randomAgentState ,'random', worldNum))
	    		windowSurface.blit(start, stateToCoordinates(State.state((0,9), worldNum), None, worldNum))
	    		windowSurface.blit(finish, stateToCoordinates(State.state((9,0), worldNum), None, worldNum))
	    		if worldNum > 0:
	    			for _, winner in enumerate(victors[0]):
	    				windowSurface.blit(winner, victorPositions[0][_])
	    			if worldNum is 2:
	    				for _, winner in enumerate(victors[1]):
	    					windowSurface.blit(winner, victorPositions[1][_])

	    		pygame.display.flip()
	    		move += 1
	victors.append([tdAgent, adpAgent, randomAgent])
	victorPositions.append([stateToCoordinates(State.state((float("inf"), float("inf")), worldNum), 'td', worldNum), 
		stateToCoordinates(State.state((float("inf"), float("inf")), worldNum), 'adp', worldNum), 
		stateToCoordinates(State.state((float("inf"), float("inf")), worldNum), 'random', worldNum)])

def getAgentImage(agentType, index):

	image = None
	if agentType == 'random':
		if index == 0:
			image = pygame.image.load("mario.png")
		elif index == 1:
			image = pygame.image.load("luigi.png")
		else:
			image = pygame.image.load("bowser.png")
	elif agentType == 'td':
		if index == 0:
			image = pygame.image.load("jake.jpg")
		elif index == 1:
			image = pygame.image.load("willie.jpg")
		else:
			image = pygame.image.load("matt.jpg")
	else:
		if index == 0:
			image = pygame.image.load("fred.jpg")
		elif index == 1:
			image = pygame.image.load("karen.jpg")
		else:
			image = pygame.image.load("jim.jpg")
	image = pygame.transform.scale(image, (60, 60))
	return image

def stateToCoordinates(state, typeAgent, worldNum):
	offset = 0
	if state.getPosition() == (float("inf"), float("inf")):
		if typeAgent is 'td':
			offset = 20
		elif typeAgent is 'adp':
			offset = 120
		else:
			offset = 220
		if worldNum is 1:
			offset += 570
		elif worldNum is 2:
			offset += 1140
		return(offset, 0)
	else:
		if type is "adp":
			offset = 44
		if type is "random":
			offset = 84

	x, y = state.getPosition()
	return (((144 * x) + offset), ((70 * y) + 150))








