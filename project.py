from random import randint

import networkx as nx
import matplotlib.pyplot as plt

class digraph():
    def __init__(self,adjMat=[],n=0,m=0,directed=True):
        self.n=n
        self.m=m
        self.K=[-1 for _ in range(n)]
        if adjMat==[]:
            self.G=self.randomDigraph(n,m,directed)

    #Input : n the nb of vertices, m the nb of arcs
    #Output : An adjacency matrix G, s.t G[u][v]==1 => uv in A            
    def randomDigraph(self,n,m,directed=True):
        G=[[0 for _ in range(n)] for _ in range(n)]
        k=0
        while k<m:
            u=randint(0,n-1)
            v=randint(0,n-1)
            if u!=v and G[u][v]==0:
                G[u][v]=1
                if not(directed):
                    G[v][u]=1
                k+=1
        return G

    #Input : a vertex u
    #Output : an array of indexes of the neighbours of u
    def neighbours(self,u):
        N=[]
        for v in range(len(self.G[u])):
            if self.G[u][v]:
                N.append(v)
        return N

    #Input : a vertex u, a color i
    #Output : the set of neighbours of u with color i
    def neighbours_i(self,u,i):
        Ni=[]
        for v in self.neighbours(u):
            if self.K[v]==i:
                Ni.append(v)
        return Ni
    #Input : a vertex u
    #Output : an array of indexes of the neighbours of u
    def predecessors(self,v):
        P=[]
        for u in range(len(self.G)):
            if self.G[u][v]:
                P.append(u)
        return P


    #Input : a vertex u, a color i
    #Output : the set of neighbours of u with color i
    def predecessors_i(self,v,i):
        Ni=[]
        for u in self.predecessors(v):
            if self.K[u]==i:
                Ni.append(u)
        return Ni
        

    #Input :
    #Output : True if the power coloring of G is feasible, False otherwise
    def checkPowerColoring(self,k=2):
        for v in range(self.n):
            if not(len(self.neighbours_i(v,self.K[v])) <= len(self.neighbours(v))//k):
                print(len(self.neighbours_i(v,self.K[v])),len(self.neighbours(v)))
                return False
        return True
        

    #Input : 
    #Output : An array K s.t K[v] is the color of vertex v
    def greedyPowerColoring(self,k=2):
        self.K=[-1 for _ in range(self.n)]
        for vj in range(self.n):
            #Find the minimum value of color that can be used in vertex vj
            c=-1
            nb_colors=self.nb_colors()
            for i in range(nb_colors):
                tmp=True
                #Check that the property holds for every predecessor if we color vj with i
                P=self.predecessors_i(vj,i)
                for u in P:
                    if len(self.neighbours_i(u,i))+1>len(self.neighbours(u))//k:   
                        tmp=False
                        break
                #Check if the property holds for vj if we color vj with i
                if len(self.neighbours_i(vj,i))<=len(self.neighbours(vj))//k:
                    if tmp:
                        c=i
                        break

                    
            if c==-1:
                self.K[vj]=nb_colors
            else:
                self.K[vj]=c
        assert(self.checkPowerColoring(k))
        return self.K
    def nb_colors(self):
        n=0
        diff=[]
        for c in self.K:
            if c not in diff and c!=-1:
                diff.append(c)
        return len(diff)


def plot_digraph(adjMat,coloring):
    colors=["white","blue","red","yellow","green","cyan","magenta","black","violet","pink"]
    G = nx.DiGraph()
    edges=[]
    for u in range(len(adjMat)):
        for v in range(len(adjMat)):
            if adjMat[u][v]:
                edges.append((u,v))
    G.add_edges_from(edges)
    edge_colours = ['black' for edge in G.edges()]
    #Create color_map using coloring
    color_map=[]
    for node in G.nodes():
        color_map.append(colors[coloring[node]])
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size = 200,node_color=color_map)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=edges, arrows=True)
    plt.show()

###Compute 1000 random digraphs of size nxm, compute a power coloring using greedyAlgorithm and plot the graph with the biggest power coloring and smallest power coloring######

k=0
M=0
m=2**32
while k<10000:
    example=digraph(n=10,m=12)
    colors=example.greedyPowerColoring(2)
    #print("Coloring",colors)
    nb_colors=example.nb_colors()
    #print("Number of colors", nb_colors)
    if nb_colors>M:
        M=nb_colors
        max_colors=list(colors)
        maxAdjMat=list(example.G)
    if nb_colors<m:
        m=nb_colors
        min_colors=list(colors)
        minAdjMat=list(example.G)
    k+=1



print("min colors", min_colors)
print("nb colors",m)

print("max colors", max_colors)
print("nb colors",M)

plot_digraph(minAdjMat,min_colors)
plot_digraph(maxAdjMat,max_colors)

        
        
