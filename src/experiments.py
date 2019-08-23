import numpy as np
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter

sampleNumber = "01"
liverReader = LiverReader()
cubeInterpolator = CubeInterpolator()

liverData = liverReader.readLiverData(sampleNumber)
interpolated = cubeInterpolator.interpolateCube(liverData, 2)
Plotter(interpolated, interpolated, 100)

