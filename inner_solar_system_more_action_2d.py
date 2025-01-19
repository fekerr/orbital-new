import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.colors as mcolors
from matplotlib.animation import FFMpegWriter
import os

OS_PATH = os.path.dirname(os.path.realpath('__file__'))

class SolarSystemAnimation:
    def __init__(self, style='default'):
        # Set up the figure
        plt.style.use(style)
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
        
        # Initialize main belt asteroids with more dynamic properties
        self.belt_angles = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        self.belt_radii = np.random.uniform(4.5, 11, self.num_asteroids)
        self.belt_eccentricity = np.random.uniform(0, 0.15, self.num_asteroids)
        self.belt_inclination = np.random.uniform(-0.1, 0.1, self.num_asteroids)
        self.belt_phase = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        # New parameters for enhanced belt movement
        self.belt_oscillation = np.random.uniform(0.1, 0.3, self.num_asteroids)
        self.belt_oscillation_freq = np.random.uniform(0.01, 0.03, self.num_asteroids)
        self.belt_radial_variation = np.random.uniform(0.2, 0.4, self.num_asteroids)
        
        # Initialize Hildas with more dynamic movement
        self.hilda_angles = []
        for angle in [0, 2*np.pi/3, 4*np.pi/3]:
            cluster_angles = np.random.normal(angle, 0.3, self.num_hildas//3)
            self.hilda_angles.extend(cluster_angles)
        self.hilda_angles = np.array(self.hilda_angles)
        self.hilda_radii = np.random.normal(self.radii['Jupiter'] * 0.8, 0.3, len(self.hilda_angles))
        self.hilda_oscillation = np.random.uniform(0.1, 0.3, len(self.hilda_angles))
        self.hilda_phase = np.random.uniform(0, 2*np.pi, len(self.hilda_angles))
        
        # Initialize Trojans with libration
        self.trojan_angles1 = np.random.normal(np.pi/3, 0.2, self.num_trojans)
        self.trojan_angles2 = np.random.normal(5*np.pi/3, 0.2, self.num_trojans)
        self.trojan_radii = np.random.normal(self.radii['Jupiter'], 0.5, self.num_trojans)
        self.trojan_libration = np.random.uniform(0.05, 0.15, self.num_trojans)
        self.trojan_phase = np.random.uniform(0, 2*np.pi, self.num_trojans)
        
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
        
        # Update main belt asteroids with enhanced dynamic movement
        belt_angles_update = self.belt_angles + frame * 0.02 / np.sqrt(self.belt_radii)
        
        # Combine multiple movement patterns
        # 1. Eccentric orbits
        eccentric_radii = self.belt_radii * (1 + self.belt_eccentricity * np.cos(belt_angles_update))
        
        # 2. Radial oscillation
        radial_oscillation = self.belt_radial_variation * np.sin(frame * self.belt_oscillation_freq + self.belt_phase)
        dynamic_radii = eccentric_radii + radial_oscillation
        
        # 3. Vertical oscillation with varying frequencies
        belt_z = self.belt_inclination * np.sin(belt_angles_update * 2 + self.belt_phase)
        
        # 4. Additional orbital perturbation
        orbital_perturbation = self.belt_oscillation * np.cos(frame * 0.03 + self.belt_phase)
        
        # Combine all movements
        belt_x = dynamic_radii * np.cos(belt_angles_update + orbital_perturbation)
        belt_y = dynamic_radii * np.sin(belt_angles_update + orbital_perturbation)
        belt_y += belt_z
        
        # Jupiter's position affects Trojans and Hildas
        jupiter_angle = (2 * np.pi * frame / (100 * self.periods['Jupiter'])) % (2 * np.pi)
        
        # Update Hildas with oscillating movement
        base_hilda_speed = 0.005  # Base orbital speed for Hildas
        hilda_angles_update = (self.hilda_angles + 
                             frame * base_hilda_speed + # Add basic orbital motion
                             jupiter_angle * 2/3)       # Keep resonance with Jupiter
        
        # Add oscillation to create the triangular pattern
        oscillation = self.hilda_oscillation * np.sin(frame * 0.1 + self.hilda_phase)
        hilda_radii_dynamic = self.hilda_radii + oscillation
        
        # Calculate positions
        hilda_x = hilda_radii_dynamic * np.cos(hilda_angles_update)
        hilda_y = hilda_radii_dynamic * np.sin(hilda_angles_update)
        
        # Update Trojans with libration
        libration1 = self.trojan_libration * np.sin(frame * 0.05 + self.trojan_phase)
        libration2 = self.trojan_libration * np.sin(frame * 0.05 + self.trojan_phase + np.pi)
        trojan_angles1_update = self.trojan_angles1 + jupiter_angle + libration1
        trojan_angles2_update = self.trojan_angles2 + jupiter_angle + libration2
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
        
        # Asteroids with varying opacity based on vertical position and radial oscillation
        belt_opacity = 0.3 + 0.2 * (belt_z / np.max(np.abs(belt_z))) + 0.1 * (radial_oscillation / np.max(np.abs(radial_oscillation)))
        belt_opacity = np.clip(belt_opacity, 0.1, 0.8)
        self.ax.scatter(belt_x, belt_y, c='red', s=1, alpha=belt_opacity)
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
        anim = FuncAnimation(self.fig, self.update, frames=2000, 
                           interval=50, blit=False)
        plt.show()
        
    def save(self, filename):
        anim = FuncAnimation(self.fig, self.update, frames=2000, interval=50, blit=False)
        anim.save(filename, writer=PillowWriter(fps=20))
        print(f"Animation saved as {filename}")

    def save4k(self, filename):
        anim = FuncAnimation(self.fig, self.update, frames=2000, interval=50, blit=False)
        
        # Set up the figure for 4K export while maintaining aspect ratio
        self.fig.set_size_inches(16, 9)  # Set to 16:9 ratio
        self.fig.set_dpi(240)  # 240 DPI * 16 inches = 3840 pixels wide
        
        writer = FFMpegWriter(fps=30, codec='h264')
        anim.save(filename, writer=writer)
        print(f"Animation saved as {filename}")

styles = {'light': 'default', 'dark': 'dark_background'}
for version, style in styles.items():
    solar_system = SolarSystemAnimation(style=style)
    filename = os.path.join(OS_PATH, f"output/inner_solar_system_more_action_{version}.mov")
    solar_system.save4k(filename)
    filename = os.path.join(OS_PATH, f"output/inner_solar_system_more_action_{version}.gif")
    solar_system.save(filename)
    #solar_system.animate()
