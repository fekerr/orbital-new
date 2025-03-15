# Begin chunk 010 of 12 (3000 bytes max)
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
# End chunk 010 of 12 (3000 bytes max)
