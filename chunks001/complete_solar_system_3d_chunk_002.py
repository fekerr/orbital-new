# Begin chunk 002
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
# End chunk 002
