"""
isslib.position
===============

Fournit la classe principale de gestion des positions de l'ISS.
"""
import os
import re
import requests

import numpy as np
import pandas as pd


class ISS_Position:
    """Classe d'extraction des données de position de l'ISS."""
    def __init__(self, filename=None, force_download=False):
        """Coordonnées de l'ISS extraites d'un fichier source.

        La lecture s'effectue depuis un fichier local si spécifié. Dans le cas
        contraire, le fichier est téléchargé depuis le stockage S3 de la NASA
        s'il n'existe pas déjà un téléchargement local de ce fichier.

        Paramètres:
        - filename: le fichier local à utiliser comme source de données.
        - force_download: force le téléchargement du fichier même s'il existe
                          déjà en local.
        """
        if not filename:
            # Pas de fichié spécifié, génère le nom de fichier local du jour
            datetime = pd.Timestamp.today().strftime('%Y%m%d')
            filename = os.path.join("data", f"ISS.OEM_J2K_EPH_{datetime}.txt")
            # Télécharge le fichier du jour si absent ou téléchargement forcé
            if force_download or not os.path.exists(filename):
                self.__download(filename)
        # Parse le contenu du fichier
        self.__parse_source(filename)

    def __download(self, filename):
        """Télécharge le fichier de coordonnées de l'ISS du jour."""
        # Permalien du fichier depuis le bucket public de la NASA
        url = ("https://nasa-public-data.s3.amazonaws.com/iss-coords/current/"
               "ISS_OEM/ISS.OEM_J2K_EPH.txt")
        # Téléchargement en mémoire du fichier
        myfile = requests.get(url)
        # Ecriture en fichier local
        with open(filename, 'wb') as file:
            file.write(myfile.content)

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
        meta = slice(source_lines.index('META_START\n')+1,
                     source_lines.index('META_STOP\n'))
        # Enregistrement des métadonnées dans un dictionnaire
        self.meta = {
            key.strip(): pd.to_datetime(value.strip())
            if key.strip().endswith('_TIME') else value.strip()
            for line in source_lines[meta]
            for (key, value) in [line.split('=', 1)]
        }

    def __parse_source_comments(self, source_lines):
        """Extraction des commentaires du fichier."""
        # Sélection des lignes de commentaires
        comments = [line for line in source_lines
                    if line.startswith("COMMENT")]
        # Index de la dernière ligne de commentaires
        self.__last_comment_index = source_lines.index(comments[-1])
        # Enregistrement des commentaires dans une liste
        self.comments = [comment[7:].strip() for comment in comments]
        # Recherche par motif des metadonnées inclues dans les commentaires
        motif = r"([A-Z_]+)=([0-9\.]+)"
        md_comments = re.findall(motif, '\n'.join(self.comments))
        # Ajout de ces métadonnées aux dictonnaire des métadonnées
        self.meta.update({match[0]: float(match[1]) for match in md_comments})

    def __parse_data(self, filename):
        """Extraction des données du fichier."""
        # Enregistrement des données dans un DataFrame à partir des lignes
        # suivant le dernier commentaire
        columns = ['datetime', 'x', 'y', 'z', 'vx', 'vy', 'vz']
        self.data = pd.read_csv(filename, sep=" ", names=columns,
                                skiprows=self.__last_comment_index+1,
                                parse_dates=[0], infer_datetime_format=True)
        # Ajoute les annotations de poussée
        self.__add_thrust_metadata()

    def __add_thrust_metadata(self):
        """Ajout des annotation de poussé et épisodes de poussée."""
        # Les enregistrements datant de deux secondes après leur précédent
        # sont marqués en tant que poussée
        self.data['on_thrust'] = np.isclose(
            self.data.diff().datetime.dt.total_seconds(), 2)
        # Initialisation des valeurs d'épisode de poussée
        self.__current_state = self.data.iloc[0]['on_thrust']
        self.__current_tid = 0
        # Un épsiode est une séquence contiguë d'état de poussée
        self.data['thrust_episode'] = self.data['on_thrust'].apply(
            self.__thrust_episode)
        # Suppression des marqueurs inutiles
        del self.__current_state, self.__current_tid

    def __thrust_episode(self, on_thrust):
        """Parours de proche en proche des états de poussée."""
        # Si l'état actuel est différent du dernier état enregistré
        if on_thrust != self.__current_state:
            # Changement d'état et d'identifiant d'épisode.
            self.__current_state = on_thrust
            self.__current_tid += 1
        # Renvoi de l'indentifiant actuel
        return self.__current_tid

    def get_metadata(self, key=None):
        """Accès aux métadonnées.

        Si une clé est spécifiée et qu'elle existe dans les métadonnées,
        retourne sa valeur.
        Si aucune clé n'est fournie, retourne l'ensemble des métadonnées
        en utilisant un DataFrame (pour son rendu élégant à l'affichage).
        """
        if key:
            return self.meta.get(key)
        else:
            return pd.DataFrame(self.meta.values(), self.meta.keys(),
                                ['Metadata'])

    def get_comments(self):
        """Retourne les commentaires en tant que bloc de texte."""
        return '\n'.join(self.comments)

    def get_data(self):
        """Retourne le DataFrame des données"""
        return self.data

    def __repr__(self):
        """Représentation en string de l'objet."""
        start, stop = self.meta['START_TIME'], self.meta['STOP_TIME']
        return fr"ISS coordinates from {start} to {stop}"

    def _repr_html_(self):
        """Représentation riche en HTML de l'objet."""
        # Représentation en string des datetimes de début et de fin des données
        start_date = self.meta['START_TIME'].strftime('%d/%m/%Y')
        stop_date = self.meta['STOP_TIME'].strftime('%d/%m/%Y')
        # Représentation HTML avec le tableau des épisodes de poussées
        return (r"<div style='border:4px #eee outset;background:#fcfcfc;"
                r"padding:1px 10px 10px'><h4 style='padding-left:10px'>"
                fr"Coordonnées de l'ISS du {start_date} au {stop_date}</h4>"
                fr"{self.__repr_thrust_episode()}</div>")

    def __repr_thrust_episode(self):
        """Représentation des épisodes de poussées en tant que DataFrame."""
        # Group-by par épisode
        gb = self.data.groupby('thrust_episode')
        # Dataframe des dates de début et de fin de chaque épisode
        df = pd.DataFrame([gb.min().datetime.rename('Début'),
                           gb.max().datetime.rename('Fin')]).T
        # Durée des épisodes
        df['Durée'] = df['Fin'] - df['Début']
        # Réécriture de l'index pour expliciter les épisodes
        df.index = df.index.map(
            lambda x: f"Episode {x} : "
            + ("Poussée moteurs" if x % 2
               else "Mouvement libre")).rename(None)
        return df.to_html()
