# Begin chunk 001
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
                        'size': 10,
                        'orbital_period': 1.769,
                        'orbital_radius': 5.9,
                        'inclination': 0.04
                    },
                    'Europa': {
                        'color': 'white',
                        'size': 8,
                        'orbital_period': 3.551,
                        'orbital_radius': 9.4,
                        'inclination': 0.47
                    },
                    'Ganymede': {
                        'color': 'gray',
                        'size': 12,
                        'orbital_period': 7.155,
                        'orbital_radius': 15.0,
                        'inclination': 0.21
                    },
                    'Callisto': {
                        'color': 'darkgray',
                        'size': 11,
                        'orbital_period': 16.689,
                        'orbital_radius': 26.4,
                        'inclination': 0.51
                    }
                }
            },
            'Saturn': {
                'color': 'gold',
                'size': 55,
                'orbital_period': 29.46,
                'orbital_radius': 24,
                'inclination': 2.5,
                'moons': {
                    'Mimas': {
                        'color': 'gray',
                        'size': 3,
                        'orbital_period': 0.942,
                        'orbital_radius': 3.08,
                        'inclination': 1.53
                    },
                    'Enceladus': {
                        'color': 'white',
                        'size': 4,
                        'orbital_period': 1.370,
                        'orbital_radius': 3.95,
                        'inclination': 0.00
                    },
                    'Tethys': {
                        'color': 'gray',
                        'size': 5,
                        'orbital_period': 1.888,
                        'orbital_radius': 4.89,
                        'inclination': 1.09
                    },
                    'Dione': {
                        'color': 'lightgray',
                        'size': 5,
                        'orbital_period': 2.737,
                        'orbital_radius': 6.26,
                        'inclination': 0.02
                    },
                    'Rhea': {
                        'color': 'lightgray',
                        'size': 6,
                        'orbital_period': 4.518,
                        'orbital_radius': 8.74,
                        'inclination': 0.35
                    },
                    'Titan': {
                        'color': 'orange',
                        'size': 12,
                        'orbital_period': 15.945,
                        'orbital_radius': 20.27,
                        'inclination': 0.33
                    },
                    'Iapetus': {
                        'color': 'gray',
                        'size': 6,
                        'orbital_period': 79.321,
                        'orbital_radius': 59.02,
                        'inclination': 15.47
                    }
                }
            },
            'Uranus': {
                'color': 'lightblue',
                'size': 45,
                'orbital_period': 84.01,
                'orbital_radius': 48,
                'inclination': 0.8,
                'moons': {
                    'Miranda': {
                        'color': 'gray',
                        'size': 3,
                        'orbital_period': 1.413,
                        'orbital_radius': 5.08,
                        'inclination': 4.34
                    },
                    'Ariel': {
                        'color': 'lightgray',
                        'size': 4,
                        'orbital_period': 2.520,
                        'orbital_radius': 7.27,
                        'inclination': 0.04
                    },
                    'Umbriel': {
                        'color': 'darkgray',
                        'size': 4,
                        'orbital_period': 4.144,
                        'orbital_radius': 10.12,
                        'inclination': 0.13
                    },
                    'Titania': {
                        'color': 'gray',
                        'size': 5,
                        'orbital_period': 8.706,
                        'orbital_radius': 16.84,
                        'inclination': 0.08
                    },
                    'Oberon': {
                        'color': 'gray',
                        'size': 5,
                        'orbital_period': 13.463,
                        'orbital_radius': 22.75,
                        'inclination': 0.07
                    }
                }
            },
            'Neptune': {
                'color': 'blue',
                'size': 45,
                'orbital_period': 164.79,
                'orbital_radius': 75,
                'inclination': 1.8,
                'moons': {
                    'Naiad': {
                        'color': 'gray',
                        'size': 2,
                        'orbital_period': 0.294,
                        'orbital_radius': 3.18,
                        'inclination': 4.75
                    },
                    'Thalassa': {
                        'color': 'gray',
                        'size': 2,
                        'orbital_period': 0.311,
                        'orbital_radius': 3.32,
                        'inclination': 0.21
                    },
                    'Despina': {
                        'color': 'gray',
                        'size': 2,
                        'orbital_period': 0.335,
                        'orbital_radius': 3.51,
                        'inclination': 0.07
                    },
                    'Galatea': {
                        'color': 'gray',
# End chunk 001
