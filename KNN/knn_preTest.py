# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 19:16:26 2023

@author: leroy
"""
import math
import random as rd
import matplotlib.pyplot as plt

def Main():
    listeEntrainement = FichierEnListe("dataset.csv")+FichierEnListe("preTest.txt")
    rd.shuffle(listeEntrainement)
    listeInconnue,listeEntrainement = listeEntrainement[:400],listeEntrainement[400:]
    pourcentages = testK(listeInconnue,listeEntrainement)
    print(f"Le k avec le plus haut % de réussite est le k={pourcentages.index(max(pourcentages))+1} avec un taux de réussite de {max(pourcentages)}%")
    affichageReussite(pourcentages)
    return 

def FichierEnListe(chemin_d_acces):
    fichier = open(chemin_d_acces,"r")
    lignes = [line.strip("\n").split(';') for line in fichier]
    for fleur in lignes :
        
        for i in range(len(fleur)):
            fleur[i] = float(fleur[i])
        if len(fleur)==7 :
            fleur[0],fleur[1] = fleur[:len(fleur)-1],fleur[-1]
            del(fleur[2:])
    fichier.close()
    return lignes


def TypeDesKnn(fleurEntrainement,fleurInconnues, k):
    distances = []
    knn = []
    nombreApp = []

    for i in fleurInconnues :
        distances = [math.sqrt(sum((a - b)** 2 for a, b in zip(i[0], j[0]))) for j in fleurEntrainement]
        distance_avec_indice = list(enumerate(distance for distance in distances))
        knn.append(sorted(distance_avec_indice, key=lambda x: x[1])[:k])
        countApparition = dict()
        for j in knn[-1] :
            if fleurEntrainement[j[0]][1] in countApparition:
                countApparition[fleurEntrainement[j[0]][1]]+=1
            else :
                    countApparition[fleurEntrainement[j[0]][1]] = 1
        nombreApp.append(countApparition) 
    return nombreApp

def Pred(liste):
    return [max(d.keys(),key=d.get) for d in liste]

def Verification(fleurInconnues,prediction):
    vrai,faux = 0,0
    if len(fleurInconnues)!=len(prediction):
        return 0
    for i in range(len(prediction)):
        if prediction[i]==fleurInconnues[i][1]:
            vrai +=1
        else : 
            faux+=1
    return vrai/len(prediction)*100

def testK(listeInconnue,listeEntrainement):
    pourcentages = []
    for k in range(1,10):
        TypeDesVoisins = TypeDesKnn(listeEntrainement,listeInconnue,k)
        prediction = Pred(TypeDesVoisins)

        # for predictions in prediction:
        #     fichier_pred.write(f"{int(predictions)}\n")

        pourcentages.append(Verification(listeInconnue,prediction))
    return pourcentages   
        
def affichageReussite(pourcentages):
    plt.plot(range(1,len(pourcentages)+1),pourcentages)
    plt.show()
    return

Main()