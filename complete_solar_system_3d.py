import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from matplotlib.animation import FFMpegWriter
import os

OS_PATH = os.path.dirname(os.path.realpath('__file__'))

class Config:
    SETTINGS = {
        'frames': 2500,
        'camera_distance': 100,
        'min_camera_distance': 10,
        'max_camera_distance': 400,
        'zoom_speed': 0.00005,
        'base_speed': 0.2,
        'asteroid_counts': {
            'belt': 2000,
            'hildas': 300,
            'trojans': 300,
            'kuiper': 4000,
        },
        'planet_properties': {
            'Mercury': {'color': 'gray', 'size': 20},
            'Venus': {'color': 'orange', 'size': 30},
            'Earth': {'color': 'blue', 'size': 30},
            'Mars': {'color': 'red', 'size': 25},
            'Jupiter': {'color': 'orange', 'size': 60},
            'Saturn': {'color': 'gold', 'size': 55},
            'Uranus': {'color': 'lightblue', 'size': 45},
            'Neptune': {'color': 'blue', 'size': 45},
            'Pluto': {'color': 'brown', 'size': 15},
        },
        'orbital_periods': {
            'Mercury': 0.24,
            'Venus': 0.62,
            'Earth': 1.0,
            'Mars': 1.88,
            'Jupiter': 11.86,
            'Saturn': 29.46,
            'Uranus': 84.01,
            'Neptune': 164.79,
            'Pluto': 248.09,
        },
        'orbital_radii': {
            'Mercury': 1,
            'Venus': 1.8,
            'Earth': 2.5,
            'Mars': 3.8,
            'Jupiter': 13,
            'Saturn': 24,
            'Uranus': 48,
            'Neptune': 75,
            'Pluto': 79,
        },
        'orbital_inclinations': {
            'Mercury': 7.0,
            'Venus': 3.4,
            'Earth': 0.0,
            'Mars': 1.9,
            'Jupiter': 1.3,
            'Saturn': 2.5,
            'Uranus': 0.8,
            'Neptune': 1.8,
            'Pluto': 17.16,
        },
    }

