"""
isslib.force
============

Fournit la classe abstraite de modélisation des forces
et la classe de jeu de forces.
"""
from abc import ABC, abstractmethod
import sys


import numpy as np


class Force(ABC):
    """Classe abstraite de modélisation d'une force."""

    # Le décorateur property permet de définir une propriété en lecture-seule.
    @property
    def G(self):
        """Constante universelle de gravitation."""
        return 6.67430e-20  # km^3 kg^−1 s^−2

    @property
    def earth_mass(self):
        """Masse de la Terre."""
        return 5.972e24  # kg

    @property
    def earth_radius(self):
        """Rayon moyen volumétrique de la Terre."""
        return 6371  # km

    @property
    @abstractmethod
    def name(self):
        """Nom de la force sous forme de string."""
        raise NotImplementedError(self.name)

    @property
    @abstractmethod
    def formula(self):
        """Expression de la force au format LaTeX."""
        raise NotImplementedError(self.formula)

    @abstractmethod
    def acceleration(self, u, t):
        """Accélération de la force appliquée au vecteur spécifié."""
        raise NotImplementedError(self.acceleration)

    def acc_norm(self, u, t=0):
        """Norme de l'accélération appliquée au vecteur spécifié."""
        # Application de l'accélération au vecteur
        a = self.acceleration(u, t)
        # Retourne la norme du vecteur
        return np.linalg.norm(a)

    def __repr__(self):
        """Représentation de la force sous forme de string."""
        return self.name

    def _repr_latex_(self):
        """[Jupyter] Représentation de la force au format LaTeX."""
        return fr"{self.name} : $\displaystyle {self.formula}$"


class ForceSet():
    """Classe de jeu de forces à appliquer à une particule."""
    def __init__(self, forces):
        """Instancie la classe à partir d'une liste de forces."""
        self.forces = forces

    def derivee(self, u, t):
        """Calcule la dérivée à partir d'un vecteur de coordonnées.

        Dans un repère cartésien tridimensionnel, le vecteur de
        coordonnées est `[x, y, z, dx, dy, dz]`.
        """
        # Vecteur des coordonnées sources
        x, y, z, vx, vy, vz = u
        # Les vitesses sont les dérivées des positions
        dx, dy, dz = vx, vy, vz
        # Les acclélérations sont définies par les EDO de chaque force
        dvx, dvy, dvz = np.sum([force.acceleration(u, t)
                                for force in self.forces], axis=0)
        # Retourne les dérivées
        return np.array([dx, dy, dz, dvx, dvy, dvz])

    def magnitude(self, u):
        """Calcul des ordres de grandeur des forces à des coordonnées."""
        # Retourne un dictonnaire du log10 de chaque force aux coordonnées
        return {str(force): np.log10(force.acc_norm(u))
                for force in self.forces}

    def solve(self, t_start, t_stop, t_step, coords, interrupt=None):
        """Résolution d'équation différentielle par la méthode de Runge-Kutta.

        Attributs:
            t_start:   valeur de départ de la variable temporelle
            t_stop:    valeur d'arrivée de la variable temporelle
            t_step:    intervalle de temps entre deux calculs
            coords:    coordonnées initiales
            interrupt: fonction pour interrompre prématurément le calcul (par
                       exemple, pour éviter des calculs inutiles une fois les
                       données hors-limites)
         """
        # Création du tableau temps
        num_points = int((t_stop - t_start) / t_step) + 1
        t = np.linspace(t_start, t_stop, num_points)
        # Initialisation du tableau solution
        v = np.empty((len(coords), num_points))
        # Condition initiale
        v[:, 0] = coords
        # Boucle for des variables de la méthode
        for i in range(num_points - 1):
            d1 = self.derivee(v[:, i], t[i])
            d2 = self.derivee(v[:, i] + t_step / 2 * d1, t[i] + t_step / 2)
            d3 = self.derivee(v[:, i] + t_step / 2 * d2, t[i] + t_step / 2)
            d4 = self.derivee(v[:, i] + t_step * d3,  t[i] + t_step)
            v[:, i + 1] = v[:, i] + t_step / 6 * (d1 + 2*d2 + 2*d3 + d4)
            if interrupt and interrupt(v[:, i+1]):
                t_inter = t_start + i*t_step
                print(f"Interruption du calcul de solution à t={t_inter}!",
                      file=sys.stderr)
                v[:, i+2:] = np.nan
                break
        # Retourne des tableaux des temps et des solutions
        return t, v

    def __repr__(self):
        """Représentation du jeu de forces sous forme de string."""
        return fr"ForceSet[{', '.join(str(force) for force in self.forces)}]"
