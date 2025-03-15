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
                        'size': 3,
                        'orbital_period': 0.429,
                        'orbital_radius': 4.18,
                        'inclination': 0.05
                    },
                    'Larissa': {
                        'color': 'gray',
                        'size': 3,
                        'orbital_period': 0.555,
                        'orbital_radius': 4.97,
                        'inclination': 0.20
                    },
                    'Proteus': {
                        'color': 'darkgray',
                        'size': 4,
                        'orbital_period': 1.122,
                        'orbital_radius': 7.96,
                        'inclination': 0.08
                    },
                    'Triton': {
                        'color': 'pink',
                        'size': 8,
                        'orbital_period': 5.877,
                        'orbital_radius': 14.33,
                        'inclination': 156.885  # Retrograde orbit
                    },
                    'Nereid': {
                        'color': 'gray',
                        'size': 3,
                        'orbital_period': 360.13,
                        'orbital_radius': 222.65,
                        'inclination': 7.23
                    }
                }
            },
            'Pluto': {
                'color': 'brown',
                'size': 15,
                'orbital_period': 248.09,
                'orbital_radius': 79,
                'inclination': 17.16,
                'moons': {
                    'Charon': {
                        'color': 'gray',
                        'size': 7,
                        'orbital_period': 6.387,
                        'orbital_radius': 17.53,
                        'inclination': 0.001
                    },
                    'Nix': {
                        'color': 'gray',
                        'size': 2,
                        'orbital_period': 24.856,
                        'orbital_radius': 48.69,
                        'inclination': 0.133
                    },
                    'Hydra': {
                        'color': 'gray',
                        'size': 2,
                        'orbital_period': 38.206,
                        'orbital_radius': 64.74,
                        'inclination': 0.242
                    },
                    'Kerberos': {
                        'color': 'gray',
                        'size': 1,
                        'orbital_period': 32.168,
                        'orbital_radius': 57.78,
                        'inclination': 0.389
                    },
                    'Styx': {
                        'color': 'gray',
                        'size': 1,
                        'orbital_period': 20.162,
                        'orbital_radius': 42.65,
                        'inclination': 0.809
                    }
                }
            }
        }
    }


