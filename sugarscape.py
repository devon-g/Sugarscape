import pygame as pg
import random
import sys
from settings import *
from sprites import *


class Sugarscape:

    def __init__(self):

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def new(self):
        #random.seed(1)

        # Python dumb so index (y, x) instead of (x, y)
        self.map = []
        for y in range(GRIDHEIGHT):
            row = []
            for x in range(GRIDWIDTH):
                sugar_max = random.randint(1, 20)
                row.append({
                    'sugar_current': random.randint(0, sugar_max),
                    'sugar_max': sugar_max,
                    'regen_rate': random.random(),
                    'agent': None,
                    'coordinates': (x, y)
                })
            self.map.append(row)

        # Group containing all sprites for easy updating
        self.all_sprites = pg.sprite.Group()

        na = 20 # Number of agents
        nra = 5 # Number of reproductive agents

        # Generate agents
        for n in range(na + nra):
            # Initial agent coords
            x = random.randint(0, GRIDWIDTH - 1)
            y = random.randint(0, GRIDHEIGHT - 1)

            # Check if agent is already present at coords
            while self.map[y][x]['agent'] is not None:
                x = random.randint(0, GRIDWIDTH - 1)
                y = random.randint(0, GRIDHEIGHT - 1)

            # Spawn agents
            if n < nra:
                ReproductiveAgent(self, x, y)
            else:
                Agent(self, x, y)


    def run(self):

        self.paused = False
        self.running = True

        while self.running:

            self.clock.tick(FPS)
            self.events()

            if ~self.paused:
                self.update()
                self.draw()

    def quit(self):

        pg.quit()
        sys.exit()

    def update(self):
        # Update sprites.
        self.all_sprites.update()
        pg.display.set_caption(TITLE + f"; Agents Alive: {str(len(self.all_sprites.sprites()))}")

        # Update sugar
        for y in range(GRIDHEIGHT):
            for x in range(GRIDWIDTH):
                self.map[y][x]['sugar_current'] = min(self.map[y][x]['sugar_current'] + self.map[y][x]['regen_rate'], self.map[y][x]['sugar_max'])

    def draw_grid(self):

        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):

        self.screen.fill(DARKGREY)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:
                    self.paused = ~self.paused

                if event.key == pg.K_ESCAPE:
                    self.quit()


scape = Sugarscape()
while True:
    scape.new()
    scape.run()
