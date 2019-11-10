# 20106911 Minjae Park
# Finding an Ear decomposition of 2(-edge)-connected graph

import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

colorList = [
    "orange", "blue", "red", "green", "magenta", "purple", "yellow", "black"
    "brown","silver","pink","gray",    
    ]
global count
count=0

'''
Input Graph
'''
# Complete Graph
# G=nx.complete_graph(6)


# Non 2-connected (but 2-edge-connected) Graph
'''
G=nx.Graph()
G.add_edge(0,1)
G.add_edge(7,0)
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(5,6)
G.add_edge(6,7)
G.add_edge(1,7)
G.add_edge(2,6)
G.add_edge(3,5)
G.add_edge(1,5)
'''



# Petersen Graph
G = nx.tetrahedral_graph()
'''
Testing 2-edge-connectivity
'''
P = nx.Graph(G)
#print(G.edges())
for e in P.edges():         
    H=nx.Graph(G)
    
    G.remove_edge(*e)    
    if not nx.is_connected(G):
        raise SystemExit("G is not 2-edge-connected. This algorithm is not valid.")
  
    G=H

'''
Testing 2-connectivity
'''
for v in P.nodes():    
    H=nx.Graph(G)
    G.remove_node(v)
    if not nx.is_connected(G):
        print "G is not 2-connected. The result is not an open ear decomposition."
    G=H
'''
Algorithm for Finding an Ear Decomposition
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
tiempo = instanteFinal - instanteInicial # Devuelve un objeto timedelta
segundos = tiempo.microseconds
print("Segundos: ",segundos," microsegundos")

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