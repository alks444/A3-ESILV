# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 19:16:26 2023

@author: leroy
"""
import math
fichier_pred = open("prediction.txt", "w")

def Main():
    listeEntrainement = FichierEnListe("dataset.csv")+FichierEnListe("preTest.txt")
    listeInconnue = FichierEnListe("finalTest.txt")
    Ecrire(listeInconnue,listeEntrainement,7)
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

def TypeDesKnn(listeEntrainement,listeInconnues, k):
    distances = []
    knn = []
    nombreApp = []

    for i in listeInconnues :
        distances = [math.sqrt(sum((a - b)** 2 for a, b in zip(i, j[0]))) for j in listeEntrainement]
        distance_avec_indice = list(enumerate(distance for distance in distances))
        knn.append(sorted(distance_avec_indice, key=lambda x: x[1])[:k])

        countApparition = dict()
        for j in knn[-1] :
            if listeEntrainement[j[0]][1] in countApparition:
                countApparition[listeEntrainement[j[0]][1]]+=1
            else :
                    countApparition[listeEntrainement[j[0]][1]] = 1
        nombreApp.append(countApparition) 
    return nombreApp

def Pred(liste):
    return [max(d.keys(),key=d.get) for d in liste]

def Ecrire(listeInconnue,listeEntrainement,k):
    TypeDesVoisins = TypeDesKnn(listeEntrainement,listeInconnue,k)
    prediction = Pred(TypeDesVoisins)
    for predictions in prediction:
        fichier_pred.write(f"{int(predictions)}\n")
    return  

Main()
fichier_pred.close()