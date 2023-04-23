"""
ISS LIB
=======
Bibliothèque de support pour les notebooks du projet de Modélisation des forces
perturbatrices en orbite terrestre basse.

12345678901234567890123456789012345678901234567890123456789012345678901234567890


sous-packages
-------------
coordinates
    fonctions de conversions de repères et coordonnées
position
    classe principale de gestion des positions de l'ISS
visualization
    contextes de représentation graphiques des données


Par commodité, la classe `ISS_Position` est chargée dans le package principal.
"""
import isslib.coordinates as coordinates  # noqa: F401
import isslib.visualization as visualization  # noqa: F401
from isslib.position import ISS_Position  # noqa: F401
