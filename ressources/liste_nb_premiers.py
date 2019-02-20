# coding: utf-8 


import os 
import pickle 
import math


os.chdir(os.getcwd())


def afficherNombrePremiers():
	with open("liste_nb_premiers", "rb") as f:
		print(pickle.Unpickler(f).load())


def listerNombrePremiers(nb_max):
	""" Fonction qui permet de lister les nombres premiers de 2 jusqu'à un nombre maximum donné. """
	liste_nb_premiers = [2]
	for nombre_etudie in range(3, nb_max + 1):
		nb_premier = True
		for diviseur in range(2, nombre_etudie - 1):
			if nombre_etudie % diviseur == 0:
				nb_premier = False 
		if(nb_premier):
			liste_nb_premiers.append(nombre_etudie)
	return liste_nb_premiers


def main():
	""" Fonction principale du programme. """
	liste_nb_premiers = listerNombrePremiers(10000)
	with open("liste_nb_premiers", "wb") as f:
		pickle.Pickler(f).dump(liste_nb_premiers)
	afficherNombrePremiers()

if __name__ == "__main__":
	main()