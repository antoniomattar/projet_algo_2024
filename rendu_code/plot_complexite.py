#!/usr/bin/env python3
"""Module qui plot la complexité des algorithmes de détection d'inclusions"""

import sys
import time
import matplotlib.pyplot as plt 
import math
from tools.tycat import read_instance
import naif
import tri_aire
import gen_test

OPERATIONS_COST_CONSTANT = 1/3

def plot(liste_liste_polygones,mode):
    liste_temps = []
    liste_abcisse = []
    liste_temps_theo = []
    liste_temps_theo_2 = []
    print("Générateur utilisé ?")
    generateur_utilise = input()
    if mode in ["naif","naif_quadrant"]:
        for polygones in liste_liste_polygones:
            m = len(polygones)
            n = 0
            #Détermination du nombre moyen de sommets
            for polygone in polygones:
                n += len(polygone.points)
            n = n/m
            print("Algorithme testé : naïf")
            t1 = time.time()
            inclusions = naif.trouve_inclusions(polygones,mode)
            t2 = time.time()
            liste_abcisse.append(m)
            liste_temps.append(t2-t1)
            liste_temps_theo.append(OPERATIONS_COST_CONSTANT* m**2*n*10**(-6))
            liste_temps_theo_2.append(OPERATIONS_COST_CONSTANT*m*math.log(m)*n*10**(-6))
    else:
        for polygones in liste_liste_polygones:
            m = len(polygones)
            n = 0
            #Détermination du nombre moyen de sommets
            for polygone in polygones:
                n += len(polygone.points)
            n = n/m
            print("Algorithme testé : aire_décroissante")
            t1 = time.time()
            inclusions = tri_aire.trouve_inclusions(polygones,mode)
            t2 = time.time()
            liste_abcisse.append(m)
            liste_temps.append(t2-t1)
            liste_temps_theo.append(OPERATIONS_COST_CONSTANT*m**2*n*10**(-6))
            liste_temps_theo_2.append(OPERATIONS_COST_CONSTANT*m*math.log(m)*n*10**(-6))
    plt.plot(liste_abcisse, liste_temps, label = 'Résultat')
    plt.plot(liste_abcisse, liste_temps_theo, label = 'm^2.n')
    plt.plot(liste_abcisse, liste_temps_theo_2, label = 'mlog(m)n')
    plt.title(f"Générateur utilisé: {generateur_utilise} \n Algo utilisé: {mode}")
    plt.xlabel("Nombre de polygones")
    plt.ylabel("Temps d'éxecution en secondes")
    plt.legend()
    plt.show()

def plot_from_file_input(mode):
    """Plot les données des fichiers donnés en argument en utilisant l'algorithme donné en argument"""
    liste = []
    if len(sys.argv) < 2:
        print("Veuillez renseigner les fichiers à traiter en argument")
        return
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        liste.append(polygones)
    plot(liste,mode)


if __name__ == "__main__":
    sizes = [500, 1000, 3000, 5000, 10000]
    liste_liste_polygones = [
        list(gen_test.aligned_squares(0,0,100,200,0,i)) for i in sizes
    ]
    # for polygones in liste_liste_polygones:
    #     print(len(polygones))
    plot(liste_liste_polygones,"aire_decroissante_merge")