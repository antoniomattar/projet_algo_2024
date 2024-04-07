#!/usr/bin/env python3
"""
Contient l'essentiel de la classe arbre qui va être utile
pour contenir des polygônes
"""
import geo.point
import geo.polygon
import ray_casting
import os

class Arbre:

    def __init__(self,indice = -1):
        self.racine = indice
        self.feuille = [] 
    