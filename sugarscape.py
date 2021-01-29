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

        # Group containing sprites for easy updating
        self.all_sprites = pg.sprite.Group()
        self.agents = pg.sprite.Group()
        self.reproductive_agents = pg.sprite.Group()
        self.cells = pg.sprite.Group()

        # Python dumb so index (y, x) instead of (x, y)
        self.map = []
        for y in range(GRIDHEIGHT):
            
            row = []
            
            for x in range(GRIDWIDTH):

                row.append(Cell(self, x, y))

            self.map.append(row)

        # Generate agents
        for n in range(NUMAGENTS + NUMREPAGENTS):
            # Spawn agents
            if n < NUMREPAGENTS:
                ReproductiveAgent(self)
            else:
                Agent(self)

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
        pg.display.set_caption(TITLE + f"; Agents: {str(len(self.agents.sprites()))}, ReAgents: {str(len(self.reproductive_agents.sprites()))}")

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
