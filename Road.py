from config import *
import random
import pygame



class Road():

    def __init__(self):
        self.road = [-1]*cells
        self.screen = None
        self.clock = None
        self.globalDensity = 0
        self.globalFlow = 0
        self.passingSteps = 0

    def initialise(self):
        print(noCars)
        for i in range(int(noCars)):
            index = random.randint(0, cells - 1)

            while(self.road[index] != -1):
                index = random.randint(0, cells)
            self.road[index] = random.randint(0, vMax)

    def accelerate(self):
        for i in range(cells):
            if (self.road[i] != -1 and self.road[i] < vMax):
                self.road[i] += 1

    def braking(self):
        for i in range(cells - 1):
            if (self.road[i] != -1):
                currentVelocity = self.road[i]
                distance = 0
                for j in range(0, currentVelocity):
                    if (i + j + 1 >= cells):
                        self.road[i] = -1
                    else:
                        if (self.road[i + j + 1] == -1):
                            distance +=1
                        else:
                            break
                print("cell no ", i, "velcity ", currentVelocity, "distance: ", distance)
                if (currentVelocity >= distance):
                    self.road[i] = distance

    def randomisation(self):
        for i in range(cells):
            if (random.random() <= probability and self.road[i] > 0):
                self.road[i] -= 1

    def driving(self):
        currentPosition = 0
        while (currentPosition < cells):
            if (self.road[currentPosition] != -1 and self.road[currentPosition] != 0):
                print("drive cell: ", currentPosition)
                distance = self.road[currentPosition]
                if (distance + currentPosition < cells):
                    self.road[distance + currentPosition] = distance
                self.road[currentPosition] = -1
                currentPosition += distance + 1
            else:
                currentPosition += 1
            print("road: ", self.road)

    def initialiseGui(self):
        pygame.init()
        self.clock = pygame.time.Clock() #set no of frames
        self.screen = pygame.display.set_mode([screenWidth, screenHeight])

    def drawBorders(self):
        pygame.draw.line(self.screen, yellow, (0, 100), (1200, 100), 10)
        pygame.draw.line(self.screen, yellow, (0, 300), (1200, 300), 10)

    def drawCars(self):
        for i in range(cells):
            if (self.road[i] != -1):
                if (self.road[i] == 0):
                    # currently doesn t work, might fix later
                    pygame.draw.rect(self.screen, red, pygame.Rect((screenWidth/cells)*i, 200, cellSize, cellSize))
                else:
                    pygame.draw.rect(self.screen, green, pygame.Rect((screenWidth/cells)*i, 200, cellSize, cellSize))

    def run(self):
        self.initialise()
        print("init: ", self.road)

        self.initialiseGui()
        #global density = (no of vehicles)/(no of sites)
        self.globalDensity = noCars/cells
        loop = True
        #global flow = (no of vehicles passing a point)/(no of time steps)
        #current time step
        t = 0
        while loop and  t < 25:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            self.screen.fill((0, 0, 0))
            self.accelerate()
            print("acce: ", self.road)
            self.braking()
            print("brak: ", self.road)
            self.randomisation()
            print("rand: ", self.road)
            self.driving()
            print("driv: ", self.road)
            msElapsed = self.clock.tick(frames)
            self.drawCars()
            self.drawBorders()

            pygame.display.flip()

            t = t + 1  #passing time

        self.printResults(t)


    def printResults(self, time):
        f = open("results.txt", "a")
        f.write("global density: ")
        f.write(str(self.globalDensity))
        f.write('\n')
        f.write("time passed: ")
        f.write(str(time))
        f.write('\n')
        f.close()




