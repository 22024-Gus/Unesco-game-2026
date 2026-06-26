import pygame 
from pygame.math import Vector2 as vector
from sys import exit
import random
''' ^^ imports ^^ '''

WIN_WID, WIN_HGT = 960,800 #window size
TILE_SIZE = 32 #tile size

tower_rules = { #rules for each tower. defines where each tower can be placed.
    'jesus christ': {'land_ok': True, 'water_ok': True, 'snow_ok': False},
    'albert einstein': {'land_ok': True, 'water_ok': False, 'snow_ok': True},
    'david attenborough': {'land_ok': True, 'water_ok': False, 'snow_ok': True},
    'michael jackson': {'land_ok': True, 'water_ok': False, 'snow_ok': False}
}

tower_info = { #stats for each tower. defines range, damage, and cooldown between attacks.
    'jesus christ': {'damage': 100, 'range': 20, 'cooldown': 10, 'cost': 500},
    'albert einstein': {'damage': 10, 'range': 3, 'cooldown': 0.5, 'cost': 150},
    'michael jackson': {'damage': 20, 'range': 5, 'cooldown': 1.5, 'cost': 100},
    'david attenborough': {'damage': 50, 'range': 5, 'cooldown': 3, 'cost': 200},
}

enemy_info = { #stats for enemy towers. defines speed and health.
    'jeff bezos': {'speed': 90, 'health': 48, 'reward': 50},
    'donald trump': {'speed': 40, 'health': 102, 'reward': 100}
}

enemy_waves = [ #defining the waves for the game.

    [('jeff bezos', 5)], #wave 1
    [('jeff bezos', 8), ('donald trump', 3)], #wave 2
    [('jeff bezos', 10), ('donald trump', 5), ('jeff bezos', 5)] #wave 3
]

particle_colours = [
    (235, 90, 90),
    (175, 20, 20),
    (240, 135, 110),
    (225, 80, 55),
    (215, 85, 105),
    (237, 190, 75) #secret gold colour
]