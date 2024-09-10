import copy

#Gale Shapeyl for stable matching
class glale_shapely:
    def __init__(self,men,women):
        self.orig_pref_men=men
        self.orig_pref_women=women

    def makeGraph (self):
        self.sz = len(self.orig_pref)
        self.graph = [ [0] * self.sz for a in range(self.sz) ]

    def runAlgo(self):
        self.matches=set()
        self.sz = len(self.orig_pref_men) #assuming both same szie
        #self.matches.add(self.orig_pref_men.keys)
        #self.matches.add(self.orig_pref_women.keys)
        request_list_women = {k : [] for k in self.orig_pref_women.keys() }

        while len(self.matches) != self.sz:
            #men_pref = copy.deepcopy(self.orig_pref_men)
            #women_pref = copy.deepcopy(self.orig_pref_women)

            for m,mV in self.orig_pref_men.items():
                for w in mV:
                    print(w," ",m)
                    request_list_women[w].append(m)

            for w,req in request_list_women:
                pass




if __name__ == "__main__":
    men = {'A': ['D', 'E', 'F'],
           'B': ['D', 'F', 'E'],
           'C': ['F', 'D', 'E']}

    women = {'D': ['B', 'C', 'A'],
             'E': ['A', 'C', 'B'],
             'F': ['C', 'B', 'A']}

    obj = glale_shapely(men,women)
    obj.runAlgo()