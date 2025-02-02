"""
PathFile Formatt: space separated number pairs, one per line
like this:
x1 y1
x2 y2
x3 y3
...
xn yn

a path is a list of complex numbers:
[x1+y1j, x2+y2j, ..., xn+ynj]

"""


def readPathFromFile(fileName: str) -> list:
    """Reads a path from a file and returns it as a list of complex numbers"""
    with open(fileName, 'r') as file:
        lines = file.readlines()
        path = []
        for line in lines:
            x, y = line.split()
            path.append(complex(float(x), float(y)))
        return path


def functionFromPath(path: list, t: float) -> complex:
    """Returns the function represented by the path"""
    if len(path) == 0:
        return 0
    elif len(path) == 1:
        return path[0]
    elif t >= 1:
        return path[-1]
    elif t <= 0:
        return path[0]
    else:
        # do linear interpolation
        n = len(path)
        i = int(t * (n - 1))
        t = t * (n - 1) - i
        return path[i] * (1 - t) + path[i + 1] * t
