# Begin chunk 004
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
# End chunk 004
