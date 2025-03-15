# Begin chunk 009 of 12 (3000 bytes max)
        
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
# End chunk 009 of 12 (3000 bytes max)