class SolarSystemAnimation3D:
    
    def __init__(self, style='default'):
        # Set up the 3D figure
        plt.style.use(style)
        self.fig = plt.figure(figsize=(16, 9))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.settings = Config.SETTINGS
        self.frames = self.settings['frames']
        self.camera_distance = self.settings['camera_distance']
        self.min_camera_distance = self.settings['min_camera_distance']
        self.max_camera_distance = self.settings['max_camera_distance']
        self.zoom_speed = self.settings['zoom_speed']
        self.base_speed = self.settings['base_speed']
        self.planet_properties = self.settings['planet_properties']
        self.periods = self.settings['orbital_periods']
        self.radii = self.settings['orbital_radii']
        self.inclinations = self.settings['orbital_inclinations']
        
        asteroid_counts = self.settings['asteroid_counts']
        self.num_asteroids = asteroid_counts['belt']
        self.num_hildas = asteroid_counts['hildas']
        self.num_trojans = asteroid_counts['trojans']
        self.num_kuiper = asteroid_counts['kuiper']
        
        # Initialize positions
        self.init_positions()
        
    def init_positions(self):
        # Initialize planet positions
        self.planet_positions = {planet: {'x': [], 'y': [], 'z': []} for planet in self.radii.keys()}
        
        # Initialize main belt asteroids with more spread
        self.belt_angles = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        # Spread asteroids between Mars and Jupiter with a more uniform distribution
        self.belt_radii = np.random.uniform(5, 11, self.num_asteroids)  # Start after Mars
        # Increase eccentricity variation
        self.belt_eccentricity = np.random.uniform(0.1, 0.3, self.num_asteroids)
        # Increase inclination spread
        self.belt_inclination = np.random.uniform(-20, 20, self.num_asteroids)
        self.belt_phase = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        self.belt_ascending_nodes = np.random.uniform(0, 2*np.pi, self.num_asteroids)
        
        # Initialize Hildas with more spread
        self.hilda_angles = []
        for angle in [0, 2*np.pi/3, 4*np.pi/3]:
            cluster_angles = np.random.normal(angle, 0.5, self.num_hildas//3)  # Increased spread
            self.hilda_angles.extend(cluster_angles)
        self.hilda_angles = np.array(self.hilda_angles)
        self.hilda_radii = np.random.normal(self.radii['Jupiter'] * 0.8, 0.8, len(self.hilda_angles))
        self.hilda_inclination = np.random.uniform(-10, 10, len(self.hilda_angles))
        self.hilda_phase = np.random.uniform(0, 2*np.pi, len(self.hilda_angles))
        
        # Initialize Trojans with more spread
        self.trojan_angles1 = np.random.normal(np.pi/3, 0.4, self.num_trojans)  # Increased spread
        self.trojan_angles2 = np.random.normal(5*np.pi/3, 0.4, self.num_trojans)
        self.trojan_radii = np.random.normal(self.radii['Jupiter'], 1.0, self.num_trojans)
        self.trojan_inclination = np.random.uniform(-15, 15, self.num_trojans)
        self.trojan_phase = np.random.uniform(0, 2*np.pi, self.num_trojans)
        
        # Initialize Kuiper Belt objects with more spread
        self.kuiper_angles = np.random.uniform(0, 2*np.pi, self.num_kuiper)
        self.kuiper_radii = np.random.uniform(80, 120, self.num_kuiper)  # Increased range
        self.kuiper_inclination = np.random.uniform(-30, 30, self.num_kuiper)  # Increased inclination
        self.kuiper_eccentricity = np.random.uniform(0.1, 0.3, self.num_kuiper)  # Increased eccentricity
        self.kuiper_ascending_nodes = np.random.uniform(0, 2*np.pi, self.num_kuiper)
        
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
    
    def calculate_visibility(self, positions, camera_distance, max_distance=500):
        """Calculate opacity based on distance from camera"""
        # Calculate distances from camera position
        camera_pos = np.array([0, -camera_distance, camera_distance/2])  # Angled view
        if isinstance(positions[0], np.ndarray):
            points = np.vstack((positions[0], positions[1], positions[2])).T
        else:
            points = np.array([[positions[0], positions[1], positions[2]]])
            
        distances = np.linalg.norm(points - camera_pos, axis=1)
        
        # Calculate opacity based on distance
        max_opacity = 0.8
        min_opacity = 0.1
        
        # Inverse relationship between distance and opacity
        opacity = np.clip(max_opacity * (1 - distances/max_distance), min_opacity, max_opacity)
        
        # Add distance-based size scaling
        size_scale = np.clip(1.5 * (1 - distances/max_distance), 0.2, 1.0)
        
        return opacity, size_scale
    
    def update(self, frame):
        print(f"{frame}")
        self.ax.clear()
        
        # Calculate camera distance with smooth zoom
        zoom_progress = frame / 100
        self.camera_distance = self.max_camera_distance - (self.max_camera_distance - self.min_camera_distance) * (1 - np.exp(-self.zoom_speed * frame))
        
        # Update planet positions using angular velocities
        for planet in self.radii.keys():
            # Convert period to angular velocity
            angular_velocity = 1.0 / self.periods[planet]
            angle = self.base_speed * frame * angular_velocity
            
            x, y, z = self.calculate_3d_position(
                self.radii[planet], 
                angle, 
                self.inclinations[planet]
            )
            self.planet_positions[planet]['x'] = x
            self.planet_positions[planet]['y'] = y
            self.planet_positions[planet]['z'] = z
        
        # Draw orbital paths with distance-based opacity
        theta = np.linspace(0, 2*np.pi, 100)
        for planet in self.radii.keys():
            x, y, z = self.calculate_3d_position(
                self.radii[planet], 
                theta, 
                self.inclinations[planet]
            )
            opacity, _ = self.calculate_visibility((x, y, z), self.camera_distance)
            self.ax.plot(x, y, z, 'b-', alpha=opacity.mean() * 0.8)
        
        # Calculate asteroid belt velocities
        mars_velocity = 1.0 / self.periods['Mars']
        jupiter_velocity = 1.0 / self.periods['Jupiter']
        
        # Interpolate velocities instead of periods
        asteroid_velocities = jupiter_velocity + (mars_velocity - jupiter_velocity) * (
            (self.belt_radii - self.radii['Jupiter']) / (self.radii['Mars'] - self.radii['Jupiter'])
        )
        
        # Update asteroid positions
        belt_angles_update = self.belt_angles + self.base_speed * frame * asteroid_velocities
        eccentric_radii = self.belt_radii * (1 + self.belt_eccentricity * np.cos(belt_angles_update))
        belt_x, belt_y, belt_z = self.calculate_3d_position(
            eccentric_radii, 
            belt_angles_update, 
            self.belt_inclination,
            self.belt_ascending_nodes
        )
        belt_opacity, belt_size = self.calculate_visibility((belt_x, belt_y, belt_z), self.camera_distance)
        
        # Update Hildas using Jupiter's velocity
        jupiter_velocity = 1.0 / self.periods['Jupiter']
        jupiter_angle = self.base_speed * frame * jupiter_velocity
        hilda_angles_update = self.hilda_angles + jupiter_angle * 2/3
        hilda_x, hilda_y, hilda_z = self.calculate_3d_position(
            self.hilda_radii,
            hilda_angles_update,
            self.hilda_inclination
        )
        hilda_opacity, hilda_size = self.calculate_visibility((hilda_x, hilda_y, hilda_z), self.camera_distance)
        
        # Update Trojans with Jupiter's velocity
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
        trojan_opacity1, trojan_size1 = self.calculate_visibility((trojan_x1, trojan_y1, trojan_z1), self.camera_distance)
        trojan_opacity2, trojan_size2 = self.calculate_visibility((trojan_x2, trojan_y2, trojan_z2), self.camera_distance)
        
        # Update Kuiper Belt with much slower velocities
        kuiper_velocities = 0.1 / np.sqrt(self.kuiper_radii)  # Slower velocity for outer objects
        kuiper_angles_update = self.kuiper_angles + self.base_speed * frame * kuiper_velocities
        eccentric_kuiper_radii = self.kuiper_radii * (1 + self.kuiper_eccentricity * np.cos(kuiper_angles_update))
        kuiper_x, kuiper_y, kuiper_z = self.calculate_3d_position(
            eccentric_kuiper_radii,
            kuiper_angles_update,
            self.kuiper_inclination,
            self.kuiper_ascending_nodes
        )
        kuiper_opacity, kuiper_size = self.calculate_visibility((kuiper_x, kuiper_y, kuiper_z), self.camera_distance)
        
        # Plot everything with dynamic visibility
        self.ax.scatter([0], [0], [0], c='yellow', s=100)  # Sun
        
        # Plot planets with distance-based visibility
        for planet, pos in self.planet_positions.items():
            props = self.planet_properties[planet]
            planet_opacity, planet_size = self.calculate_visibility(
                (pos['x'], pos['y'], pos['z']), 
                self.camera_distance
            )
            self.ax.scatter(pos['x'], pos['y'], pos['z'],
                        c=props['color'],
                        s=props['size'] * planet_size[0],
                        alpha=planet_opacity[0])
            if planet_opacity[0] > 0.3:
                self.ax.text(pos['x'], pos['y'], pos['z'], planet, fontsize=8)
        
        # Plot asteroid populations with dynamic visibility
        self.ax.scatter(belt_x, belt_y, belt_z, 
                    c='red', s=1 * belt_size, alpha=belt_opacity)
        self.ax.scatter(hilda_x, hilda_y, hilda_z, 
                    c='purple', s=1 * hilda_size, alpha=hilda_opacity)
        self.ax.scatter(trojan_x1, trojan_y1, trojan_z1, 
                    c='green', s=1 * trojan_size1, alpha=trojan_opacity1)
        self.ax.scatter(trojan_x2, trojan_y2, trojan_z2, 
                    c='green', s=1 * trojan_size2, alpha=trojan_opacity2)
        self.ax.scatter(kuiper_x, kuiper_y, kuiper_z, 
                    c='gray', s=1 * kuiper_size, alpha=kuiper_opacity)
        
        # Update view limits
        limit = self.camera_distance * 0.6
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_zlim(-limit, limit)
        self.ax.set_axis_off()
        
        plt.subplots_adjust(left=-.5, bottom=-2, right=1.5, top=3, wspace=None, hspace=None)
        
        #self.ax.view_init(elev=90, azim=0) # Top down view
        #self.ax.view_init(elev=20, azim=frame/0.2) # Rotation frame by frame
        self.ax.view_init(elev=20, azim=45) 
        
        self.ax.set_title('Complete Solar System Animation', pad=20)
        
    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=self.frames, interval=50, blit=False)
        plt.show()
        
    def save(self, filename):
        anim = FuncAnimation(self.fig, self.update, frames=self.frames, interval=50, blit=False)
        self.fig.set_size_inches(16, 9)
        self.fig.set_dpi(100)
        anim.save(filename, writer=PillowWriter(fps=20))
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
    solar_system = SolarSystemAnimation3D(style=style)
    filename = os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}.gif")
    # solar_system.save(filename)
    filename = os.path.join(OS_PATH, f"output/complete_solar_system_3d_{version}.mov")
    solar_system.save4k(filename)
    # solar_system.animate()
