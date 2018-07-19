#! /usr/bin/env python

import os
import random
import pygame
import math

death = 0

# Class for the orange dude
class Player(object):
    
    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)

    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

        
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Enemy(object):

    def __init__(self, pos, movetype, ang=0):
        self.ang = ang
        self.r = 40
        self.movetype = movetype
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.rect.center = (pos[0], pos[1])
        self.startx = self.rect.centerx
        self.starty = self.rect.centery
        enemies.append(self)

    def move(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy
    
    def spin(self):
        self.rect.centerx = math.cos(self.ang) * self.r + self.startx
        self.rect.centery = math.sin(self.ang) * self.r + self.starty
        self.ang += 0.05


# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("The World's Easiest Game!")
screen = pygame.display.set_mode((688, 240))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
enemies = []
player = Player() # Create the player

count = 0 
speed = 3
reps = 35

# Holds the level layout in a list of strings.
level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W                                         W",
"W                   U                     W",
"W                                         W",
"W                                         W",
"W                                         W",
"W                   U                     W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWH   W",
"WE                                        W",
"W                                         W",
"W                                         W",
"W          C                   C          W",
"W                                         W",
"W                                         W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "C":
            Enemy((x, y), 'r')
            Enemy((x, y), 'r', math.pi/2)
            Enemy((x, y), 'r', math.pi)
            Enemy((x, y), 'r', 3*math.pi/2)
        if col == "U":
            Enemy((x, y), 'u')
        if col == "H":
            Enemy((x, y), 'h')
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 96)
        x += 16
    y += 16
    x = 0

running = True
while running:
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-3, 0)
    if key[pygame.K_RIGHT]:
        player.move(3, 0)
    if key[pygame.K_UP]:
        player.move(0, -3)
    if key[pygame.K_DOWN]:
        player.move(0, 3)
    
    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        raise SystemExit("You win!")

    
    for enemy in enemies:
        if enemy.movetype == 'u':
            enemy.move(0, speed)
        elif enemy.movetype == 'h':
            enemy.move(speed, 0)
        elif enemy.movetype == 'r':
            enemy.spin()
        if player.rect.colliderect(enemy.rect):
            player.rect = pygame.Rect(32, 32, 16, 16)
            death += 1
            print(f"You died {death} time(s)!")
    
    count += 1
    
    if count >= reps:
        speed *= -1
        count = 0
    
    # Draw the scene
    screen.fill((255, 255, 255))
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall.rect)
    for enemy in enemies:
        pygame.draw.circle(screen, (0, 0, 255), enemy.rect.center, 8)
    pygame.draw.rect(screen, (0, 255, 50), end_rect)
    pygame.draw.rect(screen, (255, 0, 0), player.rect)
    pygame.display.flip()
