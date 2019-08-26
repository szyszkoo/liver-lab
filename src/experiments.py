import numpy as np
import nrrd
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
from regionGrowing import RegionGrowing
from liverDataUtils.fileNames import FileNames

sampleNumber = "03"
liverReader = LiverReader()
fileNames = FileNames()
cubeInterpolator = CubeInterpolator()
regionGrowing = RegionGrowing()

liverData = liverReader.readInterpolatedLiverData(sampleNumber)
regionGrowth = regionGrowing.grow(liverData, (107,136,142), 4)
# interpolated = cubeInterpolator.interpolateCube(liverData, 2)

Plotter(liverData, regionGrowth, 164)
# nrrd.write(fileNames.getInterpolatedCubeFileName(sampleNumber), interpolated)


