from contextlib import contextmanager


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go


@contextmanager
def worldmap(transparency=.5):
    """Fournit un fond de carte mondial utilisant une projection équirectangulaire plate carrée.
    
    Paramètres:
      - transparency: Définit la transparence de la carte, de 0 (mat) à 1 (invisible).
    """
    # Définit alpha comme le complémentaire à 1 de transparency borné à [0,1]
    alpha = min(max(transparency,0),1)
    # Visualition sur toute la largeur du notebook
    plt.figure(figsize=(16,12))
    # Paramétrage des coordonnées extrêmes de l'image de fond
    plt.imshow(plt.imread("plate_carree.jpg"), alpha=alpha, extent=[ -180, 180, -90, 90])
    # Paramétrage des axes
    plt.xticks(np.arange(-180, 181, 30))
    plt.xlabel("Longitude [°]")
    plt.yticks(np.arange(-90, 91, 30))
    plt.ylabel("Latitude [°]")
    # Retour de la fonction pour exécution du bloc `with`
    yield
    # Affichage en sortie du `with`
    plt.show()


class ISS_Position:
    """Classe d'extraction des données de position de l'ISS."""
    def __init__(self, filename="ISS.OEM_J2K_EPH.txt"):
        """Reçoit en paramètre le nom du fichier de données. Utilise "ISS.OEM_J2K_EPH.txt" par défaut."""
        self.__parse_source(filename)
        
    def __parse_source(self, filename):
        """Analyse syntaxique du fichier."""
        with open(filename) as file:
            source_lines = file.readlines()
        # Extraction des métadonnées
        self.__parse_source_meta(source_lines)
        # Extraction des commentaires
        self.__parse_source_comments(source_lines)
        # Extraction des données
        self.__parse_data(filename)
    
    def __parse_source_meta(self, source_lines):
        """Extraction des métadonnées du fichier."""
        # Détection des lignes de métadonnées
        meta = slice(source_lines.index('META_START\n')+1, source_lines.index('META_STOP\n'))
        # Enregistrement des métadonnées dans un dictionnaire
        self.meta = {key.strip(): pd.to_datetime(value.strip()) if key.strip().endswith('_TIME') else value.strip()
                     for line in source_lines[meta]
                     for (key, value) in [line.split('=', 1)]
                    }
    
    def __parse_source_comments(self, source_lines):
        """Extraction des commentaires du fichier."""
        # Sélection des lignes de commentaires
        comments = [line for line in source_lines if line.startswith("COMMENT")]
        # Stockage de l'index de la dernière ligne de commentaire en prévision de l'accès aux données
        self.__last_comment_index = source_lines.index(comments[-1])
        # Enregistrement des commentaires dans une liste
        self.comments = [comment[7:].strip() for comment in comments]
    
    def __parse_data(self, filename):
        """Extraction des données du fichier."""
        # Enregistrement des données dans un DataFrame, à partir des lignes suivant le dernier commentaire
        self.data = pd.read_csv(filename, skiprows=self.__last_comment_index+1,
                                sep=" ", names=['datetime', 'x', 'y', 'z', 'vx', 'vy', 'vz'],
                                parse_dates=[0], infer_datetime_format=True)
        # Ajoute les annotations de poussée
        self.__add_thrust_metadata()
        
    def __add_thrust_metadata(self):
        """Ajout des annotation de poussé et épisodes de poussée."""
        # Les enregistrements datant de deux secondes après leur précédent sont marqués en tant que poussée
        self.data['on_thrust'] = np.isclose(self.data.diff().datetime.dt.total_seconds(), 2)
        # Initialisation des valeurs d'épisode de poussée
        self.__current_state = self.data.iloc[0]['on_thrust']
        self.__current_tid = 0
        # Un épsiode est une séquence contiguë d'état de poussée
        self.data['thrust_episode'] = self.data['on_thrust'].apply(self.__thrust_episode)
        # Suppression des marqueurs inutiles
        del self.__current_state, self.__current_tid

    def __thrust_episode(self, on_thrust):
        """Méthode pour le parours de proche en proche des états de poussée pour la définition d'épisodes."""
        # Si l'état actuel est différent du dernier état enregistré
        if on_thrust != self.__current_state:
            # Changement d'état et d'identifiant d'épisode.
            self.__current_state = on_thrust
            self.__current_tid += 1
        # Renvoi de l'indentifiant actuel
        return self.__current_tid


    def get_metadata(self):
        # Retourne les métadonnées en utilisant un DataFrame (pour son rendu élégant à l'affichage)
        return pd.DataFrame(self.meta.values(), self.meta.keys(), ['Metadata'])
    
    def get_comments(self):
        # Retourne les commentaires en tant que bloc de texte avec retours à la ligne
        return '\n'.join(self.comments)
    
    def get_data(self):
        # Retourne le DataFrame des données
        return self.data


