import math
import numpy as np


# basic maths
def exp2piI_old(x: float) -> complex:  # to calculate e^(2πix)
    return complex(math.cos(x * 2.0 * math.pi), math.sin(x * 2.0 * math.pi))


def exp2piI(x: np.ndarray) -> np.ndarray:
    return np.exp(2j * np.pi * x)


def integrate(f, mi: float, ma: float, precision) -> complex:
    sum = complex(0.0, 0.0)
    deltax = (ma - mi) / precision
    x = mi
    while x <= ma:
        sum += f(x) * deltax
        x += deltax
    return sum


# fourier tools
def transform_old(target, order: int, precision) -> dict:
    # the dict is in this form: {"order": value, ... , -2: value, -1: value, 0: value, 1: value, ...}
    # target function should be defined on [0, 1]
    # it works with the funciton "untransform"
    factors = {"order": order}
    for n in range(-order, order + 1):
        key = n
        value = integrate(lambda t: target(t) * exp2piI(-n * t), 0.0, 1.0,
                          precision)
        factors[key] = value
    return factors


def transform(target, order: int, precision: int) -> dict:
    factors = {"order": order}
    mi, ma = 0.0, 1.0
    deltax = (ma - mi) / precision
    t_values = np.linspace(mi, ma, precision,
                           endpoint=False) + deltax / 2  # Midpoint sampling
    target_values = target(t_values)  # target now handles array input

    n_values = np.arange(-order, order + 1)
    exponents = -np.outer(n_values, t_values)
    exp_terms = exp2piI(exponents)

    integrals = np.sum(target_values * exp_terms, axis=1) * deltax
    for n, val in zip(n_values, integrals):
        factors[n] = val
    return factors


def untransform(complexParameters: dict,
                t: float) -> complex:  # t should be in [0, 1]
    sum = complex(0.0, 0.0)
    order = complexParameters["order"]
    for n in range(-order, order + 1):
        cn: complex = complexParameters[n]
        sum += cn * exp2piI(n * t)
    return sum


def getCircles(complexParameters: dict, t: float) -> list:
    circles = []
    sum = complex(0.0, 0.0)
    order = complexParameters["order"]
    c0: complex = complexParameters[0]
    circles.append({"pos": 0, "radius": abs(c0)})
    sum += c0
    for n in range(1, order + 1):
        cn: complex = complexParameters[n]
        cm: complex = complexParameters[-n]
        circles.append({"pos": sum, "radius": abs(cn)})
        sum += cn * exp2piI(n * t)
        circles.append({"pos": sum, "radius": abs(cm)})
        sum += cm * exp2piI(-n * t)
    circles.append({"pos": sum, "radius": 0})  # this is the end point
    return circles
