import networkx as nx
import mythread
import TreeEdgeThread
import matplotlib.pyplot as plt
from datetime import datetime
#Lista de colores para las orejas
colorList = [
    "orange", "blue", "red", "green", "magenta", "purple", "yellow", "black",
    "brown","silver","pink","gray",    
    ]
global count
count=0

G= nx.tutte_graph()
P = nx.Graph(G)
for e in P.edges():         
    H=nx.Graph(G)
    
    G.remove_edge(*e)    
    if not nx.is_connected(G):
        raise SystemExit("G is not 2-edge-connected. This algorithm is not valid.")
  
    G=H

for v in P.nodes():    
    H=nx.Graph(G)
    G.remove_node(v)
    if not nx.is_connected(G):
        print("G is not 2-connected. The result is not an open ear decomposition.")
    G=H

'''
Algoritmo para encontrar una descomposicion de oreja 
'''
def makeSpanningTree(G,root):
    T=nx.Graph()
    T.add_node(root)
    T.node[root]['dfsnum']=len(T.nodes())
    makeSpanningTreeDFS(G,T,root)
    return T

def makeSpanningTreeDFS(G,T,current):
    threads = []
    i = 1 
    if not 'child' in T.node[current]:
        T.node[current]['child']=[]        
    
    for neighbor in G.neighbors(current):        
        if not neighbor in T.nodes():         
            hilo =  TreeEdgeThread.myThread(G,neighbor,T,current,1,"Hilo "+str(i))            
            threads.append(hilo)            
            hilo.start()                        
            i+=1

                                
    for x in threads:         
        x.join()
    
    print("Finalizo hilos principales")


    

def assignNonTreeEdgeLabel(G,T,current):    
    global count    
    subrootdfsnum=T.nodes(data=True)[current]['dfsnum']
    for node,nodeattr in T.nodes(data=True):
        if nodeattr['dfsnum']>subrootdfsnum:
            if ((current,node) in G.edges() or (node,current) in G.edges()) and not ((current,node) in T.edges() or (node,current) in T.edges()):
                G[current][node]['oreja']=count                
                count+=1    
    for neighbor in T.nodes(data=True)[current]['child']:
        assignNonTreeEdgeLabel(G,T,neighbor)

def assignTreeEdgeLabel(G,T,current):
    if not T.nodes(data=True)[current]['child']:
        label=[]
        for neighbor in G.neighbors(current):
            if 'oreja' in G[current][neighbor]:
                label.append(G[current][neighbor]['oreja'])
        if 'parent' in T.node[current]:
            parent=T.node[current]['parent']
            G[current][parent]['oreja']=min(label)
            
    else:
        for neighbor in T.nodes(data=True)[current]['child']:
            if not 'oreja' in T.node[neighbor]:
                assignTreeEdgeLabel(G,T,neighbor)
        if 'parent' in T.node[current]:
            parent=T.node[current]['parent']
            label=[]
            for neighbor in G.neighbors(current):
                if 'oreja' in G[current][neighbor]:
                    label.append(G[current][neighbor]['oreja'])
            G[current][parent]['oreja']=min(label)


instanteInicial = datetime.now()

T=makeSpanningTree(G,0)
assignNonTreeEdgeLabel(G,T,0)
assignTreeEdgeLabel(G,T,0)

instanteFinal = datetime.now()
tiempo = instanteFinal - instanteInicial 
segundos = tiempo.microseconds
print("Tiempo Transcurrido: ",segundos," microsegundos")
archivo = open("mediciones_paralelo.txt", "at")
print("Tiempo Transcurrido: "+str(segundos)+" microsegundos")
archivo.write(str(segundos)+'\n')
archivo.close()

'''
Output
'''
print("Ejecutando...")
'''
pos=nx.circular_layout(G)
ear_list=[[] for i in range(count+1)]

for (x,y) in G.edges():
   ear=G[x][y]['oreja']
   ear_list[ear].append((x,y))
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_labels(G,pos)
for i in range(len(ear_list)):
    nx.draw_networkx_edges(G,pos,edgelist=ear_list[i],edge_color=colorList[i%len(colorList)],alpha=0.5,width=3)
nx.draw_networkx_edge_labels(G,pos,alpha=0.5)

plt.show()
'''