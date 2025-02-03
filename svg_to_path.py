import svgpathtools
import numpy as np
import argparse
import os


def readPathFromFile(fileName: str, pathIndex=0) -> list:
    path = svgpathtools.svg2paths(fileName)[0][pathIndex]
    return path


def convertSvgToPath(fileName: str,
                     pathIndex=0,
                     offset=(0, 0),
                     delta=1) -> None:
    path = readPathFromFile(fileName, pathIndex)
    total_length = path.length()
    samples = []
    s_values = np.arange(0, total_length, delta)
    for s in s_values:
        t = path.ilength(s)
        point = path.point(t)
        samples.append((point.real, point.imag))

    output_string = ""
    for _, (x, y) in enumerate(samples):
        output_string += f"{x + offset[0]} {y + offset[1]}"
        output_string += "\n"
    return output_string


def getNumOfPaths(fileName: str) -> int:
    paths, _ = svgpathtools.svg2paths(fileName)
    return len(paths)


def getOffsetOfPaths(pathlist: list) -> tuple:
    global_xmin, global_xmax, global_ymin, global_ymax = float('inf'), float(
        '-inf'), float('inf'), float('-inf')
    for path in pathlist:
        bbox = path.bbox()
        if bbox is not None:  # 确保路径有效
            xmin, xmax, ymin, ymax = bbox
            global_xmin = min(global_xmin, xmin)
            global_xmax = max(global_xmax, xmax)
            global_ymin = min(global_ymin, ymin)
            global_ymax = max(global_ymax, ymax)
    return (-(global_xmin + global_xmax) / 2, -(global_ymin + global_ymax) / 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-name', type=str)
    parser.add_argument('--path-index', type=int, default=None)
    filename = parser.parse_args().file_name
    index = parser.parse_args().path_index
    if index is None:
        directory = filename.replace(".svg", "")
        os.mkdir(directory)
        shortname = os.path.basename(directory)
        num = getNumOfPaths(filename)
        pathlist = []
        for i in range(num):
            pathlist.append(readPathFromFile(filename, i))
        print("total {} path files".format(num))
        for i in range(num):
            s = convertSvgToPath(filename,
                                 pathIndex=i,
                                 offset=getOffsetOfPaths(pathlist))
            with open(directory + "/" + shortname + str(i), "w") as f:
                f.write(s)
    else:
        s = convertSvgToPath(filename, pathIndex=index)
        with open(filename.replace(".svg", str(index)), "w") as f:
            f.write(s)
