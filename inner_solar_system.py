import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.colors as mcolors

class SolarSystemAnimation:
    def __init__(self):
        # Set up the figure
        plt.style.use('default')
        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        
        # Orbital periods (relative to Jupiter = 1)
        self.periods = {
            'Mercury': 0.24,
            'Venus': 0.62,
            'Earth': 1.0,
            'Mars': 1.88,
            'Jupiter': 11.86
        }
        
        # Orbital radii
        self.radii = {
            'Mercury': 1,
            'Venus': 1.8,
            'Earth': 2.5,
            'Mars': 3.8,
            'Jupiter': 13
        }
        
        # Initialize asteroid populations
        self.num_asteroids = 1000
        self.num_hildas = 300
        self.num_trojans = 200
        
        # Initialize positions
        self.init_positions()
        
    def init_positions(self):
        # Initialize planet positions
        self.planet_positions = {}
        for planet in self.radii.keys():
            self.planet_positions[planet] = {'x': [], 'y': []}
        
        # Initialize main belt asteroids
        self.belt_angles = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        self.belt_radii = np.random.uniform(4.5, 11, self.num_asteroids)
        
        # Initialize Hildas (three clusters)
        self.hilda_angles = []
        for angle in [0, 2*np.pi/3, 4*np.pi/3]:
            cluster_angles = np.random.normal(angle, 0.3, self.num_hildas//3)
            self.hilda_angles.extend(cluster_angles)
        self.hilda_angles = np.array(self.hilda_angles)
        self.hilda_radii = np.random.normal(self.radii['Jupiter'] * 0.8, 0.3, len(self.hilda_angles))
        
        # Initialize Trojans (two clusters)
        self.trojan_angles1 = np.random.normal(np.pi/3, 0.2, self.num_trojans)
        self.trojan_angles2 = np.random.normal(5*np.pi/3, 0.2, self.num_trojans)
        self.trojan_radii = np.random.normal(self.radii['Jupiter'], 0.5, self.num_trojans)
        
    def update(self, frame):
        self.ax.clear()
        
        # Update planet positions
        for planet, radius in self.radii.items():
            period_factor = self.periods[planet]
            angle = (2 * np.pi * frame / (100 * period_factor)) % (2 * np.pi)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            self.planet_positions[planet]['x'] = x
            self.planet_positions[planet]['y'] = y
        
        # Draw orbital paths
        theta = np.linspace(0, 2*np.pi, 100)
        for radius in self.radii.values():
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            self.ax.plot(x, y, 'b-', alpha=0.1)
        
        # Update asteroid positions
        # Main belt - simple orbital motion
        belt_angles_update = self.belt_angles + frame * 0.02 / np.sqrt(self.belt_radii)
        belt_x = self.belt_radii * np.cos(belt_angles_update)
        belt_y = self.belt_radii * np.sin(belt_angles_update)
        
        # Jupiter's position affects Trojans and Hildas
        jupiter_angle = (2 * np.pi * frame / (100 * self.periods['Jupiter'])) % (2 * np.pi)
        
        # Update Hildas - maintain triangular formation relative to Jupiter
        hilda_angles_update = self.hilda_angles + jupiter_angle * 2/3  # 3:2 resonance
        hilda_x = self.hilda_radii * np.cos(hilda_angles_update)
        hilda_y = self.hilda_radii * np.sin(hilda_angles_update)
        
        # Update Trojans - maintain 60° ahead and behind Jupiter
        trojan_angles1_update = self.trojan_angles1 + jupiter_angle
        trojan_angles2_update = self.trojan_angles2 + jupiter_angle
        trojan_x1 = self.trojan_radii * np.cos(trojan_angles1_update)
        trojan_y1 = self.trojan_radii * np.sin(trojan_angles1_update)
        trojan_x2 = self.trojan_radii * np.cos(trojan_angles2_update)
        trojan_y2 = self.trojan_radii * np.sin(trojan_angles2_update)
        
        # Plot everything
        # Planets
        self.ax.scatter(0, 0, c='yellow', s=100)  # Sun
        for planet, pos in self.planet_positions.items():
            color = 'gray' if planet == 'Mercury' else 'orange' if planet in ['Venus', 'Jupiter'] else 'blue' if planet == 'Earth' else 'red'
            size = 60 if planet == 'Jupiter' else 30 if planet in ['Earth', 'Venus'] else 20
            self.ax.scatter(pos['x'], pos['y'], c=color, s=size)
            self.ax.text(pos['x'] + 0.2, pos['y'] + 0.2, planet, fontsize=8)
        
        # Asteroids
        self.ax.scatter(belt_x, belt_y, c='red', s=1, alpha=0.3)
        self.ax.scatter(hilda_x, hilda_y, c='purple', s=1, alpha=0.3)
        self.ax.scatter(trojan_x1, trojan_y1, c='green', s=1, alpha=0.3)
        self.ax.scatter(trojan_x2, trojan_y2, c='green', s=1, alpha=0.3)
        
        # Customize plot
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        self.ax.set_axis_off()
        self.ax.set_title(f'Solar System Animation - Frame {frame}', pad=20)
        
    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=500, 
                           interval=50, blit=False)
        plt.show()
        
    def save(self, filename):
        anim = FuncAnimation(self.fig, self.update, frames=500, interval=50, blit=False)
        anim.save(filename, writer=PillowWriter(fps=20))
        print(f"Animation saved as {filename}")

# Create and run the animation
solar_system = SolarSystemAnimation()
solar_system.save("solar_system_asteroid.gif")
solar_system.animate()
