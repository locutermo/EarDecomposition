#!/usr/bin/python

import threading
import time
 
exitFlag = 0

class myThread (threading.Thread):
   def __init__(self,G, neighbor, T,current,number,name):
      threading.Thread.__init__(self)
      self.G = G 
      self.neighbor = neighbor
      self.T = T
      self.number = number
      self.current = current
      self.name = name 
   def run(self):      
      mythreads = []
      print("---"+self.name+" - Ciclo: "+str(self.number)+"\n")
      asignNode(self.T,self.neighbor,self.current)            
      if not 'child' in self.T.node[self.neighbor]: self.T.node[self.current]['child'] = []
      for myneighbor in self.G.neighbors(self.neighbor):
         if not myneighbor in self.T.nodes():
            hilo = myThread(self.G,myneighbor,self.T,self.neighbor,self.number+1,"-----"+self.name)      
            mythreads.append(hilo)
            hilo.start()
      for mythread in mythreads:
         mythread.join()
      print("Finalizo ")

      
             
def asignNode(T,neighbor,current):
   if not 'child' in T.node[current]:
        T.node[current]['child']=[]      
   T.add_node(neighbor)
   T.add_edge(current,neighbor)
   T.node[neighbor]['dfsnum']=len(T.nodes())
   T.node[neighbor]['parent']=current
   T.node[current]['child'].append(neighbor) 
   print "================================\n"
   print ("Datos del nodo: "+ str(current)+"\n")
   print("Hijo ",T.node[current]['child'])
   print("Neightbor: ",neighbor)
   print "*==============================*\n"
                     
   



