"""
isslib.coordinates
==================

Fournit les fonctions de conversions de repères et coordonnées.
"""
from astropy.coordinates import GCRS, ITRS, SkyCoord
import astropy.units as units


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
