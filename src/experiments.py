import numpy as np
import nrrd
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
# from regionGrowing import RegionGrowing
from liverDataUtils.fileNames import FileNames
from skimage.filters import gaussian
from frangi.frangi import frangi
import time 

start_time = time.time()

sampleNumber = "03"
liverReader = LiverReader()
fileNames = FileNames()
# cubeInterpolator = CubeInterpolator()
# regionGrowing = RegionGrowing()

roi = liverReader.readNrrdData("interpolatedCube_03_roi.nrrd")
# liverData = liverReader.readInterpolatedLiverData(sampleNumber)
liverData = liverReader.readNrrdData("interpolatedCube_03_fullPic.nrrd")
print(np.shape(liverData))
livfrang = frangi(liverData)

nrrd.write('interpolatedFrangi3D_03.nrrd', np.multiply(livfrang, roi))
# roi = liverReader.readLiverROIData(sampleNumber)
# afterGauss = gaussian(liverData, sigma=0.5)
# regionGrowth = regionGrowing.grow(afterGauss, (107,136,142), 5)
# interpolated = cubeInterpolator.interpolateCube(liverData, 2)

# Plotter(liverData, liverData, 100)
# nrrd.write(fileNames.getInterpolatedCubeFileName(sampleNumber), interpolated)

print("------ Execution time: %s seconds ------" % (time.time() - start_time))
