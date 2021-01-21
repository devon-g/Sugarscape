import pygame as pg
import random
from settings import *


class Agent(pg.sprite.Sprite):

    def __init__(self, sugarscape, x, y):

        self.groups = sugarscape.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.sugarscape = sugarscape
        self.image = pg.Surface((TILESIZE - 1, TILESIZE - 1))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.vision = random.randint(1, 7)
        self.metabolism = random.uniform(1, 4)
        self.sugar = random.uniform(0, self.metabolism*2)
        self.sugar_max = self.sugar

        self.x = x
        self.y = y

        self.sugarscape.map[self.y][self.x]['agent'] = self
        self.eat()

    def look(self):

        # I hate vanilla 2darrays
        north = [self.sugarscape.map[max(0, self.y - dy)][self.x] for dy in range(1, self.vision + 1)]
        south = [self.sugarscape.map[min(GRIDHEIGHT - 1, self.y + dy)][self.x] for dy in range(1, self.vision + 1)]
        east = [self.sugarscape.map[self.y][min(GRIDWIDTH - 1, self.x + dx)] for dx in range(1, self.vision + 1)]
        west = [self.sugarscape.map[self.y][max(0, self.x - dx)] for dx in range(1, self.vision + 1)]
        directions = [north, south, east, west]
        random.shuffle(directions)
        # Flatten directions into cells
        cells = [cell for direction in directions for cell in direction]

        # Search for cell with most sugar
        best_cell = cells[0]
        best_val = cells[0]['sugar_current']
        for cell in cells:
            if cell['sugar_current'] > best_val and cell['agent'] is None:
                best_cell = cell
                best_val = cell['sugar_current']

        # Return old cell to new cell displacement
        return best_cell['coordinates'][0] - self.x, best_cell['coordinates'][1] - self.y

    def move(self, dx=0, dy=0):

        # Clear current agent global coordinates
        self.sugarscape.map[self.y][self.x]['agent'] = None

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
        self.sugarscape.map[self.y][self.x]['agent'] = self

    def eat(self):
        # Eat entire contents of cell sugar
        self.sugar += self.sugarscape.map[self.y][self.x]['sugar_current']
        self.sugarscape.map[self.y][self.x]['sugar_current'] = 0

    def update(self):

        # Exist
        dx, dy = self.look()
        self.move(dx, dy)
        self.sugar -= self.metabolism

        # If Agent sugar level at or below 0, Agent starves to death.
        if self.sugar <= 0:
            self.sugar = 0
            self.sugarscape.map[self.y][self.x]['agent'] = None
            self.sugarscape.all_sprites.remove(self)

        self.eat()

        if self.sugar >= self.sugar_max:
            self.sugar_max = self.sugar

        # Update sprite location and color
        r = int((1 - (self.sugar / self.sugar_max)) * 255)
        g = int(self.sugar / self.sugar_max * 255)
        b = 0
        self.image.fill((r, g, b))

        self.rect.x = self.x * TILESIZE + 1
        self.rect.y = self.y * TILESIZE + 1


class ReproductiveAgent(Agent):

    def __init__(self, sugarscape, x, y):

        Agent.__init__(self, sugarscape, x, y)
        self.reproduce_threshold = 1.5 * self.metabolism

    def reproduce(self):

        if self.sugar >= self.reproduce_threshold:

            north = self.sugarscape.map[max(0, self.y - 1)][self.x]
            south = self.sugarscape.map[min(GRIDHEIGHT - 1, self.y + 1)][self.x]
            east = self.sugarscape.map[self.y][min(GRIDWIDTH - 1, self.x + 1)]
            west = self.sugarscape.map[self.y][max(0, self.x - 1)]
            directions = [north, south, east, west]
            random.shuffle(directions)

            for d in directions:
                if d['agent'] is None:
                    random.choice([Agent(self.sugarscape, d['coordinates'][0], d['coordinates'][1]), ReproductiveAgent(self.sugarscape, d['coordinates'][0], d['coordinates'][1])])
                    return

    def update(self):

        Agent.update(self)
        self.reproduce()

        r = int((1 - (self.sugar / self.sugar_max)) * 255)
        g = 0
        b = int(self.sugar / self.sugar_max * 255)
        self.image.fill((r, g, b))


class Cell(pg.sprite.Sprite):

    def __init__(self):

        pass

    def update(self):

        r = max(40, int(self.sugar / self.sugar_max * 255))
        g = max(40, int(self.sugar / self.sugar_max * 255))
        b = max(40, int(self.sugar / self.sugar_max * 255))
        self.image.fill((r, g, b))