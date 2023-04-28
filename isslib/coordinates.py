"""
isslib.coordinates
==================

Fournit les fonctions de conversions de repères et coordonnées.
"""
from astropy.coordinates import GCRS, ITRS, SkyCoord
import astropy.units as units


def cartesian2spherical(x, y, z):
    """Transforme des coordonnées cartésiennes en coordonnées sphériques.
    
    La convention rayon-longitude-latitude est ici utilisée.
    """
    # Représentation cartésienne (l'unité est sans importance ici)
    sk_cart = SkyCoord(x, y, z, frame=GCRS, representation_type='cartesian')
    # Représentation sphérique
    sk_sph = sk_cart.represent_as('spherical')
    # Renvoi des longitude et latitudes du point
    return sk_sph.distance.value, sk_sph.lon.value, sk_sph.lat.value


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
