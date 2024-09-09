import math
import heapq
#Leetcode 733
class Graph:
    def __init__(self,size):
        self.size=size
        graph=[]
        for i in range(size):
            graph.append([])

        for i in range(size):
            for j in range(size):
                graph[i].append(0)

        self.graph=graph

    def add_edge_undirected(self, start, end, weight):
        self.graph[start][end] = self.graph[end][start] = weight

    def add_edge_directed(self, start, end, weight):
        if weight >=0:
            self.graph[start][end]=weight
        else:
            self.graph[end][start] = abs(weight)

    def getChildren(self,arg):
        children=[]
        for i in range(self.size):
            if self.graph[arg][i]:
                children.append(i)
        return children

    def getChildrenWithWeights(self,arg):
        children=[]
        weights=[]
        for i in range(self.size):
            if self.graph[arg][i]:
                children.append(i)
                weights.append(self.graph[arg][i]) #deep copy weights
        return (children,weights)

    def bfs(self,start):
        toBeVisited=[start]
        visited=[] #never delete from visited
        while toBeVisited:
            node=toBeVisited.pop()
            visited.append(node)
            print(node)
            children=self.getChildren(node)
            for child in children:
#                if child not in visited:
                 if child not in set(visited+toBeVisited):
                    toBeVisited.append(child)
        return



    def dijkstra(self,start):
        distance=[math.inf] * self.size
        # will be done in while loop #distance[start] = 0
        toBeVisited=[(0,start)]
        visited=[] #never delete from visited
        while toBeVisited:
            weight,node=toBeVisited.pop()
            distance[node]= distance[node]+weight if distance[node] != math.inf else weight
            visited.append(node)
            print(node)
            children,weights=self.getChildrenWithWeights(node)
            for child,childWeight in zip(children,weights):
#                if child not in visited:
                if child not in set(visited+[x[1] for x in toBeVisited]):
#                    toBeVisited.append((childWeight,child))
                    toBeVisited.append((distance[node]+childWeight, child))
        heapq.heapify(toBeVisited)
        return distance

if __name__=="__main__":
    print("Main Function")
    g = Graph(5)
    g.add_edge_directed(3, 0, 4)  # D -> A, weight 4
    g.add_edge_directed(3, 2, 7)  # D -> C, weight 7
    g.add_edge_directed(3, 4, 3)  # D -> E, weight 3
    g.add_edge_directed(4, 1, 5)  # E -> B, weight 5
    g.add_edge_directed(4, 2, 6)  # E -> C, weight 6
    g.add_edge_directed(1, 2, 1)  # B -> C, weight 1
    g.add_edge_directed(2, 0, -2)  # C -> A, weight -2

    #g.bfs(3)
    shortestDistance=g.dijkstra(3)

    i = 0