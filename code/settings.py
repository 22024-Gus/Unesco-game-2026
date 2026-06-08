import pygame
from pygame.math import Vector2 as vector
from sys import exit

WIN_WID, WIN_HGT = 960,800
TILE_SIZE = 32

COLOURS = { 
    'white': '#f4fefa',
    'pure white': '#ffffff',
    'dark': '#2b292c',
    'light': '#c8c8c8',
    'grey': '#3a373b',
                
}

'''WORLD_LAYERS = {
    'water': 0,
    'bg': 1,
    'shadow': 2,
    'main': 3,
    'top': 4,
}'''

tower_rules = {
    'timothy chalamet': {'land_ok': True, 'water_ok': False, 'snow_ok': False},
    'albert einstein': {'land_ok': True, 'water_ok': False, 'snow_ok': True},
    'nikola tesla': {'land_ok': True, 'water_ok': True, 'snow_ok': False}
}