def main ():
    print("hello")

def makeList ():
    l=[0,1,2]
    #l[3]=3 #wont work
    l.append(3)
    #return l[3]
    l = list( ( 1,2,3) )
    return l

def makeSet ():
    s = set((1,2))
    s = set( ( [1, 2],[3,4] ) )
    return s

#main()
print (makeList())
#print(makeSet())