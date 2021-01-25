import pygame as pg
import random
from settings import *


class Agent(pg.sprite.Sprite):

    def __init__(self, sugarscape, x = None, y = None):
        # Pygame sprite stuff
        if type(self) == Agent:
            self.groups_list = [sugarscape.all_sprites, sugarscape.agents]
        pg.sprite.Sprite.__init__(self, self.groups_list)
        self.image = pg.Surface((TILESIZE - 10, TILESIZE - 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        print(self, sugarscape)
        # Sugarscape agent stuff
        self.sugarscape = sugarscape
        self.vision = random.randint(1, 7)
        self.metabolism = random.uniform(1, 4)
        self.sugar = random.uniform(0, self.metabolism*2)
        self.sugar_max = self.sugar

        self.x = x
        self.y = y

        # Generate coordinates if not specified during init.
        if self.x is None or self.y is None:
            
            self.x = random.randint(0, GRIDWIDTH - 1)
            self.y = random.randint(0, GRIDHEIGHT - 1)

            while self.sugarscape.map[self.y][self.x].agentPresent():

                self.x = random.randint(0, GRIDWIDTH - 1)
                self.y = random.randint(0, GRIDHEIGHT - 1)

        self.rect.x = self.x * TILESIZE + 5
        self.rect.y = self.y * TILESIZE + 5

        self.sugarscape.map[self.y][self.x].setAgent(self)
        self.eat()

    def look(self):

        # I hate sublist 2darrays
        north = [self.sugarscape.map[(self.y - dy) % GRIDHEIGHT][self.x] for dy in range(1, self.vision + 1)]
        south = [self.sugarscape.map[(self.y + dy) % GRIDHEIGHT][self.x] for dy in range(1, self.vision + 1)]
        east = [self.sugarscape.map[self.y][(self.x + dx) % GRIDWIDTH] for dx in range(1, self.vision + 1)]
        west = [self.sugarscape.map[self.y][(self.x - dx) % GRIDWIDTH] for dx in range(1, self.vision + 1)]
        current = [self.sugarscape.map[self.y][self.x]]
        directions = [north, south, east, west, current]
        random.shuffle(directions)
        # Flatten directions into cells
        cells = [cell for direction in directions for cell in direction]

        # Search for cell with most sugar
        best_cell = cells[0]
        best_val = cells[0].getSugar()
        for cell in cells:
            if cell.getSugar() > best_val and cell.agentPresent() is False:
                best_cell = cell
                best_val = cell.getSugar()

        # Return old cell to new cell displacement
        cellx, celly = best_cell.getCoords()
        return cellx - self.x, celly - self.y

    def move(self, dx=0, dy=0):

        # Clear current agent global coordinates
        self.sugarscape.map[self.y][self.x].delAgent()

        # Update local coordinates
        self.x += dx
        self.y += dy

        # Wrap around
        if self.x >= GRIDWIDTH:
            self.x = self.x - GRIDWIDTH
        if self.x < 0:
            self.x = GRIDWIDTH + self.x
        if self.y >= GRIDHEIGHT:
            self.y = self.y - GRIDHEIGHT
        if self.y < 0:
            self.y = GRIDHEIGHT + self.y

        # Set new agent global coordinates
        self.sugarscape.map[self.y][self.x].setAgent(self)

    def eat(self):
        # Eat entire contents of cell sugar
        self.sugar += self.sugarscape.map[self.y][self.x].getSugar()
        self.sugarscape.map[self.y][self.x].sugarEaten()

    def update(self):

        # Exist
        dx, dy = self.look()
        self.move(dx, dy)
        self.sugar -= self.metabolism

        # If Agent sugar level at or below 0, Agent starves to death.
        if self.sugar <= 0:
            self.sugar = 0
            self.kill()

            self.sugarscape.map[self.y][self.x].delAgent()

        self.eat()

        if self.sugar >= self.sugar_max:
            self.sugar_max = self.sugar

        # Update sprite location and color
        r = int((1 - (self.sugar / self.sugar_max)) * 255)
        g = int(self.sugar / self.sugar_max * 255)
        b = 0
        self.image.fill((r, g, b))

        self.rect.x = self.x * TILESIZE + 5
        self.rect.y = self.y * TILESIZE + 5


class ReproductiveAgent(Agent):

    def __init__(self, sugarscape, x = None, y = None):

        self.groups_list = [sugarscape.all_sprites, sugarscape.reproductive_agents]
        self.reproduce_threshold = 10
        Agent.__init__(self, sugarscape, x, y)

    def reproduce(self):

        if self.sugar >= self.reproduce_threshold:

            north = self.sugarscape.map[(self.y - 1) % GRIDHEIGHT][self.x]
            south = self.sugarscape.map[(self.y + 1) % GRIDHEIGHT][self.x]
            east = self.sugarscape.map[self.y][(self.x + 1) % GRIDWIDTH]
            west = self.sugarscape.map[self.y][(self.x - 1) % GRIDWIDTH]
            directions = [north, south, east, west]
            random.shuffle(directions)

            for d in directions:
                if ~d.agentPresent():
                    x, y = d.getCoords()
                    child = Agent(self.sugarscape, x, y)
                    print(child.groups())
                    print(child.x, child.y)
                    print(child.rect.x, child.rect.y)
                    #random.choice([Agent(self.sugarscape, x, y), ReproductiveAgent(self.sugarscape, x, y)])
                    return

    def update(self):

        Agent.update(self)
        self.reproduce()

        r = int((1 - (self.sugar / self.sugar_max)) * 255)
        g = 0
        b = int(self.sugar / self.sugar_max * 255)
        self.image.fill((r, g, b))


class Cell(pg.sprite.Sprite):

    def __init__(self, sugarscape, x, y):

        self.groups_list = [sugarscape.all_sprites, sugarscape.cells]
        pg.sprite.Sprite.__init__(self, self.groups_list)
        self.sugarscape = sugarscape
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        self.sugar_max = random.randint(1, 20)
        self.sugar = random.randint(0, self.sugar_max)
        self.regen_rate = random.random()
        self.agent = None
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def getSugar(self):
        
        return self.sugar

    def getSugarMax(self):
        
        return self.sugar_max

    def sugarEaten(self):
        
        self.sugar = 0

    def setAgent(self, agent):

        self.agent = agent
    
    def delAgent(self):

        self.agent = None

    def agentPresent(self):
        
        if self.agent is None:
            present = False
        else:
            present = True
        
        return present

    def getCoords(self):

        return self.x, self.y

    def sugarRegen(self):
        
        self.sugar = min(self.sugar + self.regen_rate, self.sugar_max)

    def update(self):

        self.sugarRegen()

        r = max(40, int(self.sugar / self.sugar_max * 255))
        g = max(40, int(self.sugar / self.sugar_max * 255))
        b = max(40, int(self.sugar / self.sugar_max * 255))
        self.image.fill((r, g, b))
