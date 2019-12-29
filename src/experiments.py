import numpy as np
import nrrd
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
# from regionGrowing import RegionGrowing
from liverDataUtils.fileNames import FileNames
from skimage.filters import gaussian
from frangi.frangi import frangi

sampleNumber = "03"
liverReader = LiverReader()
fileNames = FileNames()
# cubeInterpolator = CubeInterpolator()
# regionGrowing = RegionGrowing()

roi = liverReader.readLiverROIData(sampleNumber)
liverData = liverReader.readInterpolatedLiverData(sampleNumber)
livfrang = frangi(liverData)

nrrd.write('interpolatedFrangi3D_03.nrrd', livfrang)
# roi = liverReader.readLiverROIData(sampleNumber)
# afterGauss = gaussian(liverData, sigma=0.5)
# regionGrowth = regionGrowing.grow(afterGauss, (107,136,142), 5)
# interpolated = cubeInterpolator.interpolateCube(liverData, 2)

# Plotter(liverData, liverData, 100)
# nrrd.write(fileNames.getInterpolatedCubeFileName(sampleNumber), interpolated)


