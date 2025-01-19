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
    
    def __init__(self, style='default'):
        # Set up the 3D figure
        plt.style.use(style)
        self.fig = plt.figure(figsize=(16, 9))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
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
        belt_orbital_period = np.sqrt(self.belt_radii ** 3)
        belt_velocities = 2 * np.pi / belt_orbital_period
        belt_angles_update = self.belt_angles - current_speed * frame * belt_velocities
        
        belt_radii_update = self.belt_radii * (1 + self.belt_eccentricity * np.cos(belt_angles_update))
        belt_x, belt_y, belt_z = self.calculate_3d_position(
            belt_radii_update,
            belt_angles_update,
            self.belt_inclination,
            self.belt_ascending_nodes
        )
        
        # Hildas at 2:3 resonance with Jupiter
        hilda_angles_update = self.hilda_angles + jupiter_planet_angle * (2/3)
        hilda_x, hilda_y, hilda_z = self.calculate_3d_position(
            self.hilda_radii,
            hilda_angles_update,
            self.hilda_inclination
        )
        
        # Trojans at Jupiter's L4 and L5 points
        trojan_x1, trojan_y1, trojan_z1 = self.calculate_3d_position(
            self.trojan_radii,
            self.trojan_angles1 + jupiter_planet_angle,
            self.trojan_inclination
        )
        trojan_x2, trojan_y2, trojan_z2 = self.calculate_3d_position(
            self.trojan_radii,
            self.trojan_angles2 + jupiter_planet_angle,
            self.trojan_inclination
        )
        
        # Kuiper Belt with proper Keplerian motion
        kuiper_orbital_period = np.sqrt(self.kuiper_radii ** 3)
        kuiper_velocities = 2 * np.pi / kuiper_orbital_period
        kuiper_angles_update = self.kuiper_angles - current_speed * frame * kuiper_velocities
        
        kuiper_radii_update = self.kuiper_radii * (1 + self.kuiper_eccentricity * np.cos(kuiper_angles_update))
        kuiper_x, kuiper_y, kuiper_z = self.calculate_3d_position(
            kuiper_radii_update,
            kuiper_angles_update,
            self.kuiper_inclination,
            self.kuiper_ascending_nodes
        )
        
        # Calculate visibilities
        belt_opacity, belt_size = self.calculate_visibility((belt_x, belt_y, belt_z), self.camera_distance)
        hilda_opacity, hilda_size = self.calculate_visibility((hilda_x, hilda_y, hilda_z), self.camera_distance)
        trojan_opacity1, trojan_size1 = self.calculate_visibility((trojan_x1, trojan_y1, trojan_z1), self.camera_distance)
        trojan_opacity2, trojan_size2 = self.calculate_visibility((trojan_x2, trojan_y2, trojan_z2), self.camera_distance)
        kuiper_opacity, kuiper_size = self.calculate_visibility((kuiper_x, kuiper_y, kuiper_z), self.camera_distance)
        
        # Calculate Oort Cloud positions with much slower motion
        inner_orbital_period = np.sqrt(self.inner_oort_radii ** 3)
        inner_velocities = 2 * np.pi / inner_orbital_period
        inner_angles = self.inner_oort_rotation - current_speed * frame * inner_velocities * 0.001
        
        inner_x = self.inner_oort_radii * np.sin(self.inner_oort_theta) * np.cos(self.inner_oort_phi + inner_angles)
        inner_y = self.inner_oort_radii * np.sin(self.inner_oort_theta) * np.sin(self.inner_oort_phi + inner_angles)
        inner_z = self.inner_oort_radii * np.cos(self.inner_oort_theta)
        
        outer_orbital_period = np.sqrt(self.outer_oort_radii ** 3)
        outer_velocities = 2 * np.pi / outer_orbital_period
        outer_angles = self.outer_oort_rotation - current_speed * frame * outer_velocities * 0.0005
        
        outer_x = self.outer_oort_radii * np.sin(self.outer_oort_theta) * np.cos(self.outer_oort_phi + outer_angles)
        outer_y = self.outer_oort_radii * np.sin(self.outer_oort_theta) * np.sin(self.outer_oort_phi + outer_angles)
        outer_z = self.outer_oort_radii * np.cos(self.outer_oort_theta)
        
        inner_opacity, inner_size = self.calculate_visibility(
            (inner_x, inner_y, inner_z),
            self.camera_distance,
            max_distance=100000
        )
        outer_opacity, outer_size = self.calculate_visibility(
            (outer_x, outer_y, outer_z),
            self.camera_distance,
            max_distance=100000
        )
        
        # Plot everything
        self.ax.scatter([0], [0], [0], c='yellow', s=100)  # Sun
        
        # Plot planets and moons
        for planet, pos in self.planet_positions.items():
            properties = self.planets[planet]
            planet_opacity, planet_size = self.calculate_visibility(
                (pos['x'], pos['y'], pos['z']),
                self.camera_distance
            )
            
            self.ax.scatter(pos['x'], pos['y'], pos['z'],
                        c=properties['color'],
                        s=properties['size'] * planet_size[0],
                        alpha=planet_opacity[0])
            
            if planet_opacity[0] > 0.3:
                self.ax.text(pos['x'], pos['y'], pos['z'], planet, fontsize=8)
            
            for moon, moon_props in properties['moons'].items():
                moon_pos = self.moon_positions[planet][moon]
                moon_opacity, moon_size = self.calculate_visibility(
                    (moon_pos['x'], moon_pos['y'], moon_pos['z']),
                    self.camera_distance
                )
                
                self.ax.scatter(moon_pos['x'], moon_pos['y'], moon_pos['z'],
                            c=moon_props['color'],
                            s=moon_props['size'] * moon_size[0],
                            alpha=moon_opacity[0])
        
        # Plot asteroid populations
        self.ax.scatter(belt_x, belt_y, belt_z, c='gray', s=1 * belt_size, alpha=belt_opacity)
        self.ax.scatter(hilda_x, hilda_y, hilda_z, c='gray', s=1 * hilda_size, alpha=hilda_opacity)
        self.ax.scatter(trojan_x1, trojan_y1, trojan_z1, c='gray', s=1 * trojan_size1, alpha=trojan_opacity1)
        self.ax.scatter(trojan_x2, trojan_y2, trojan_z2, c='gray', s=1 * trojan_size2, alpha=trojan_opacity2)
        self.ax.scatter(kuiper_x, kuiper_y, kuiper_z, c='gray', s=1 * kuiper_size, alpha=kuiper_opacity)
        
        # Plot Oort Clouds
        self.ax.scatter(inner_x, inner_y, inner_z,
                    c='lightblue', s=0.8 * inner_size, alpha=inner_opacity * 0.4,
                    label='Hills Cloud')
        self.ax.scatter(outer_x, outer_y, outer_z,
                    c='lightgray', s=0.5 * outer_size, alpha=outer_opacity * 0.3,
                    label='Outer Oort Cloud')
        
        # Update view limits
        max_radius = max(self.outer_oort_radii.max(), self.inner_oort_radii.max())
        limit = self.camera_distance * (1 + np.log10(max_radius / self.camera_distance))
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_zlim(-limit, limit)
        self.ax.set_axis_off()
        
        plt.subplots_adjust(left=-.5, bottom=-2, right=1.5, top=3, wspace=None, hspace=None)
        self.ax.view_init(elev=20, azim=45)
        self.ax.set_title('Complete Solar System Animation', pad=20)

        
    def calculate_oort_positions(self, frame):
        """Calculate positions for both Inner and Outer Oort Cloud objects"""
        # Inner Oort Cloud (Hills Cloud) - slightly faster motion
        inner_angular_velocity = 0.00002 / np.sqrt(self.inner_oort_radii)
        inner_angles = self.inner_oort_rotation + self.base_speed * frame * inner_angular_velocity
        
        inner_x = self.inner_oort_radii * np.sin(self.inner_oort_theta) * np.cos(self.inner_oort_phi + inner_angles)
        inner_y = self.inner_oort_radii * np.sin(self.inner_oort_theta) * np.sin(self.inner_oort_phi + inner_angles)
        inner_z = self.inner_oort_radii * np.cos(self.inner_oort_theta)
        
        # Outer Oort Cloud - slower motion
        outer_angular_velocity = 0.00001 / np.sqrt(self.outer_oort_radii)
        outer_angles = self.outer_oort_rotation + self.base_speed * frame * outer_angular_velocity
        
        outer_x = self.outer_oort_radii * np.sin(self.outer_oort_theta) * np.cos(self.outer_oort_phi + outer_angles)
        outer_y = self.outer_oort_radii * np.sin(self.outer_oort_theta) * np.sin(self.outer_oort_phi + outer_angles)
        outer_z = self.outer_oort_radii * np.cos(self.outer_oort_theta)
        
        return (inner_x, inner_y, inner_z), (outer_x, outer_y, outer_z)
        
    def calculate_3d_position(self, radius, angle, inclination, ascending_node=0):
        # Convert inclination to radians
        incl_rad = np.radians(inclination)
        
        # Calculate position in orbital plane
        # Let sine and cosine handle the periodicity naturally
        x_orbit = radius * np.cos(angle)
        y_orbit = radius * np.sin(angle)
        
        # Apply inclination and ascending node rotation
        x = (x_orbit * np.cos(ascending_node) - 
            y_orbit * np.cos(incl_rad) * np.sin(ascending_node))
        y = (x_orbit * np.sin(ascending_node) + 
            y_orbit * np.cos(incl_rad) * np.cos(ascending_node))
        z = y_orbit * np.sin(incl_rad)
        
        return x, y, z
    
    def calculate_visibility(self, positions, camera_distance, max_distance=50):
        """Calculate opacity based on distance from camera"""
        # Calculate camera position that rotates with the view
        azim = np.radians(45)  # Match the view_init azimuth
        elev = np.radians(20)  # Match the view_init elevation
        
        x = camera_distance * np.cos(elev) * np.sin(azim)
        y = camera_distance * np.cos(elev) * np.cos(azim)
        z = camera_distance * np.sin(elev)
        
        camera_pos = np.array([x, y, z])
        
        if isinstance(positions[0], np.ndarray):
            points = np.vstack((positions[0], positions[1], positions[2])).T
        else:
            points = np.array([[positions[0], positions[1], positions[2]]])
            
        distances = np.linalg.norm(points - camera_pos, axis=1)
        
        # Calculate opacity based on distance
        max_opacity = 0.8
        min_opacity = 0.0
        opacity = np.clip(max_opacity * (1 - distances/max_distance), min_opacity, max_opacity)
        
        # Add distance-based size scaling
        size_scale = np.clip(1.5 * (1 - distances/max_distance), 0.2, 1.0)
        
        return opacity, size_scale
        
    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=self.frames, interval=50, blit=False)
        plt.show()
        
    def save(self, filename):
        anim = FuncAnimation(self.fig, self.update, frames=self.frames, interval=50, blit=False)
        self.fig.set_size_inches(16, 9)
        self.fig.set_dpi(100)
        anim.save(filename, writer=PillowWriter(fps=20))
        print(f"Animation saved as {filename}")
        
    def save1080p(self, filename):
        """
        Save the animation in 1080p resolution (1920x1080) using H.264 codec
        
        Parameters:
        filename (str): The output filename (should end in .mp4 or .mov)
        """
        anim = FuncAnimation(self.fig, self.update, frames=self.frames, interval=50, blit=False)
        self.fig.set_size_inches(16, 9)  # 16:9 aspect ratio
        self.fig.set_dpi(120)  # 1920/16 = 120 DPI for 1080p
        writer = FFMpegWriter(fps=30, codec='h264', bitrate=8000)
        anim.save(filename, writer=writer)
        print(f"Animation saved as {filename}")

    def save4k(self, filename):
        anim = FuncAnimation(self.fig, self.update, frames=self.frames, interval=50, blit=False)
        self.fig.set_size_inches(16, 9)
        self.fig.set_dpi(240)
        writer = FFMpegWriter(fps=30, codec='h264')
        anim.save(filename, writer=writer)
        print(f"Animation saved as {filename}")



styles = {'light': 'default', 'dark': 'dark_background'}
for version, style in styles.items():
    solar_system = SolarSystemAnimation3D(style=style)
    
    filename = os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}.gif")
    # solar_system.save(filename)
    
    filename = os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}_1080p.mp4")
    solar_system.save1080p(filename)
    
    filename = os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}_4k.mov")
    solar_system.save4k(filename)
    # solar_system.animate()
