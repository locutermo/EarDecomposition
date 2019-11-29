import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
#Lista de colores para las orejas
colorList = [
    "orange", "blue", "red", "green", "magenta", "purple", "yellow", "black",
    "brown","silver","pink","gray",    
    ]
global count
count=0


G=nx.Graph()
G.add_edge(0,1)
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(5,6)
G.add_edge(6,7)
G.add_edge(7,8)
G.add_edge(8,9)
G.add_edge(9,10)
G.add_edge(10,11)
G.add_edge(11,12)
G.add_edge(12,13)
G.add_edge(13,14)
G.add_edge(14,15)
G.add_edge(15,16)
G.add_edge(16,17)
G.add_edge(17,18)
G.add_edge(18,19)
G.add_edge(19,20)
G.add_edge(20,21)
G.add_edge(21,22)
G.add_edge(22,23)
G.add_edge(23,24)
G.add_edge(24,25)
G.add_edge(25,26)
G.add_edge(26,27)
G.add_edge(27,28)
G.add_edge(28,29)
G.add_edge(29,30)
G.add_edge(30,31)
G.add_edge(31,32)
G.add_edge(32,33)
G.add_edge(33,34)
G.add_edge(34,35)
G.add_edge(35,36)
G.add_edge(36,37)
G.add_edge(37,38)
G.add_edge(38,39)
G.add_edge(39,40)
G.add_edge(40,41)
G.add_edge(41,42)
G.add_edge(42,43)
G.add_edge(43,44)
G.add_edge(44,45)
G.add_edge(45,46)
G.add_edge(46,47)
G.add_edge(47,48)
G.add_edge(48,49)
G.add_edge(50,51)
G.add_edge(51,0)
G.add_edge(50,3)



# house_graph
# Petersen Graph
# tutte_graph
# G= nx.tutte_graph()


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
    if not 'child' in T.node[current]:
        T.node[current]['child']=[]        

    for neighbor in G.neighbors(current):        
        if not neighbor in T.nodes():
            T.add_node(neighbor)
            T.add_edge(current,neighbor)
            T.node[neighbor]['dfsnum']=len(T.nodes())
            T.node[neighbor]['parent']=current
            T.node[current]['child'].append(neighbor)
            makeSpanningTreeDFS(G,T,neighbor)

def assignNonTreeEdgeLabel(G,T,current):
    global count
    #print(T.nodes(data=True))
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

'''
Output
'''
print("Ejecutando...")
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