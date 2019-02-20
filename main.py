# coding: utf-8 


import os
import pickle  


os.chdir(os.getcwd())


class Immeuble(): 
	"""Classe représentant un immeuble et ses différentes propriétés : nombre d'étages, boutons de l'ascenseur.
	On y trouve aussi de nombreuses méthodes qui analysent l'immeuble. """
	def __init__(self, intervalle, liste_boutons):
		""" On crée notre objet."""
		self.intervalle = intervalle  # l'intervalle représente le nombre d'étages 
		self.liste_boutons = liste_boutons
		self.liste_etages_accessibles = self.calculerEtagesAccessibles()
		self.limite = self.calculerLimiteFormule()

		# constantes
		with open("ressources/liste_nb_premiers", "rb") as f: 
			self.liste_nb_premiers = pickle.Unpickler(f).load()

	def decomposer(self, nombre_a_decomposer): 
		""" Méthode permettant de décomposer en produit de facteurs premiers un nombre donné. """
		decomposition = []
		i = 0
		while nombre_a_decomposer != 1:
			if nombre_a_decomposer % self.nb_premiers[i] == 0: 
				nombre_a_decomposer /= self.nb_premiers[i]
				decomposition.append(self.nb_premiers[i])
			else: 
				i += 1
		return decomposition

	def premiersEntreEux(self, x, y): 
		""" Méthode permettant de savoir si deux nombres donnés sont premiers entre eux. """ 
		premiers_entre_eux = True 
		dec_x = self.decomposer(x)
		dec_y = self.decomposer(y)
		for i in range(len(dec_x)):
			if dec_x[i] in dec_y: # on teste si on trouve un facteur de la décomposition commun 
				premiers_entre_eux = False 
		return premiers_entre_eux


class ImmeubleDeuxBoutonsNaturels(Immeuble): 
	""" Classe représentant un immeuble possédant deux boutons naturels, en plus du bouton 0. """
	def __init__(self, intervalle, liste_boutons):
		Immeuble.__init__(self, intervalle, liste_boutons) # on reprend le constructeur d'Immeuble

	def calculerEtagesAccessibles(self):
		""" Méthode permettant de calculer les étages accessibles de l'immeuble à partir deux deux boutons. """
		etages_accessibles = []
		bouton1, bouton2 = self.liste_boutons[1], self.liste_boutons[2]
		i = 0
		while i * bouton1 <= self.intervalle: 
			j = 0
			while i * bouton1 + j * bouton2 <= self.intervalle:
				etages_accessibles.append(i * bouton1 + j * bouton2)
				j += 1
			i += 1
		etages_accessibles = sorted(list(set(etages_accessibles)))  # pour éviter les doublons et trier la liste 
		return etages_accessibles

	def calculerLimiteFormule(self): 
		""" On calcule la 'limite' des boutons grâce à la formule f(x, y) = (x - 1)(y - 1). """
		bouton1, bouton2 = self.liste_boutons[1], self.liste_boutons[2]
		if self.premiersEntreEux(bouton1, bouton2):
			limite = (bouton1 - 1) * (bouton2 - 1)
		else: # ils ne sont pas premiers entre eux
			limite = "PAS DE LIMITE CAR PAS PREMIERS ENTRE EUX"
		return limite 

def main():
	""" Fonction prinpale du programme. """
	pass 


if __name__ == "__main__":
	main()