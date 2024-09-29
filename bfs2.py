
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
#                 if child not in set(visited+toBeVisited):
                if child not in visited+toBeVisited:
                    toBeVisited.append(child)
        return



    def dijkstra(self,start):
        distance=[math.inf] * self.size
        # will be done in while loop #distance[start] = 0
        toBeVisited=[(0,start)] #weight, node
        visited=[] #nodes visited
        while toBeVisited:
            weight,node=toBeVisited.pop()
            distance[node]= distance[node]+weight if distance[node] != math.inf else weight
            visited.append(node)
#            print(node)
            children,weights=self.getChildrenWithWeights(node)
            for child,childWeight in zip(children,weights):
#                if child not in visited:
                if child not in set(visited+[x[1] for x in toBeVisited]):
#                    toBeVisited.append((childWeight,child))
                    toBeVisited.append((distance[node]+childWeight, child))
        heapq.heapify(toBeVisited) #Does not Sort it

        return distance

    def dijkstraWithBackTrack(self, start):
        distance = [math.inf] * self.size
        distancePaths = [[]]* len(distance)
        # will be done in while loop #distance[start] = 0
        toBeVisited = [(0, start)]  # weight, node
        visited = []  # nodes visited
        while toBeVisited:
            weight, node, parent = toBeVisited.pop()
            distance[node] = distance[node] + weight if distance[node] != math.inf else weight
            distancePaths[node].append(parent)
            visited.append(node)
            #            print(node)
            children, weights = self.getChildrenWithWeights(node)
            for child, childWeight in zip(children, weights):
                #                if child not in visited:
                if child not in set(visited + [x[1] for x in toBeVisited]):
                    #                    toBeVisited.append((childWeight,child))
                    toBeVisited.append((distance[node] + childWeight, child, node))
            heapq.heapify(toBeVisited)  # Does not Sort it

        return distance, distancePaths

    def refreshVertexList(self):
        self.Vertices=[]
        for i in range(self.size):
            for j in range(self.size):
                if self.graph[i][j] != 0:
                    self.Vertices.append(i)
                    self.Vertices.append(j)

        self.Vertices=list(set(self.Vertices))


    def findClosetNeighbor(self,g_mst):
        g_mst.refreshVertexList()
        self.refreshVertexList()
        neighbour = [] #weight,start,end ; all Edges of MST have to be ranked in order
        v_not_mst= list ( set(self.Vertices) - set(g_mst.Vertices) )

        for v in g_mst.Vertices:
            neigh_v = [ i for i in range(g_mst.size) if 0 != self.graph[v][i] ]
            neigh_for_mst= [random_v for random_v in neigh_v if random_v in v_not_mst ]
            neigh_for_mst_weight= [ self.graph[v][i] for i in neigh_for_mst ]
            curr_node= [ v for i in range(len(neigh_for_mst_weight)) ]
            for w,s,e in zip(neigh_for_mst_weight,curr_node,neigh_for_mst):
                neighbour.append((w,s,e))

        heapq.heapify(neighbour)
        ret = neighbour[0] if 0< len(neighbour) else (None,None,None)# weight, start, end
        return ret

    def prim(self,start):
        g_mst = Graph(self.size)
        #self.findClosetNeighbor(g_mst)
        #self.graph[0][1]=10

        #Random end
        end_nodes = [ i for i in range(self.size) if 0 != self.graph[start][i] ]
        end = random.choice( end_nodes )

        mstCumWeight = g_mst.graph[start][end] = self.graph[start][end]
        toBeVisited = [start]
        visited = []
        while toBeVisited:
            node = toBeVisited.pop()
            visited.append(node)

            #get Closest edge (u,v) where u is V_mst and V is not
            w,s,e = self.findClosetNeighbor(g_mst)
            if s == None:
                print("prim loop skipped")
                continue
            toBeVisited.append(e)

            #Add to MST
            g_mst.graph[s][e] = w #TODO Confirm w eith original grpah
            mstCumWeight+=w

        g_mst.refreshVertexList()
        return (mstCumWeight,g_mst)


def main():
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
    distances, paths= g.dijkstra(3)

main()