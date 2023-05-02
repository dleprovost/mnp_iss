"""
isslib.coordinates
==================

Fournit les fonctions de conversions de repères et coordonnées.
"""
from astropy.coordinates import GCRS, ITRS, SkyCoord
import astropy.units as units
import numpy as np


def cartesian2spherical(x, y, z, unit='rad'):
    """Transforme des coordonnées cartésiennes en coordonnées sphériques.

    La convention utilisée ici est rayon-longitude-latitude.
    """
    # Représentation cartésienne
    sk_cart = SkyCoord(x, y, z, frame=GCRS, unit=units.km,
                       representation_type='cartesian')
    # Représentation sphérique
    sk_sph = sk_cart.represent_as('spherical')
    # Retourne les distances en km et les longitude et latitudes en radians
    if unit == 'rad':
        return sk_sph.distance.km, sk_sph.lon.rad, sk_sph.lat.rad
    # Retourne les distances en km et les longitude et latitudes en degrés
    elif unit == 'deg':
        return sk_sph.distance.km, sk_sph.lon.deg, sk_sph.lat.deg
    # Paramètre d'unité incorrect
    else:
        raise ValueError("unit should be either 'deg' or 'rad'.")


def celestial2terrestrial(x, y, z, datetime, mode='cartesian'):
    """Transformation de coordonnées du repère celeste vers le repère terrestre

    La fonction prend en paramètre les coordonnées cartésiennes d'origine ainsi
    que la date et l'heure de la position, nécessaire pour la projeter dans le
    repère terrestre.
    La fonction retourne les coordonnées (x,y,z) dans le repère terrestre,
    ou les valeurs (rayon, longitude, latitude) si le paramètre facultatif
    `mode='spherical'` est utilisé.
    """
    # coordonnées sidérales depuis les données
    geo = SkyCoord(x=x, y=y, z=z, unit=units.km, frame=GCRS,
                   representation_type='cartesian',
                   obstime=datetime).transform_to(ITRS)
    # Représentation cartésienne
    if mode == 'cartesian':
        return geo.x.value, geo.y.value, geo.z.value
    # Représentation sphérique
    elif mode == 'spherical':
        sph = geo.represent_as('spherical')
        return sph.distance.value, sph.lon.degree, sph.lat.degree
    # Paramètre de représentation incorrect
    else:
        raise ValueError("mode should be either 'cartesian' or 'spherical'.")


def worldmap_traces(longitudes, latitudes, join_traces=True):
    """Séparation de tableaux de longitudes/latitudes en traces planisphère."""
    # Position des retours arrières
    crs = np.where(np.diff(longitudes) < -300)[0] + 1
    # Tableau des débuts de traces
    line_starts = np.concatenate([[0], crs])
    # Tableau des fin de traces
    line_ends = np.concatenate([crs, [len(longitudes)]])
    # Séparation des traces
    traces = [(longitudes[start:end], latitudes[start:end])
              for (start, end) in zip(line_starts, line_ends)]
    # Si création de traces jointes sur les bords
    if join_traces:
        jtraces = [None] * len(traces)
        for i in range(len(traces)):
            # Ajout hors-champ de la position précédente à gauche
            in_lon, in_lat = ((traces[i-1][0][-1:] - 360,
                               traces[i-1][1][-1:])
                              if i > 0 else ([], []))
            # Ajout hors-champ de la position suivante à droite
            out_lon, out_lat = (([traces[i+1][0][:1] + 360,
                                  traces[i+1][1][:1]])
                                if i < len(traces) - 1 else ([], []))
            # Création des nouvelles traces
            jtraces[i] = (np.concatenate([in_lon, traces[i][0], out_lon]),
                          np.concatenate([in_lat, traces[i][1], out_lat]))
        return jtraces
    else:
        return traces


def pi_interval(value):
    """Convertit un angle en radian à son égal dans l'intervalle [-pi;pi[."""
    # Utilise la position du point relatif dans le cercle complexe
    return np.angle(complex(np.cos(value), np.sin(value)))


def positive_pi(value):
    """Convertit un angle en radian à son égal dans l'intervalle [0;2*pi[."""
    # Utilise le modulo 2pi de son égal dans l'intervalle [-pi;pi[
    return pi_interval(value) % (2*np.pi)


# Vectorise les fonctions `pi_interval` et `positive_pi`
pi_interval = np.vectorize(pi_interval)
positive_pi = np.vectorize(positive_pi)
