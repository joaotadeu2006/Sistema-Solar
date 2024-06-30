import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric, CartesianRepresentation
import astropy.units as u

# Configura a animação
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-10, 10)  # More zoom out
ax.set_ylim(-10, 10)  # More zoom out
ax.set_zlim(-10, 10)  # More zoom out
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Função para iniciar a animação
def init():
    return []

# Função para atualizar a animação
def update(frame):
    ax.cla()
    ax.set_xlim(-10, 10)  # More zoom out
    ax.set_ylim(-10, 10)  # More zoom out
    ax.set_zlim(-10, 10)  # More zoom out
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    with solar_system_ephemeris.set('builtin'):
        time = Time(frame, format='jyear')
        planet_colors = {'sun': 'yellow', 'mercury': 'gray', 'venus': 'orange', 'earth': 'blue', 'mars': 'red',
                         'jupiter': 'brown', 'saturn': 'silver', 'uranus': 'cyan', 'neptune': 'purple'}

        planets = list(planet_colors.keys())
        for planet_name in planets:
            planet = get_body_barycentric(planet_name, time)
            planet_position = planet.represent_as(CartesianRepresentation)
            color = planet_colors.get(planet_name, 'gray')
            ax.scatter(planet_position.x, planet_position.y, planet_position.z, label=planet_name.capitalize(), color=color)

            # Traça a órbita
            orbit_positions = get_body_barycentric(planet_name, time - np.linspace(0, 365, 100)*u.day).represent_as(CartesianRepresentation)
            ax.plot(orbit_positions.x, orbit_positions.y, orbit_positions.z, linestyle='dashed', color=color)

    ax.legend(loc='upper right')
    return []

# Cria a animação
ani = animation.FuncAnimation(fig, update, frames=np.linspace(2024, 2025, 365), init_func=init, blit=True)

plt.show()