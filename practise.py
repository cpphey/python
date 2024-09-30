from dill.pointers import children


class Graph:
    def __init__(self,size):
        self.size=size
        graph = []
        for i in range(0, size):
            graph.append([0] * size)
        self.graph = graph

    def add_edge_undirected(self,s,d,w):
        self.graph[s][d]=self.graph[d][s]=w

    def getChildren(self,node):
        children = []
        for i in range(0, self.size):
            if self.graph[node][i] != 0:
                children.append(i)

        return children

    def bfs(self,start):
        queue = [start]
        visited= []
        while queue:
            node = queue.pop()
            print(node)
            visited.append(node)
            children = self.getChildren(node)
            #children not visited and not in queue
            #children_unvisited = list (set(children) - set(visited) - set(queue) ) #smart set way but creating more obj
            children_unvisited = []
            for e in children:
                if e not in visited+queue:
                    children_unvisited.append(e)
            #add them to queue
            queue = queue + children_unvisited

def main():
    g = Graph(5)
    g.add_edge_undirected(3, 0, 4)  # D -> A, weight 4
    g.add_edge_undirected(3, 2, 7)  # D -> C, weight 7
    g.add_edge_undirected(3, 4, 3)  # D -> E, weight 3
    g.add_edge_undirected(4, 1, 5)  # E -> B, weight 5
    g.add_edge_undirected(4, 2, 6)  # E -> C, weight 6
    g.add_edge_undirected(1, 2, 1)  # B -> C, weight 1
    g.add_edge_undirected(2, 0, 2)

    g.bfs(3)

#######################################
############## KRUSKAL ################
#######################################
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

def kruskal(n, edges):
    ds = DisjointSet(n)
    mst = []
    edges.sort(key=lambda x: x[2])  # Sort by weight
    for u, v, weight in edges:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst.append((u, v, weight))
    return mst

# Example usage
def main_kruskal():
    edges = [
        (0, 1, 10), (0, 2, 6), (0, 3, 5),
        (1, 3, 15), (2, 3, 4)
    ]
    n = 4  # Number of vertices
    mst = kruskal(n, edges)
    print("Minimum Spanning Tree:", mst)

main_kruskal()