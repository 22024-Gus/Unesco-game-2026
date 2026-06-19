import pygame
from pygame.math import Vector2 as vector
from sys import exit

WIN_WID, WIN_HGT = 960,800
TILE_SIZE = 32

'''COLOURS = { 
    'white': '#f4fefa',
    'pure white': '#ffffff',
    'dark': '#2b292c',
    'light': '#c8c8c8',
    'grey': '#3a373b',
    #other colours, not using it rn though
}'''

tower_rules = {
    'timothy chalamet': {'land_ok': True, 'water_ok': False, 'snow_ok': False},
    'albert einstein': {'land_ok': True, 'water_ok': False, 'snow_ok': True},
    'nikola tesla': {'land_ok': True, 'water_ok': True, 'snow_ok': False}
}

tower_info = {
    'timothy chalamet': {'damage': 10, 'range': 3, 'cooldown': 0.33},
    'albert einstein': {'damage': 20, 'range': 10, 'cooldown': 1},
    'nikola tesla': {'damage': 50, 'range': 5, 'cooldown': 3},
}

enemy_info = {
    'jeff bezos': {'speed': 90, 'health': 50},
    'donald trump': {'speed': 40, 'health': 100}
}

enemy_waves = [

    [('jeff bezos', 5)], #wave 1
    [('jeff bezos', 8), ('donald trump', 3)], #wave 2
    [('jeff bezos', 10), ('donald trump', 5), ('jeff bezos', 5)] #wave 3
]