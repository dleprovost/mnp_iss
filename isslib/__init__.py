"""
ISS LIB
=======
Bibliothèque de support pour les notebooks du projet de Modélisation des forces
perturbatrices en orbite terrestre basse.


sous-packages
-------------
coordinates
    fonctions de conversions de repères et coordonnées
position
    classe principale de gestion des positions de l'ISS
visualization
    contextes de représentation graphiques des données


Par commodité, les classes `Force`, `ForceSet` et `ISS_Position` sont chargées
dans le package principal, en tant qu'éléments centraux de la bibliothèque.
"""
import isslib.coordinates as coordinates  # noqa: F401
import isslib.visualization as visualization  # noqa: F401
from isslib.position import ISS_Position  # noqa: F401
from isslib.force import Force, ForceSet  # noqa: F401
