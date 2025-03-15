# Begin chunk 011 of 12 (3000 bytes max)
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
# End chunk 011 of 12 (3000 bytes max)
