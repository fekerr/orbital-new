# Begin chunk 001 of 12 (3000 bytes max)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from matplotlib.animation import FFMpegWriter
import os

OS_PATH = os.path.dirname(os.path.realpath('__file__'))

class Config:
    SETTINGS = {
        'frames': 3000,
        'camera_distance': 100,
        'min_camera_distance': 3,
        'max_camera_distance': 100000,
        'zoom_speed': 0.0075,
        'base_speed': 0.2,
        'asteroid_counts': {
            'belt': 2000,
            'hildas': 300,
            'trojans': 300,
            'kuiper': 4000,
            'inner_oort': 40000,
            'outer_oort': 60000,
        },
        'planets': {
            'Mercury': {
                'color': 'gray',
                'size': 20,
                'orbital_period': 0.24,
                'orbital_radius': 1,
                'inclination': 7.0,
                'moons': {}  # Mercury has no moons
            },
            'Venus': {
                'color': 'orange',
                'size': 30,
                'orbital_period': 0.62,
                'orbital_radius': 1.8,
                'inclination': 3.4,
                'moons': {}  # Venus has no moons
            },
            'Earth': {
                'color': 'blue',
                'size': 30,
                'orbital_period': 1.0,
                'orbital_radius': 2.5,
                'inclination': 0.0,
                'moons': {
                    'Moon': {
                        'color': 'gray',
                        'size': 8,  # Relative to Earth
                        'orbital_period': 27.32,  # In Earth days
                        'orbital_radius': 30.3,   # In Earth radii
                        'inclination': 5.145      # Degrees relative to Earth's equator
                    }
                }
            },
            'Mars': {
                'color': 'red',
                'size': 25,
                'orbital_period': 1.88,
                'orbital_radius': 3.8,
                'inclination': 1.9,
                'moons': {
                    'Phobos': {
                        'color': 'gray',
                        'size': 2,
                        'orbital_period': 0.319,
                        'orbital_radius': 4.76,
                        'inclination': 1.093
                    },
                    'Deimos': {
                        'color': 'gray',
                        'size': 1,
                        'orbital_period': 1.263,
                        'orbital_radius': 12.92,
                        'inclination': 0.93
                    }
                }
            },
            'Jupiter': {
                'color': 'orange',
                'size': 60,
                'orbital_period': 11.86,
                'orbital_radius': 13,
                'inclination': 1.3,
                'moons': {
                    'Io': {
                        'color': 'yellow',
# End chunk 001 of 12 (3000 bytes max)
