# Modélisation des forces perturbatrices en orbite terrestre basse
***Application à la Station Spatiale Internationale***

Projet de Modélisation Numérique en Physique (LU2PY222) de L2 Physique de Sorbonne Université,
sous la supervision de Pacôme Delva.

*Auteurs : Damien Leprovost, Joséphine Maubian.*

<p align="center" width="100%">
  <a href="#">
    <img src="http://www.alpine-geckos.at/wp-content/uploads/2010/03/iss-modules-150x150.jpg" alt="Station Spatiale Internationale">
  </a>
</p>

## Calepins

Le calepin principal et point d'entrée du compte-rendu du projet est 
**[Modélisation des forces perturbatrices en orbite terrestre basse.ipynb](Mod%C3%A9lisation%20des%20forces%20perturbatrices%20en%20orbite%20terrestre%20basse.ipynb)**.

Les autres calepins sont des annexes explicitant les points clés du projets,
répartis en trois groupes, et sont les suivants :

| Calepins                                                                                        | Description                                                   |
|:------------------------------------------------------------------------------------------------|:-------------------------------------------------------------|
| [Modèle d'implémentation des forces](%5BAnnexe%5D%20Mod%C3%A8le%20d'impl%C3%A9mentation%20des%20forces.ipynb) | Classes de représentation de force |
| [Force de gravitation relative](%5BAnnexe%5D%20Force%20de%20gravitation%20relative%20WIP.ipynb) | Modélisation de la force de gravitation             |
| [Force géopotentielle](%5BAnnexe%5D%20Force%20g%C3%A9opotentielle%20WIP.ipynb)                  | Modélisation du géopotentiel terrestre               |
| [Force de traînée atmosphérique](%5BAnnexe%5D%20Force%20g%C3%A9opotentielle%20WIP.ipynb)        | Modélisation de la traînée atmosphérique           |
| [Lecture des données sources](%5BAnnexe%5D%20Lecture%20des%20donn%C3%A9es%20sources.ipynb)      | Extraction des données sources de la NASA                    |
| [Conversion de Coordonnées](%5BAnnexe%5D%20Conversion%20de%20Coordonn%C3%A9es.ipynb)            | Fonctions de manipulation de coordonnées             |
| [Représentation planisphérique](%5BAnnexe%5D%20Repr%C3%A9sentation%20planisph%C3%A9rique.ipynb) | Représentation graphique 2D en planisphère             |
| [Représentation 3D](%5BAnnexe%5D%20Repr%C3%A9sentation%203D.ipynb)                              | Représentation graphique 3D du globe terrestre               |


Toutes les annexes sont également accessibles par liens hypertexte depuis le calepin principal.



## Prérequis

Les packages suivants sont nécessaires pour exécuter les notebooks du projet :

| Pacakge      | Description                 |
|:-------------|:----------------------------|
| `astropy`    | astronomie et astrophysique |
| `numpy`      | calcul scientifique         |
| `matplotlib` | visualisation               |
| `pandas`     | analyse des données         |
| `plotly`     | bibliothèque graphique      |

Les packages manquants de cette liste peuvent être installés simplement avec la commande :

```python
pip install --user -r requirements.txt
```

## Suivi du projet

Pour tout suivre, tout savoir : [Tableau Trello du projet](https://trello.com/b/R6sQiqS1/groupe-2-leprovost-maubian)
