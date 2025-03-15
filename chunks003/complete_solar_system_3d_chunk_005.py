# Begin chunk 005 of 12 (3000 bytes max)
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
# End chunk 005 of 12 (3000 bytes max)
