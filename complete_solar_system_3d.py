import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from matplotlib.animation import FFMpegWriter
import os

OS_PATH = os.path.dirname(os.path.realpath('__file__'))

class SolarSystemAnimation3D:
    def __init__(self, style='default'):
        # Set up the 3D figure
        plt.style.use(style)
        self.fig = plt.figure(figsize=(12, 12))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Orbital periods (relative to Earth = 1)
        self.periods = {
            'Mercury': 0.24,
            'Venus': 0.62,
            'Earth': 1.0,
            'Mars': 1.88,
            'Jupiter': 11.86,
            'Saturn': 29.46,
            'Uranus': 84.01,
            'Neptune': 164.79
        }
        
        # Orbital radii (AU, scaled down for visualization)
        self.radii = {
            'Mercury': 1,
            'Venus': 1.8,
            'Earth': 2.5,
            'Mars': 3.8,
            'Jupiter': 13,
            'Saturn': 24,
            'Uranus': 48,
            'Neptune': 75
        }
        
        # Orbital inclinations (degrees)
        self.inclinations = {
            'Mercury': 7.0,
            'Venus': 3.4,
            'Earth': 0.0,
            'Mars': 1.9,
            'Jupiter': 1.3,
            'Saturn': 2.5,
            'Uranus': 0.8,
            'Neptune': 1.8
        }
        
        # Planet colors and sizes
        self.planet_properties = {
            'Mercury': {'color': 'gray', 'size': 20},
            'Venus': {'color': 'orange', 'size': 30},
            'Earth': {'color': 'blue', 'size': 30},
            'Mars': {'color': 'red', 'size': 25},
            'Jupiter': {'color': 'orange', 'size': 60},
            'Saturn': {'color': 'gold', 'size': 55},
            'Uranus': {'color': 'lightblue', 'size': 45},
            'Neptune': {'color': 'blue', 'size': 45}
        }
        
        # Initialize asteroid populations
        self.num_asteroids = 1000
        self.num_hildas = 300
        self.num_trojans = 200
        self.num_kuiper = 500  # Added Kuiper Belt objects
        
        # Initialize positions
        self.init_positions()
        
    def init_positions(self):
        # Initialize planet positions
        self.planet_positions = {}
        for planet in self.radii.keys():
            self.planet_positions[planet] = {'x': [], 'y': [], 'z': []}
        
        # Initialize main belt asteroids
        self.belt_angles = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        self.belt_radii = np.random.uniform(4.5, 11, self.num_asteroids)
        self.belt_eccentricity = np.random.uniform(0, 0.15, self.num_asteroids)
        self.belt_inclination = np.random.uniform(-15, 15, self.num_asteroids)
        self.belt_phase = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        self.belt_ascending_nodes = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        
        # Initialize Hildas
        self.hilda_angles = []
        for angle in [0, 2*np.pi/3, 4*np.pi/3]:
            cluster_angles = np.random.normal(angle, 0.3, self.num_hildas//3)
            self.hilda_angles.extend(cluster_angles)
        self.hilda_angles = np.array(self.hilda_angles)
        self.hilda_radii = np.random.normal(self.radii['Jupiter'] * 0.8, 0.3, len(self.hilda_angles))
        self.hilda_inclination = np.random.uniform(-5, 5, len(self.hilda_angles))
        self.hilda_phase = np.random.uniform(0, 2*np.pi, len(self.hilda_angles))
        
        # Initialize Trojans
        self.trojan_angles1 = np.random.normal(np.pi/3, 0.2, self.num_trojans)
        self.trojan_angles2 = np.random.normal(5*np.pi/3, 0.2, self.num_trojans)
        self.trojan_radii = np.random.normal(self.radii['Jupiter'], 0.5, self.num_trojans)
        self.trojan_inclination = np.random.uniform(-10, 10, self.num_trojans)
        self.trojan_phase = np.random.uniform(0, 2*np.pi, self.num_trojans)
        
        # Initialize Kuiper Belt objects
        self.kuiper_angles = np.random.uniform(0, 2*np.pi, self.num_kuiper)
        self.kuiper_radii = np.random.uniform(77, 100, self.num_kuiper)
        self.kuiper_inclination = np.random.uniform(-20, 20, self.num_kuiper)
        self.kuiper_eccentricity = np.random.uniform(0, 0.2, self.num_kuiper)
        self.kuiper_ascending_nodes = np.random.uniform(0, 2*np.pi, self.num_kuiper)
        
    def calculate_3d_position(self, radius, angle, inclination, ascending_node=0):
        # Convert inclination to radians
        incl_rad = np.radians(inclination)
        
        # Calculate position in orbital plane
        x_orbit = radius * np.cos(angle)
        y_orbit = radius * np.sin(angle)
        
        # Apply inclination and ascending node rotation
        x = (x_orbit * np.cos(ascending_node) - 
             y_orbit * np.cos(incl_rad) * np.sin(ascending_node))
        y = (x_orbit * np.sin(ascending_node) + 
             y_orbit * np.cos(incl_rad) * np.cos(ascending_node))
        z = y_orbit * np.sin(incl_rad)
        
        return x, y, z
    
    def update(self, frame):
        self.ax.clear()
        
        # Update planet positions
        for planet in self.radii.keys():
            period_factor = self.periods[planet]
            angle = (2 * np.pi * frame / (100 * period_factor)) % (2 * np.pi)
            x, y, z = self.calculate_3d_position(
                self.radii[planet], 
                angle, 
                self.inclinations[planet]
            )
            self.planet_positions[planet]['x'] = x
            self.planet_positions[planet]['y'] = y
            self.planet_positions[planet]['z'] = z
        
        # Draw orbital paths
        theta = np.linspace(0, 2*np.pi, 100)
        for planet in self.radii.keys():
            x, y, z = self.calculate_3d_position(
                self.radii[planet], 
                theta, 
                self.inclinations[planet]
            )
            self.ax.plot(x, y, z, 'b-', alpha=0.1)
        
        # Update main belt asteroids
        belt_angles_update = self.belt_angles + frame * 0.02 / np.sqrt(self.belt_radii)
        eccentric_radii = self.belt_radii * (1 + self.belt_eccentricity * np.cos(belt_angles_update))
        belt_x, belt_y, belt_z = self.calculate_3d_position(
            eccentric_radii, 
            belt_angles_update, 
            self.belt_inclination,
            self.belt_ascending_nodes
        )
        
        # Update Hildas
        hilda_angles_update = (self.hilda_angles + 
                             frame * 0.005 + 
                             (2 * np.pi * frame / (100 * self.periods['Jupiter'])) * 2/3)
        hilda_x, hilda_y, hilda_z = self.calculate_3d_position(
            self.hilda_radii,
            hilda_angles_update,
            self.hilda_inclination
        )
        
        # Update Trojans
        jupiter_angle = (2 * np.pi * frame / (100 * self.periods['Jupiter'])) % (2 * np.pi)
        trojan_x1, trojan_y1, trojan_z1 = self.calculate_3d_position(
            self.trojan_radii,
            self.trojan_angles1 + jupiter_angle,
            self.trojan_inclination
        )
        trojan_x2, trojan_y2, trojan_z2 = self.calculate_3d_position(
            self.trojan_radii,
            self.trojan_angles2 + jupiter_angle,
            self.trojan_inclination
        )
        
        # Update Kuiper Belt
        kuiper_angles_update = self.kuiper_angles + frame * 0.01 / np.sqrt(self.kuiper_radii)
        eccentric_kuiper_radii = self.kuiper_radii * (1 + self.kuiper_eccentricity * np.cos(kuiper_angles_update))
        kuiper_x, kuiper_y, kuiper_z = self.calculate_3d_position(
            eccentric_kuiper_radii,
            kuiper_angles_update,
            self.kuiper_inclination,
            self.kuiper_ascending_nodes
        )
        
        # Plot everything
        self.ax.scatter([0], [0], [0], c='yellow', s=100)  # Sun
        
        # Plot planets
        for planet, pos in self.planet_positions.items():
            props = self.planet_properties[planet]
            self.ax.scatter(pos['x'], pos['y'], pos['z'], 
                          c=props['color'], s=props['size'])
            self.ax.text(pos['x'], pos['y'], pos['z'], planet, fontsize=8)
        
        # Plot asteroid populations
        self.ax.scatter(belt_x, belt_y, belt_z, c='red', s=1, alpha=0.3)
        self.ax.scatter(hilda_x, hilda_y, hilda_z, c='purple', s=1, alpha=0.3)
        self.ax.scatter(trojan_x1, trojan_y1, trojan_z1, c='green', s=1, alpha=0.3)
        self.ax.scatter(trojan_x2, trojan_y2, trojan_z2, c='green', s=1, alpha=0.3)
        self.ax.scatter(kuiper_x, kuiper_y, kuiper_z, c='gray', s=1, alpha=0.2)
        
        # Customize plot
        self.ax.set_xlim(-80, 80)
        self.ax.set_ylim(-80, 80)
        self.ax.set_zlim(-80, 80)
        self.ax.set_axis_off()
        self.ax.view_init(elev=20, azim=frame/2)  # Rotate view
        self.ax.set_title('Complete Solar System Animation', pad=20)
        
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
        
        self.fig.set_size_inches(16, 9)
        self.fig.set_dpi(240)
        
        writer = FFMpegWriter(fps=30, codec='h264')
        anim.save(filename, writer=writer)
        print(f"Animation saved as {filename}")

styles = {'light': 'default', 'dark': 'dark_background'}
for version, style in styles.items():
    solar_system = SolarSystemAnimation3D(style=style)
    filename = os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}.mov")
    solar_system.save4k(filename)
    filename = os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}.gif")
    solar_system.save(filename)
    #solar_system.animate()