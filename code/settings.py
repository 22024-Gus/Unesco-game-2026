import pygame 
from pygame.math import Vector2 as vector
from sys import exit
''' ^^ imports ^^ '''

WIN_WID, WIN_HGT = 960,800 #window size
TILE_SIZE = 32 #tile size

tower_rules = { #rules for each tower. defines where each tower can be placed.
    'timothy chalamet': {'land_ok': True, 'water_ok': False, 'snow_ok': False},
    'albert einstein': {'land_ok': True, 'water_ok': False, 'snow_ok': True},
    'nikola tesla': {'land_ok': True, 'water_ok': True, 'snow_ok': False}
}

tower_info = { #stats for each tower. defines range, damage, and cooldown between attacks.
    'timothy chalamet': {'damage': 10, 'range': 4, 'cooldown': 0.33},
    'albert einstein': {'damage': 20, 'range': 7, 'cooldown': 1},
    'nikola tesla': {'damage': 50, 'range': 3, 'cooldown': 3},
}

enemy_info = { #stats for enemy towers. defines speed and health.
    'jeff bezos': {'speed': 90, 'health': 50},
    'donald trump': {'speed': 40, 'health': 100}
}

enemy_waves = [ #defining the waves for the game.

    [('jeff bezos', 5)], #wave 1
    [('jeff bezos', 8), ('donald trump', 3)], #wave 2
    [('jeff bezos', 10), ('donald trump', 5), ('jeff bezos', 5)] #wave 3
]