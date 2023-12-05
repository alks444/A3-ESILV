# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 15:18:47 2023

@author: leroy
"""

from ortools.sat.python import cp_model

#%% Exercice 1 : Coloration 

def SimpleSat_Progm():
    
    #creer le modele :
    model = cp_model.CpModel()
    
    #creer variables :
    kBase = 3 # Nombre de couleurs !=
    
    nt = model.NewIntVar(1,kBase,'nt')
    wa = model.NewIntVar(1,kBase,'wa')
    q = model.NewIntVar(1,kBase,'q')
    nsw = model.NewIntVar(1,kBase,'nsw')
    v = model.NewIntVar(1,kBase,'v')
    sa = model.NewIntVar(1,kBase,'sa')
    t = model.NewIntVar(1,kBase,'t')
    
    #creer les contraintes :
    model.Add(sa!=wa)
    model.Add(sa!=nt)
    model.Add(sa!=q)
    model.Add(sa!=nsw)
    model.Add(sa!=v)
    model.Add(q!=nt)
    model.Add(q!=nsw)
    
    #creer le solver :
    solver = cp_model.CpSolver()
    statut = solver.Solve(model)
    
    
    if statut == cp_model.FEASIBLE or statut==cp_model.OPTIMAL :
        print('sa= %i' %solver.Value(sa))
        print('wa= %i' %solver.Value(wa))
        print('nt= %i' %solver.Value(nt))
        print('nsw= %i' %solver.Value(nsw))
        print('v= %i' %solver.Value(v))
        print('q= %i' %solver.Value(q))
        print('t= %i' %solver.Value(t))



SimpleSat_Progm()

#%% Exercice 2 : Message crypté :
    
def MessageCrypte():
    model = cp_model.CpModel()
    
    kBase = 10
    s = model.NewIntVar(1,kBase-1,'s')
    e = model.NewIntVar(1,kBase-1,'e')
    n = model.NewIntVar(0,kBase-1,'n')
    d = model.NewIntVar(0,kBase-1,'d')
    m = model.NewIntVar(0,kBase-1,'m')
    o = model.NewIntVar(0,kBase-1,'o')
    r = model.NewIntVar(0,kBase-1,'r')
    y = model.NewIntVar(0,kBase-1,'y')
    
    letters = [s,e,n,d,m,o,r,y]
    assert kBase >=len(letters)
    
    model.AddAllDifferent(letters)
    model.Add(d+e + kBase*(n+r) + kBase**2*(e+o) + kBase**3*(s+m) == y + kBase*e + kBase**2*n + kBase**3*o + kBase**4+m)
    
    solver = cp_model.CpSolver()
    statut = solver.Solve(model)
    
    if statut == cp_model.FEASIBLE or statut==cp_model.OPTIMAL :
        print('s= %i' %solver.Value(s))
        print('e= %i' %solver.Value(e))
        print('n= %i' %solver.Value(n))
        print('d= %i' %solver.Value(d))
        print('m= %i' %solver.Value(m))
        print('o= %i' %solver.Value(o))
        print('r= %i' %solver.Value(r))
        print('y= %i' %solver.Value(y))

MessageCrypte()
        

#%% Exercice 3 : Le problème des 8 reines :
    
def ProblemeDesReines(boardSize):
    model = cp_model.CpModel()
    
    configuration = [model.NewIntVar(0,boardSize-1, "d%i" %i) for i in range(8)]
    
    model.AddAllDifferent(configuration)
    
    for i in range (boardSize):
        diag1,diag2 = [],[]
        
        for j in range(boardSize):
            q1 = model.NewIntVar(0,2*(boardSize-1), 'diag1_%i' %i)
            diag1.append(q1)
            model.Add(q1 == configuration[j]+ j)
            
            q2 = model.NewIntVar(-(boardSize-1), boardSize-1, 'diag1_%i' %i)
            diag2.append(q2)
            model.Add(q2 == configuration[j] - j)
        model.AddAllDifferent(diag1)
        model.AddAllDifferent(diag2)
            
        
        solver = cp_model.CpSolver()
        afficher_solution = SolutionPrinter(configuration)
        statut = solver.SearchForAllSolutions(model, afficher_solution)
        
class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solutionCount = 0
        
    def OnSolutionCallback(self):
        self.solutionCount =+1
        for v in self.__variables:
            print('%s = %i' %(v,self.Value(v)), end = ' ')
        print()
        
    def solutionCount(self):
        return self.__solutionCount
            
ProblemeDesReines(8)


#%% Exercice 5 :
def Sudoku():
    model = cp_model.CpModel()
    
    longueurCarre = 3
    longueurLigne = longueurCarre**2
    
    grille_depart = [
        [0, 6, 0, 0, 5, 0, 0, 2, 0],
        [0, 0, 0, 3, 0, 0, 0, 9, 0],
        [7, 0, 0, 6, 0, 0, 0, 1, 0],
        [0, 0, 6, 0, 3, 0, 4, 0, 0],
        [0, 0, 5, 0, 7, 0, 1, 0, 0],
        [0, 0, 4, 0, 9, 0, 8, 0, 0],
        [0, 4, 0, 0, 0, 1, 0, 0, 6],
        [0, 3, 0, 0, 0, 8, 0, 0, 0],
        [0, 2, 0, 0, 4, 0, 0, 5, 0],
    ]
    
    grid = {}
    for i in range(longueurLigne):
        for j in range(longueurLigne):
            grid[(i, j)] = model.NewIntVar(1, longueurLigne, "grid %i %i" % (i, j))


    #Difference sur les lignes
    for i in range(longueurLigne):
        model.AddAllDifferent(grid[(i, j)] for j in range(longueurLigne))
    #Difference sur les colones
    for j in range(longueurLigne):
       model.AddAllDifferent(grid[(i, j)] for i in range(longueurLigne))
    
    #Difference sur les carrés
    for i in range(longueurCarre):
        for j in range(longueurCarre):
            one_cell = []
            for di in range(longueurCarre):
                for dj in range(longueurCarre):
                    one_cell.append(grid[(i * longueurCarre + di, j * longueurCarre + dj)])

            model.AddAllDifferent(one_cell)

    # Initialisation des valeurs
    for i in range(longueurLigne):
        for j in range(longueurLigne):
            if grille_depart[i][j]:
                model.Add(grid[(i, j)] == grille_depart[i][j])

    # Solver & Print
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        for i in range(longueurLigne):
            print([int(solver.Value(grid[(i, j)])) for j in range(longueurLigne)])



  

  
Sudoku() 
    