class SolarSystemAnimation3D:
    
    def __init__(self, style='default', elev=20, azim=45):
        # Set up the 3D figure
        plt.style.use(style)
        self.fig = plt.figure(figsize=(16, 9))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.elev = elev
        self.azim = azim
        
        # Extract settings from the new Config structure
        self.settings = Config.SETTINGS
        self.frames = self.settings['frames']
        self.camera_distance = self.settings['camera_distance']
        self.min_camera_distance = self.settings['min_camera_distance']
        self.max_camera_distance = self.settings['max_camera_distance']
        self.zoom_speed = self.settings['zoom_speed']
        self.base_speed = self.settings['base_speed']
        
        # Extract planet data
        self.planets = self.settings['planets']
        
        # Extract asteroid counts
        asteroid_counts = self.settings['asteroid_counts']
        self.num_asteroids = asteroid_counts['belt']
        self.num_hildas = asteroid_counts['hildas']
        self.num_trojans = asteroid_counts['trojans']
        self.num_kuiper = asteroid_counts['kuiper']
        self.num_inner_oort = asteroid_counts['inner_oort']
        self.num_outer_oort = asteroid_counts['outer_oort']
        
        # Initialize positions
        self.init_positions()
        
    def init_positions(self):
        # Initialize planet positions
        self.planet_positions = {planet: {'x': [], 'y': [], 'z': []} for planet in self.planets.keys()}
        self.moon_positions = {planet: {moon: {'x': [], 'y': [], 'z': []} 
                            for moon in properties['moons'].keys()} 
                            for planet, properties in self.planets.items()}
        
        # Initialize main belt asteroids
        self.belt_angles = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        self.belt_radii = np.random.uniform(5, 11, self.num_asteroids)
        self.belt_eccentricity = np.random.uniform(0.1, 0.3, self.num_asteroids)
        self.belt_inclination = np.random.uniform(-20, 20, self.num_asteroids)
        self.belt_phase = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        self.belt_ascending_nodes = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        
        # Initialize Hildas
        self.hilda_angles = []
        for angle in [0, 2*np.pi/3, 4*np.pi/3]:
            cluster_angles = np.random.normal(angle, 0.5, self.num_hildas//3)
            self.hilda_angles.extend(cluster_angles)
        self.hilda_angles = np.array(self.hilda_angles)
        jupiter_radius = self.planets['Jupiter']['orbital_radius']
        self.hilda_radii = np.random.normal(jupiter_radius * 0.8, 0.8, len(self.hilda_angles))
        self.hilda_inclination = np.random.uniform(-10, 10, len(self.hilda_angles))
        self.hilda_phase = np.random.uniform(0, 2*np.pi, len(self.hilda_angles))
        
        # Initialize Trojans
        self.trojan_angles1 = np.random.normal(np.pi/3, 0.4, self.num_trojans)
        self.trojan_angles2 = np.random.normal(5*np.pi/3, 0.4, self.num_trojans)
        self.trojan_radii = np.random.normal(jupiter_radius, 1.0, self.num_trojans)
        self.trojan_inclination = np.random.uniform(-15, 15, self.num_trojans)
        self.trojan_phase = np.random.uniform(0, 2*np.pi, self.num_trojans)
        
        # Initialize Kuiper Belt, Inner Oort Cloud, and Outer Oort Cloud positions
        # [Previous initialization code remains the same]
        self.kuiper_angles = np.random.uniform(0, 2*np.pi, self.num_kuiper)
        self.kuiper_radii = np.random.uniform(80, 120, self.num_kuiper)
        self.kuiper_inclination = np.random.uniform(-30, 30, self.num_kuiper)
        self.kuiper_eccentricity = np.random.uniform(0.1, 0.3, self.num_kuiper)
        self.kuiper_ascending_nodes = np.random.uniform(0, 2*np.pi, self.num_kuiper)
        
        # Initialize Inner Oort Cloud (Hills Cloud)
        self.inner_oort_phi = np.random.uniform(0, 2*np.pi, self.num_inner_oort)
        self.inner_oort_theta = np.random.normal(np.pi/2, 0.5, self.num_inner_oort)
        self.inner_oort_radii = np.random.power(0.7, self.num_inner_oort) * 18000 + 2000
        self.inner_oort_rotation = np.random.uniform(0, 2*np.pi, self.num_inner_oort)
        
        # Initialize Outer Oort Cloud
        self.outer_oort_phi = np.random.uniform(0, 2*np.pi, self.num_outer_oort)
        self.outer_oort_theta = np.arccos(2*np.random.uniform(0, 1, self.num_outer_oort) - 1)
        self.outer_oort_radii = np.random.power(0.5, self.num_outer_oort) * 80000 + 20000
        self.outer_oort_rotation = np.random.uniform(0, 2*np.pi, self.num_outer_oort)

    def update(self, frame):
        print(f"{frame}")
        self.ax.clear()
        
        # Calculate camera distance with smooth zoom
        self.camera_distance = self.max_camera_distance - (self.max_camera_distance - self.min_camera_distance) * (1 - np.exp(-self.zoom_speed * frame))
        speed_scale = max(0.1, (self.camera_distance / self.max_camera_distance) ** 0.3)
        current_speed = self.base_speed * speed_scale

        # Get Jupiter's planet angle for trojans/hildas
        jupiter_planet_angle = None
        for planet, properties in self.planets.items():
            if planet == 'Jupiter':
                angular_velocity = 2 * np.pi / properties['orbital_period']
                jupiter_planet_angle = -(current_speed * frame * angular_velocity)
                break

        # Update planet positions
        for planet, properties in self.planets.items():
            angular_velocity = 2 * np.pi / properties['orbital_period']
            planet_angle = -(current_speed * frame * angular_velocity)
            
            planet_x, planet_y, planet_z = self.calculate_3d_position(
                properties['orbital_radius'],
                planet_angle,
                properties['inclination']
            )
            self.planet_positions[planet]['x'] = planet_x
            self.planet_positions[planet]['y'] = planet_y
            self.planet_positions[planet]['z'] = planet_z
            
            # Update moon positions
            for moon, moon_props in properties['moons'].items():
                moon_period = moon_props['orbital_period'] / (365.25 * properties['orbital_period'])
                moon_angular_velocity = 2 * np.pi / moon_period
                moon_angle = -(current_speed * frame * moon_angular_velocity)
                
                moon_local_x, moon_local_y, moon_local_z = self.calculate_3d_position(
                    moon_props['orbital_radius'] * 0.01,
                    moon_angle,
                    moon_props['inclination']
                )
                
                self.moon_positions[planet][moon]['x'] = planet_x + moon_local_x
                self.moon_positions[planet][moon]['y'] = planet_y + moon_local_y
                self.moon_positions[planet][moon]['z'] = planet_z + moon_local_z

        # Draw orbital paths
        theta = np.linspace(0, 2*np.pi, 100)
        for planet, properties in self.planets.items():
            x, y, z = self.calculate_3d_position(
                properties['orbital_radius'],
                theta,
                properties['inclination']
            )
            opacity, _ = self.calculate_visibility((x, y, z), self.camera_distance)
            self.ax.plot(x, y, z, 'b-', alpha=opacity.mean() * 0.3)
            
            # Draw moon orbits
            planet_pos = self.planet_positions[planet]
            for moon, moon_props in properties['moons'].items():
                moon_x, moon_y, moon_z = self.calculate_3d_position(
                    moon_props['orbital_radius'] * 0.01,
                    theta,
                    moon_props['inclination']
                )
                moon_orbit_x = planet_pos['x'] + moon_x
                moon_orbit_y = planet_pos['y'] + moon_y
                moon_orbit_z = planet_pos['z'] + moon_z
                
                moon_opacity, _ = self.calculate_visibility(
                    (moon_orbit_x, moon_orbit_y, moon_orbit_z),
                    self.camera_distance
                )
                self.ax.plot(moon_orbit_x, moon_orbit_y, moon_orbit_z,
                            'gray', alpha=moon_opacity.mean() * 0.2, linewidth=0.5)

        # Calculate asteroid belt positions using Kepler's Third Law
# End chunk 001
