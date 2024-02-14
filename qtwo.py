def compose(*callables):
    def composition(x):
        for callable in callables:
            x = callable(x)
        return x

    return composition


def meter2centimeter(dist):
    """ Converting m to cm """
    return dist * 100


def centimeter2feet(dist):
    """ Converting cm to ft """
    return dist / 30.48


def feet2inches(dist):
    """ Converting ft to in """
    return dist * 12


#output=compose(feet2inches, centimeter2feet, meter2centimeter)(1.4)


def compose2(callables):
    def composition(x):
        for callable in callables:
            x = callable(x)
        return x

    return composition

fList=[feet2inches, centimeter2feet, meter2centimeter]
foo=compose2(fList)
output=foo(1.4)
temp=10
#works