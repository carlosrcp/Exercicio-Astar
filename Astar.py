import numpy as np

distanceTable = []
for d in range(14):
  distanceTable.append([0] * 14)
realDistanceTable = []
for d in range(14):
  realDistanceTable.append([0] * 14)

lines = [None] *4

azul = 0
amarela = 1
vermelha = 2
verde = 3

minCost = [-1]*14
class State:
  def __init__(self, station, line, distance, target, path):
    self.station = station
    self.line = line
    self.distance = distance
    self.target = target
    self.path = path
  
  def GetF(self):
    return self.distance + GetDistance(self.station, self.target)

class PriorityQueue:
  def __init__(self, station, line):
    self.station = station
    self.line = line

    self.states = []
  
  def Add(self, newState):
    self.states.append(newState)
  
  def Top(self):
    topState = self.states[0]
    for s in self.states:
      if s.GetF() < topState.GetF():
        topState = s
    
    return topState
  
  def PopTop(self):

    popIndex = 0    
    topState = self.states[0]
    for i in range(len(self.states)):
      s = self.states[i]
      if s.GetF() < topState.GetF():
        topState = s
        popIndex = i

    self.states.pop(popIndex)

def SetDistance(e1, e2, v):    
  distanceTable[e1][e2] = v
  distanceTable[e2][e1] = v

def GetDistance(e1, e2):
  if e1==e2:
    return 0
  else:
    return distanceTable[e1][e2]

connections = []
#print(connections)
for c in range(14):
  connections.append([])

def SetRealDistance(e1, e2, v):    
  realDistanceTable[e1][e2] = v
  realDistanceTable[e2][e1] = v

  connections[e1].append(e2)
  connections[e2].append(e1)

def GetRealDistance(e1, e2):
  if e1==e2:
    return 0
  else:
    return realDistanceTable[e1][e2]


def Load():
  lines[azul] = []
  lines[amarela] = []
  lines[vermelha] = []
  lines[verde] = []

  lazul = []
  #azul
  lines[azul].append(0)
  lines[azul].append(1)
  lines[azul].append(2)
  lines[azul].append(3)
  lines[azul].append(4)
  lines[azul].append(5)

  #amarela
  lines[amarela].append(6)
  lines[amarela].append(4)
  lines[amarela].append(7)
  lines[amarela].append(8)
  lines[amarela].append(1)
  lines[amarela].append(9)

  #vermelha
  lines[vermelha].append(10)
  lines[vermelha].append(8)
  lines[vermelha].append(2)
  lines[vermelha].append(12)

  #verde
  lines[verde].append(11)
  lines[verde].append(7)
  lines[verde].append(3)
  lines[verde].append(12)
  lines[verde].append(13)

  dists = [10, 18.5, 24.8, 36.4, 38.8, 35.8, 25.4, 17.6, 9.1, 16.7, 27.3, 27.6, 29.8,
      8.5, 14.8, 26.6, 29.1, 26.1, 17.3, 10, 3.5, 15.5, 20.9, 19.1, 21.8,
      6.3, 18.2, 20.6, 17.6, 13.6, 9.4, 10.3, 19.5, 19.1, 12.1, 16.6,
      12, 14.4, 11.5, 12.4, 12.6, 16.7, 23.6, 18.6, 10.6, 15.4,
      3, 2.4, 19.4, 23.3, 28.2, 34.2, 24.8, 14.5, 17.9,
      3.3, 22.3, 25.7, 30.3, 36.7, 27.6, 15.2, 18.2,
      20, 23, 27.3, 34.2, 25.7, 12.4, 15.6,
      8.2, 20.3, 16.1, 6.4, 22.7, 27.6,
      13.5, 11.2, 10.9, 21.2, 26.6,
      17.6, 24.2, 18.7, 21.2,
      14.2, 31.5, 35.5,
      28.8, 33.6,
      5.1
  ]

  k = 0
  for i in range(14):    
      for j in range(i+1,14):    
        SetDistance(i,j,dists[k])
        k+=1
  
  # distancias reais
  SetRealDistance(0,1,10)

  SetRealDistance(1,2,8.5)
  SetRealDistance(1,8,10)
  SetRealDistance(1,9,3.5)
  
  SetRealDistance(2,3,6.3)
  SetRealDistance(2,8,9.4)
  SetRealDistance(2,12,18.7)
  
  SetRealDistance(3,4,13)
  SetRealDistance(3,7,15.3)
  SetRealDistance(3,12,12.8)

  SetRealDistance(4,5,3)
  SetRealDistance(4,6,2.4)
  SetRealDistance(4,7,30)

  SetRealDistance(7,8,9.6)
  SetRealDistance(7,11,6.4)

  SetRealDistance(8,10,12.2)

  SetRealDistance(12,13,5.1)

def main():
  Load()
  
  bald = 30.0 * 4.0/60.0

  Q = PriorityQueue(0,0)
  
  startStation = -1
  endStation = -1
  while startStation < 0 or startStation > 13:
    startStation = int(input('Numero da estacao INICIAL: ')) - 1  
  
  while endStation < 0 or endStation > 13:
    endStation = int(input('Numero da estacao FINAL: ')) - 1
  
  startState = State(startStation, -1, 0, endStation, [])

  Q.Add(startState)
  
  breaksteps = 0

  while (Q.Top().station != endStation):  
    print("Passo: ", breaksteps, "\nMelhor estacao: ", Q.Top().station +1, "\nF:", Q.Top().GetF())
    
    print("Estacoes possiveis:")
    for s in Q.states:
      print(s.station+1, " F: ", "{:.1f}".format(s.GetF()))

    if breaksteps > 50: # contador de quantos passos, se chegar num limite para para ficar preso no while
      print("limite de passos alcancado")
      break
    breaksteps +=1
        
    top = Q.Top()
      
    Q.PopTop()    

    s = top.station
    l = top.line

    newpath = []

    for i in top.path:
      newpath.append(i)
    newpath.append(s)

    for i in range(len(connections[s])):
      
      con = connections[s][i]
      if con == s:
        continue
      
      d = GetRealDistance(s, con)
      if l != -1 and not(con in lines[l]): 
        newStation = -1
          
        for j in range(len(lines)):
          if l != j and not(s in lines[j]):
            newStation = j            
        
        if newStation!=-1:
          cost = d + top.distance + bald
          if minCost[con] == -1 or minCost[con] > cost:
            minCost[con] = cost
            Q.Add(State(con, newStation, d + top.distance + bald, endStation, newpath))
        else:
          print("ERRO")        
      else:
        cost = d + top.distance
        if minCost[con] == -1 or minCost[con] > cost:
          minCost[con] = cost
          Q.Add(State(con, l, d + top.distance, endStation, newpath))    
    
    print("")

  print("Caminho:")
  for p in Q.Top().path:
    print(p+1)

  print("Fim")


main()
