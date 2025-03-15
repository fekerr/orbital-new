# Begin chunk 006 of 12 (3000 bytes max)
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
# End chunk 006 of 12 (3000 bytes max)