@contextmanager
def orbital_visualization():
    """Représentation d'un globle terrestre pour un affichage 3D de positions orbitales."""
    # Rayon terrestre moyen volumétrique
    earth_radius = 6371
    # Découpage en 24 méridiens et 60 parallèles
    u, v = np.mgrid[0:2 * np.pi:24j, 0:np.pi:60j]
    # Surface de la Terre
    x, y, z = np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v)]) * earth_radius
    # Représentation des méridiens
    meridians = [go.Scatter3d(x=xx, y=yy, z=zz, line_width=1, line_color="cadetblue",
                              opacity=1, showlegend=False, hoverinfo='skip')
                 for xx, yy, zz in zip(x,y,z)]
    # Représentation de la surface de la Terre
    surface = go.Surface(x=earth_radius * np.cos(u)*np.sin(v),
                         y=earth_radius * np.sin(u)*np.sin(v),
                         z=earth_radius * np.cos(v),
                         opacity=0.7, colorscale="Blues_r", showscale=False, hoverinfo='none')
    # Représentation de l'axe de rotation (pour une meilleure compréhension du rendu)
    axis = go.Scatter3d(x=[0]*2, y=[0]*2, z=[-1.2*earth_radius, 1.2*earth_radius], line_width=2,
                        line_color='gray', opacity=0.6, showlegend=False)
    # Chargement de la représentation de la Terre comme figure de base
    fig = go.Figure(meridians + [axis, surface])
    # Template pour afficher les scatter3d en mode ligne par défaut
    orbit_template = go.layout.Template()
    orbit_template.data.scatter3d = [go.Scatter3d(mode="lines", line_width=3)]
    # Supression des plans d'axes en arrière-plan
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    # Paramètrage d'une caméra au plus près de la Terre
    fig.update_layout(scene_camera=dict(up=dict(x=0, y=np.sin(.409), z=np.cos(.409)), eye=dict(x=1.25, y=0, z=0)),
                      scene_dragmode='orbit', margin=dict(l=0,r=0,b=0,t=50), template=orbit_template)
    # Renvoi de la figure pour utilisation
    yield fig
    # Affichage de la représentation
    fig.show()

def celestial2terrestrial(x, y, z, datetime, mode='cartesian'):
    """Transformation de coordonnées depuis le repère celeste vers le repère terrestre.
    
    La fonction prend en paramètre les coordonnées cartésiennes d'origine ainsi que la
    date et l'heure de la position, nécessaire pour la projeter dans le repère terrestre.
    La fonction retourne les coordonnées (x,y,z) dans le repère terrestre,
    ou les valeurs (longitude, latitude, distance) si le paramètre facultatif `mode='spherical'`
    est utilisé.
    """
    # coordonnées sidérales depuis les données
    geo = SkyCoord(x=x, y=y, z=z, unit=u.km, frame=GCRS,
                   representation_type='cartesian',
                   obstime=datetime).transform_to(ITRS)
    # Représentation cartésienne
    if mode == 'cartesian':
        return geo.x.value, geo.y.value, geo.z.value
    # Représentation sphérique
    elif mode == 'spherical':
        sph = geo.represent_as('spherical')
        return sph.lon.degree, sph.lat.degree, sph.distance.value
    # Paramètre de représentation incorrect
    else:
        raise ValueError("mode should be either 'cartesian' or 'spherical'.")