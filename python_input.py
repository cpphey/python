def a():
    var = input("enter something:")
    print (var)

    #var = raw_input("enter something:") #older version
    print (var)
def b():
    pass #print (one)
    pass #print (two)

def c(arg):
    return (square := arg**2) / (square**2 / arg ) #assignment_expression walrus operator

print ( c(10.01) )