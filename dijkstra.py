#https://leetcode.com/problems/network-delay-time/
#743
import heapq
import math
class Graph:
    def __init__(self, n):
        if not n:
            return
        self.n = n + 1  # Since 1 indexed

        AdjMat = []
        for r in range(0, n):
            AdjMat.append([])

        for r in range(0, n):
            for c in range(0, n):
                AdjMat[r].append(0)

        self.nodes = AdjMat

    def addEdge(self, s, e, w):
        self.nodes[s][e] = w

    def returnChildrenWithWeights(self, row):
         c = []
         for i in range(0,self.n):
             c.append(self.nodes[row][i],i)

         return c #w, child


class Solution(object):
    def networkDelayTime(self, times, n, k):
        """
        :type times: List[List[int]]
        :type n: int
        :type k: int
        :rtype: int
        """
        g = Graph(n)
        for s, e, w in times:
            g.addEdge(s, e, w)
        distance = [math.inf] * n
        distance[k] = 0
        visited=[k]
        while visited:
            node = visited.pop()
            print(node)
            #distance[node] = distance[node] +
            childWithWeights = g.returnChildrenWithWeights(node)
            heapq.heapify(childWithWeights)
            for child in childWithWeights:
                if child not in visited:
                    visited.append(childWithWeights[1])

        return 0


if __name__ == '__main__':
    s = Solution();
    s.networkDelayTime([[2,1,1],[2,3,1],[3,4,1]],4,2)