"""
isslib.visualization
====================

Fournit les contextes de représentation graphiques des données.
"""
from contextlib import contextmanager
import os

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


@contextmanager
def orbital():
    """Globle terrestre pour un affichage 3D de positions orbitales."""
    # Rayon terrestre moyen volumétrique
    earth_radius = 6371  # km
    # Découpage en 24 méridiens et 60 parallèles (choix cosmétique)
    u, v = np.mgrid[0:2 * np.pi:24j, 0:np.pi:60j]
    # Surface de la Terre
    x, y, z = np.array([np.cos(u) * np.sin(v),
                        np.sin(u) * np.sin(v), np.cos(v)]) * earth_radius
    # Représentation des méridiens
    meridians = [go.Scatter3d(x=xx, y=yy, z=zz, line_width=1,
                              line_color="cadetblue",
                              opacity=1, showlegend=False, hoverinfo='skip')
                 for xx, yy, zz in zip(x, y, z)]
    # Représentation de la surface de la Terre
    surface = go.Surface(x=earth_radius * np.cos(u)*np.sin(v),
                         y=earth_radius * np.sin(u)*np.sin(v),
                         z=earth_radius * np.cos(v),
                         opacity=0.7, colorscale="Blues_r", showscale=False,
                         hoverinfo='none')
    # Ajout d'un axe de rotation (pour une meilleure compréhension du rendu)
    axis = go.Scatter3d(x=[0]*2, y=[0]*2,
                        z=[-1.2*earth_radius, 1.2*earth_radius], line_width=2,
                        line_color='gray', opacity=0.6, showlegend=False)
    # Chargement de la représentation de la Terre comme figure de base
    fig = go.Figure(meridians + [axis, surface])
    # Template pour afficher les scatter3d en mode ligne par défaut
    orbit_template = go.layout.Template()
    orbit_template.data.scatter3d = [go.Scatter3d(mode="lines", line_width=3,
                                                  hoverinfo='skip')]
    # Supression des plans d'axes en arrière-plan
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,
                      zaxis_visible=False)
    # Paramètrage d'une caméra au plus près de la Terre
    fig.update_layout(scene_camera=dict(up=dict(x=0, y=np.sin(.409),
                                                z=np.cos(.409)),
                                        eye=dict(x=1.25, y=0, z=0)),
                      scene_dragmode='orbit', margin=dict(l=0, r=0, b=0, t=50),
                      template=orbit_template)
    # Renvoi de la figure pour utilisation
    yield fig
    # Affichage de la représentation
    fig.show()


@contextmanager
def worldmap(transparency=.5):
    """Fond de carte utilisant une projection équirectangulaire plate carrée.

    Paramètres:
      - transparency: Définit la transparence de la carte,
                      de 0 (mat) à 1 (invisible).
    """
    # Définit alpha comme le complémentaire à 1 de transparency borné à [0,1]
    alpha = min(max(transparency, 0), 1)
    # Visualisation sur toute la largeur du calepin
    plt.figure(figsize=(16, 12))
    # Image de fond
    bg_img = os.path.join("resources", "plate_carree.jpg")
    # Paramétrage des coordonnées extrêmes de l'image de fond
    plt.imshow(plt.imread(bg_img), alpha=alpha, extent=[-180, 180, -90, 90])
    # Paramétrage des axes
    plt.xticks(np.arange(-180, 181, 30))
    plt.xlabel("Longitude [°]")
    plt.yticks(np.arange(-90, 91, 30))
    plt.ylabel("Latitude [°]")
    # Empêche les débordements par défaut (redéfinissable à l'utilisation)
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    # Retour de la fonction pour exécution du bloc `with`
    yield
    # Affichage en sortie du `with`
    plt.show()
