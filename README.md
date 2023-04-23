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

| Calepins                                                                           | Description                                    |
|:-----------------------------------------------------------------------------------|:-----------------------------------------------|
| [Force - Gravitation.ipynb](Force%20-%20Gravitation.ipynb)                         | Modélisation de la force de gravitation        |
| [Force - Géopotentiel.ipynb](Force%20-%20G%C3%A9opotentiel.ipynb)                  | Modélisation du géopotentiel terrestre         |
| [Force - Traînée atmosphérique.ipynb](Force%20-%20Tra%C3%AEn%C3%A9e%20atmosph%C3%A9rique.ipynb) | Modélisation de la traînée atmosphérique |
| [Source - Coordonnées de l'ISS.ipynb](Source%20-%20Coordonn%C3%A9es%20de%20l'ISS.ipynb) | Extraction des données sources de la NASA |
| [Visualisation - Globe.ipynb](Visualisation%20-%20Globe.ipynb)                     | Représentation graphique 3D du globe terrestre |
| [Visualisation - Planisphère.ipynb](Visualisation%20-%20Planisph%C3%A8re.ipynb)    | Représentation graphique 2D en planisphère     |

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
