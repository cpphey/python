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

if __name__== "__main__":
    g = Graph(5)
    g.add_edge_undirected(3, 0, 4)  # D -> A, weight 4
    g.add_edge_undirected(3, 2, 7)  # D -> C, weight 7
    g.add_edge_undirected(3, 4, 3)  # D -> E, weight 3
    g.add_edge_undirected(4, 1, 5)  # E -> B, weight 5
    g.add_edge_undirected(4, 2, 6)  # E -> C, weight 6
    g.add_edge_undirected(1, 2, 1)  # B -> C, weight 1
    g.add_edge_undirected(2, 0, 2)

    g.bfs(3)
