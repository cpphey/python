import copy
input=[0,1,2]
ps=[[]]

#print(len(ps))
#exit(0) exit code

def oneDimensionalCopy(argList):
    ret=[]
    for idx in range(len(argList)):
        ret.append(argList[idx])
    return ret

def twoDimensionalCopy(argList):
    ret=[]
    for idx in range(len(argList)):
        ret.append(oneDimensionalCopy(argList[idx]))
    return ret

def makePowerset(arg):
    global ps #global variable
    #orig=ps.copy() #wont work as need deep copy https://stackoverflow.com/questions/2541865/copying-nested-lists-in-python
    orig=copy.deepcopy(ps) #orig=twoDimensionalCopy(ps)#[oneDimensionalCopy(x) for x in ps]
    toAdd=copy.deepcopy(orig) #toAdd=orig=twoDimensionalCopy(orig)#[oneDimensionalCopy(x) for x in orig]
    for idx in range(len(toAdd)):
        toAdd[idx].append(arg)
    added=orig+toAdd
    ps=added

for i in input:
    makePowerset(i)


temp1=10


########################################################################################################################

################  POWER SET AGAIN  #####################################################################################

########################################################################################################################
def powerSetString(arg):
    ps=[]

    for e in arg:
        origPs=ps
        copyPs=copy.deepcopy(origPs)
        for i in range(len(copyPs)):
            copyPs[i]=copyPs[i]+e
        copyPs.append(e)
        #ps = list(set(ps+copyPs)) #uneeded since no multiple copies
        ps = ps + copyPs

    #ps.remove("") #remove emoty set, otherwise put an if statement
    return ps


def powerSetGeneral(arg):
    ps=[]

    for e in arg:
        origPs=ps
        copyPs=copy.deepcopy(origPs)
        for i in range(len(copyPs)):
            copyPs[i].append(e)
        copyPs.append([e])
        #ps = list(set(ps+copyPs)) #uneeded since no multiple copies
        ps = ps + copyPs

    #ps.remove("") #remove emoty set, otherwise put an if statement
    return ps


if __name__=="__main1__":
    print("Main func")
    #ps=powerSetString("umbrella")
    ps = powerSetString("ab")
    print(ps)

    ps = powerSetGeneral("a")
    print(ps)

    ps = powerSetGeneral("ab")
    print(ps)

    ps = powerSetGeneral([1])
    print(ps)

    ps = powerSetGeneral([1,2])
    print(ps)




def anotherImpl(arg):
    ps=[[]]
    for e in arg:
        loop_arr=copy.deepcopy(ps)
        #Add e to each element in cp
        for ee in loop_arr:
            ee.append(e)

        #Combina cp and orig to new orig
        ps = ps+loop_arr

    return ps

if __name__=="__main__":
    print(anotherImpl([1,2,3]))
    print("done")
