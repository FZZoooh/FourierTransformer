import svgpathtools
import numpy as np
import argparse
import os
from tqdm import tqdm
import shutil


def readPathFromFile(fileName: str, pathIndex=0) -> list:
    path = svgpathtools.svg2paths(fileName)[0][pathIndex]
    return path


def convertSvgToPath(fileName: str,
                     pathIndex=0,
                     offset=(0, 0),
                     delta=1) -> tuple:
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
    return (output_string, total_length)


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


def getSizeOfPaths(pathlist: list) -> tuple:
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
    return (global_xmax - global_xmin, global_ymax - global_ymin)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-name', type=str)
    parser.add_argument('--path-index', type=int, default=None)
    filename = parser.parse_args().file_name
    index = parser.parse_args().path_index
    if index is None:
        directory = filename.replace(".svg", "")
        if os.path.exists(directory):
            choice = input(
                "target directory already exists. remove it? [Y/n]: ")
            if choice == "Y" or choice == "y":
                shutil.rmtree(directory)
            else:
                print("operation aborted")
                quit()
        os.mkdir(directory)
        shortname = os.path.basename(directory)
        num = getNumOfPaths(filename)
        pathlist = []
        for i in range(num):
            pathlist.append(readPathFromFile(filename, i))
        print("total {} path files".format(num))
        lengthlist = []
        for i in tqdm(range(num)):
            s, length = convertSvgToPath(filename,
                                         pathIndex=i,
                                         offset=getOffsetOfPaths(pathlist))
            lengthlist.append(length)
            with open(directory + "/" + shortname + str(i), "w") as f:
                f.write(s)
        average = sum(lengthlist) / len(lengthlist)
        speedconfig = open(directory + "/speed.config", "w")
        for i in range(num):
            speedconfig.write(str(max(average / lengthlist[i], 1)) + "\n")
        sizeconfig = open(directory + "/size.config", "w")
        sizeconfig.write(
            str(getSizeOfPaths(pathlist)[0]) + " " +
            str(getSizeOfPaths(pathlist)[1]))
    else:
        targetfile = filename.replace(".svg", str(index))
        if os.path.exists(targetfile):
            choice = input("target file already exists. remove it? [Y/n]: ")
            if choice == "Y" or choice == "y":
                os.remove(targetfile)
            else:
                print("operation aborted")
                quit()
        s = convertSvgToPath(filename, pathIndex=index)
        with open(targetfile, "w") as f:
            f.write(s)
