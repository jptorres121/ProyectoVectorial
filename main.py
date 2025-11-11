import pyvista as pv
import numpy as np
import math

# ============================
# CONFIGURACIÓN INICIAL
# ============================
plotter = pv.Plotter(window_size=(1000, 850))
plotter.set_background("#1a0f00")  # fondo estilo pergamino oscuro

# ============================
# MODELO DEL TORNILLO AÉREO
# ============================
base = pv.Cylinder(center=(0, 0, 0), direction=(0, 0, 1),
                   radius=1.0, height=0.2, resolution=100)

mastil = pv.Cylinder(center=(0, 0, 0.9), direction=(0, 0, 1),
                     radius=0.05, height=1.8, resolution=100)

# Hélice espiral
def generar_helice(num_giros=1.5, altura=1.2, radio_inicial=1.0, radio_final=0.2):
    n = 200
    theta = np.linspace(0, num_giros * 2 * np.pi, n)
    z = np.linspace(0, altura, n)
    radios = np.linspace(radio_inicial, radio_final, n)
    x = radios * np.cos(theta)
    y = radios * np.sin(theta)
    points = np.column_stack([x, y, z + 1.2])
    return pv.Spline(points, n)

helice_borde = generar_helice()

# Tela cónica de la hélice
theta = np.linspace(0, 3*np.pi, 150)
z = np.linspace(0, 1.2, 150)
r1 = np.linspace(1.0, 0.2, 150)
r2 = np.linspace(0.05, 0.05, 150)

x1, y1 = r1 * np.cos(theta), r1 * np.sin(theta)
x2, y2 = r2 * np.cos(theta), r2 * np.sin(theta)

faces = []
for i in range(len(theta) - 1):
    faces.append([4, i, i + 1, len(theta) + i + 1, len(theta) + i])

x = np.concatenate([x1, x2])
y = np.concatenate([y1, y2])
z = np.concatenate([z + 1.2, z + 1.2])

helice_superficie = pv.PolyData(np.c_[x, y, z], faces=np.hstack(faces))

modelo = base + mastil + helice_superficie + helice_borde

# ============================
# ESTILO VISUAL
# ============================
plotter.add_text(
    "Tornillo aéreo de Leonardo da Vinci (simulación 3D)",
    font_size=18,
    color="#d2b48c",
    position='upper_edge',
)

actor = plotter.add_mesh(modelo, color="#bfa063", specular=0.8, smooth_shading=True)

# ============================
# CÁMARA INICIAL
# ============================
plotter.camera_position = [
    (4, 4, 2.5),  # posición más lejana
    (0, 0, 0.8),  # punto de enfoque
    (0, 0, 1)     # vector "arriba"
]

# ============================
# ANIMACIÓN USANDO on_render
# ============================
t = 0.0

def actualizar_camara(*args):
    global t
    x = 4 * math.cos(t)
    y = 4 * math.sin(t)
    z = 2.5 + 0.2 * math.sin(t * 2)
    plotter.camera_position = [(x, y, z), (0, 0, 0.8), (0, 0, 1)]
    modelo.rotate_z(0.5, point=(0, 0, 0.8), inplace=True)
    t += 0.02

plotter.add_on_render_callback(actualizar_camara)

# ============================
# MOSTRAR ESCENA
# ============================
plotter.show()