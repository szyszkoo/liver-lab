from liverDataUtils.liverReader import LiverReader
from liverDataUtils.fileNames import FileNames
from liverDataUtils.regionGrowing import RegionGrowing
from liverDataUtils.plotter import Plotter
import nrrd
import time
import numpy as np 

start_time = time.time()
sampleNumber = "03"
liverReader = LiverReader()
fileNames = FileNames()
regionGrowing = RegionGrowing()

liverDataFrangi = liverReader.readNrrdData("testFrangi2D.nrrd")
roi = liverReader.readInterpolatedLiverData("_03_roi")

liverDataFrangi = np.multiply(liverDataFrangi, roi)
regionMask = regionGrowing.grow(liverDataFrangi,(120,149,147), 5)

liverData = liverReader.readInterpolatedLiverData(sampleNumber)
119-134,75,159
print("Execution time [s]: ", time.time() - start_time)

# regionMask[:,149,147] = 1
# regionMask[120,:,147] = 1

nrrd.write("testRegionGrowingMask_nbgh5.nrrd", regionMask.astype(int)*255)

plotter = Plotter(regionMask, liverDataFrangi, 150)
plotter.draw()

