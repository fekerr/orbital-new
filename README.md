# Solar System 3D Animation

A comprehensive 3D visualization of our solar system including planets, moons, asteroid belts, and the Oort cloud implemented in Python using Matplotlib.

<img width="100%" alt="Screenshot 2025-01-19 at 15 32 35" src="https://github.com/user-attachments/assets/3beb28dd-457a-4fcb-b41a-de6aa0a573dc" />


## Features

- Full 3D representation of the solar system
- Accurate orbital mechanics based on Kepler's laws
- Includes all planets and major moons
- Visualization of:
  - Asteroid Belt
  - Hildas Group
  - Jupiter Trojans
  - Kuiper Belt
  - Inner Oort Cloud (Hills Cloud)
  - Outer Oort Cloud
- Dynamic camera with smooth zoom
- Multiple output formats (GIF, 1080p MP4, 4K MOV)
- Light and dark theme options

## Mathematical Physics

### Orbital Mechanics

The simulation uses Kepler's laws of planetary motion to calculate orbital positions:

1. **Kepler's First Law**: Orbits are elliptical with the Sun at one focus
   ![equation](https://latex.codecogs.com/png.latex?r=\frac{a(1-e^2)}{1+e\cos\theta})
   where:
   - r = distance from the sun
   - a = semi-major axis
   - e = eccentricity
   - θ = true anomaly

2. **Kepler's Second Law**: Equal areas are swept in equal times
   ![equation](https://latex.codecogs.com/png.latex?\frac{dA}{dt}=\frac{1}{2}r^2\frac{d\theta}{dt}=constant)

3. **Kepler's Third Law**: The square of the orbital period is proportional to the cube of the semi-major axis
   ![equation](https://latex.codecogs.com/png.latex?T^2=\frac{4\pi^2}{GM}a^3)

### 3D Position Calculation

The position of celestial bodies is calculated using:

```mermaid
graph TD
    A[Orbital Elements] --> B[Calculate in Orbital Plane]
    B --> C[Apply Inclination]
    C --> D[Apply Ascending Node]
    D --> E[Final 3D Position]
```

Position calculation formula:
![equation](https://latex.codecogs.com/png.latex?%5Cbegin%7Bpmatrix%7D%20x%20%5C%5C%20y%20%5C%5C%20z%20%5Cend%7Bpmatrix%7D%20%3D%20%5Cbegin%7Bpmatrix%7D%20%5Ccos%5COmega%20%26%20-%5Csin%5COmega%5Ccos%20i%20%5C%5C%20%5Csin%5COmega%20%26%20%5Ccos%5COmega%5Ccos%20i%20%5C%5C%200%20%26%20%5Csin%20i%20%5Cend%7Bpmatrix%7D%20%5Cbegin%7Bpmatrix%7D%20r%5Ccos%5Ctheta%20%5C%5C%20r%5Csin%5Ctheta%20%5Cend%7Bpmatrix%7D)

Where:
- Ω = ascending node
- i = inclination
- r = orbital radius
- θ = orbital angle

## System Architecture

```mermaid
classDiagram
    class Config {
        +SETTINGS: dict
        +frames: int
        +camera_distance: float
        +planets: dict
        +asteroid_counts: dict
    }
    class SolarSystemAnimation3D {
        +init_positions()
        +update(frame)
        +calculate_3d_position()
        +calculate_visibility()
        +animate()
        +save()
        +save1080p()
        +save4k()
    }
    Config -- SolarSystemAnimation3D
```

## Requirements

- Python 3.7+
- NumPy
- Matplotlib
- FFmpeg (for video output)

## Installation

```bash
pip install numpy matplotlib
# For video output
apt-get install ffmpeg  # Linux
brew install ffmpeg    # macOS
```

## Usage

Basic usage:

```python
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
```

## Customization

You can modify the Config.SETTINGS dictionary to:
- Adjust animation frames
- Change camera behavior
- Modify planet/moon properties
- Adjust asteroid population sizes

## Performance Notes

- The animation is computationally intensive, especially with large asteroid populations
- 4K rendering requires significant memory and processing power
- Consider reducing asteroid counts for smoother performance

## License

MIT License - feel free to use and modify for your own projects!
