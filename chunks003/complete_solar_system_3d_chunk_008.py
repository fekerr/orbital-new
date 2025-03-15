# Begin chunk 008 of 12 (3000 bytes max)
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
# End chunk 008 of 12 (3000 bytes max)
