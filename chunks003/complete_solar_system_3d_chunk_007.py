# Begin chunk 007 of 12 (3000 bytes max)
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
# End chunk 007 of 12 (3000 bytes max)
