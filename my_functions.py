from constants import Constants


def func0(t: float) -> complex:
    if 0.0 <= t <= 0.125:
        return complex(1, t / 0.125)
    elif 0.125 < t <= 0.375:
        return complex(1 - (t - 0.125) / 0.125, 1)
    elif 0.375 < t <= 0.625:
        return complex(-1, 1 - (t - 0.375) / 0.125)
    elif 0.625 < t <= 0.875:
        return complex(-1 + (t - 0.625) / 0.125, -1)
    elif 0.875 < t <= 1.0:
        return complex(1, -1 + (t - 0.875) / 0.125)
    else:
        raise ValueError("t is out of range")


myFunctions = {"square": func0}
