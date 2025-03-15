# Begin chunk 002
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
        self.ax.view_init(elev=self.elev, azim=self.azim)
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
    # Default 3D Perspective
    solar_system = SolarSystemAnimation3D(style=style, elev=20, azim=45)
    solar_system.save(os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}.gif"))
    solar_system.save1080p(os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}_1080p.mp4"))
    solar_system.save4k(os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}_4k.mov"))
    #solar_system.animate()

    # Top-Down View
    solar_system_top_down = SolarSystemAnimation3D(style=style, elev=90, azim=0)
    solar_system_top_down.save(os.path.join(OS_PATH, f"output/complete_solar_system_3d_top_down_{version}.gif"))
    solar_system_top_down.save1080p(os.path.join(OS_PATH, f"output/complete_solar_system_3d_top_down_{version}_1080p.mp4"))
    solar_system_top_down.save4k(os.path.join(OS_PATH, f"output/complete_solar_system_3d_top_down_{version}_4k.mov"))
    #solar_system_top_down.animate()
# End chunk 002
