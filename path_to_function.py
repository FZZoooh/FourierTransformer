import numpy as np
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


def functionFromPath_old(path: list, t: float) -> complex:
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


def functionFromPath(path: list, t: np.ndarray) -> np.ndarray:
    if len(path) == 0:
        return np.zeros_like(t, dtype=np.complex128)
    t = np.clip(t, 0.0, 1.0)
    n_segments = len(path) - 1
    if n_segments == 0:
        return np.full_like(t, path[0], dtype=np.complex128)
    indices = np.floor(t * n_segments).astype(int)
    indices = np.clip(indices, 0, n_segments - 1)
    t_segment = t * n_segments - indices
    t_segment = np.clip(t_segment, 0.0, 1.0)
    p0 = np.array([c for c in path], dtype=np.complex128)[indices]
    p1 = np.array([c for c in path], dtype=np.complex128)[indices + 1]
    return p0 * (1 - t_segment) + p1 * t_segment
