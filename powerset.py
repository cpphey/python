import copy
input=[0,1,2]
ps=[[]]

#print(len(ps))
#exit(0) exit code

def makePowerset(arg):
    global ps #global variable
    #orig=ps.copy() #wont work as need deep copy https://stackoverflow.com/questions/2541865/copying-nested-lists-in-python
    #orig=[x[:] for x in ps]
    #toAdd=orig=[x[:] for x in orig]
    orig=copy.deepcopy(ps)
    toAdd=copy.deepcopy(orig)
    for idx in range(len(toAdd)):
        toAdd[idx].append(arg)
    added=orig+toAdd
    ps=added

for i in input:
    makePowerset(i)

temp1=10