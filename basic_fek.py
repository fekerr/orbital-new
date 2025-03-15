from complete_solar_system_3d import SolarSystemAnimation3D

# Create animation
solar_system = SolarSystemAnimation3D(style='default')

# Display animation
solar_system.animate()

# Save as GIF
solar_system.save("solar_system.gif")

# Save as 1080p video
solar_system.save1080p("solar_system_1080p.mp4")

# Save as 4K video
solar_system.save4k("solar_system_4k.mov")
