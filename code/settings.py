import pygame
from pygame.math import Vector2 as vector
from sys import exit

WIN_WID, WIN_HGT = 960,720
TILE_SIZE = 64
ANIM_SPEED = 6
BATTLE_OUTLINE_WID = 4

COLOURS = { 
    'white': '#f4fefa',
    'pure white': '#ffffff',
    'dark': '#2b292c',
    'light': '#c8c8c8',
    'grey': '#3a373b',
                
}

WORLD_LAYERS = {
    'water': 0,
    'bg': 1,
    'shadow': 2,
    'main': 3,
    'top': 4,    
}

BATTLE_POSITIONS = {
}

BATTLE_LAYERS = {
}

BATTLE_CHOICES = {
}