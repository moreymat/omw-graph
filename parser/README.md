21/03/2014

Analyse des fichiers
====================

Introduction
------------

###Objectif
L objectif de cet analyseur est d extraire les donnees des dictionnaires OPW
(Open Multilingual Wordnet) afin de les preparer pour l injection dans neo4j.

###Description des donnees
Les donnees sont organisees de la facon suivante : 

ID-TYPE   lemma   MOT

* ID    : identifiant d un mot. Non unique, deux mots avec le meme sens ont le
* meme identifiant.
* TYPE  : type de mot - a,r,v,n
* lemma : designe un mot masculin singulier - invariable pour l instant
* MOT   : mot conserne

Les 3 champs sont separes par une tabulation.

***
Module as installer
-------------------
* nltk-3.0a3
* PyYAML-3.11
* py2neo

***
Fichiers
--------
simplefileparser.py : lit et extrais les lemmes  d'un fichier .tab
directoryparser.py : extrait les lemmes d'un ensemble de fichier .tab contenu
                     dans un dossier
extractrelations.py: extrais les relations de nltk pour l'anglais


***

Structure de donnees
--------------------

Nous avons choisi de charger les donnees dans un dictionnaire.

* key : ID-TYPE
* value : [ ( mot, langue ) ]

Exemple :

00001740-n: [ ('entitet\n', 'als'), ('0', 'als'),                   ('كَيْنُونَة\n', 'arb'), 
              ('وُجُود\n', 'arb'),    ('entité\n', 'fra'),            ('كينونة\n', 'arb'), 
              ('وجود\n', 'arb'),    ('entiteetti\n','fin'),         ('kokonaisuus\n', 'fin'), 
              ('יֵשׁוּת\n', 'heb'),    ('כל דבר שיש לו קיום\n','heb'), ('cosa\n', 'ita'), 
              ('entità\n', 'ita'),  ('実体\n', 'jpn'),              ('entidad\n','spa'), 
              ('entidade\n', 'glg'),('izaki\n', 'eus'),             ('entitate\n', 'eus'),
              ('sorkari\n', 'eus'), ('entitat\n', 'cat'),           ('3\n', 'ind'), 
              ('entiti\n', 'zsm'),  ('hakikat\n', 'zsm'),           ('kewujudan\n', 'zsm'), 
              ('sesuatu\n', 'zsm'), ('tablet\n','zsm'),             ('entitas\n', 'ind'), 
              ('entiti\n', 'ind'),  ('hakikat\n', 'ind'),           ('kewujudan\n', 'ind'),
              ('sesuatu\n', 'ind'), ('tablet\n', 'ind'),            ('entidade\n', 'por'), 
              ('ente\n', 'por'),    ('ser\n', 'por'),               ('เอกลักษณ์\n','tha')]

Python3 encode par défaut en utf-8.

Ainsi pour une clef donnee nous avons toutes les traductions correspondante des
autres langues et nous profitons de l alignement deja present.

***

Visualisation des relations
---------------------------

Les deux images Graph_1.png et Graph_2.png representent les relations entre les
mots.

###Graph_1

Ceci represente la structure de donnee utilise pour analyser les mots et met en
valeur l alignement sur l anglais - celui-ci se retrouve au milieu.

Pour l instant cette representation n est pas connexe. Rien ne relie chat et
chien entre eux.

***
Problemes rencontres
--------------------

* installation de nltk pour python3 solution version alpha de nltk
  comptatible avec python3

* py2neo pour python3 Solution pas trouver
