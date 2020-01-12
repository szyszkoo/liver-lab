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

liverData = liverReader.readInterpolatedLiverData(sampleNumber)
liverDataFrangi = liverReader.readNrrdData("testFrangi2D.nrrd")
roi = liverReader.readInterpolatedLiverData("_03_roi")

liverDataFrangi = np.multiply(liverDataFrangi, roi)
# regionMask = regionGrowing.grow(liverDataFrangi,(129,179,150), 1)

liverData = liverReader.readInterpolatedLiverData(sampleNumber)
print("Execution time [s]: ", time.time() - start_time)

# regionMask[:,179,150] = 1
# regionMask[129,:,150] = 1

# nrrd.write("testRegionGrowingMask_nbgh5.nrrd", regionMask.astype(int)*255)

plotter = Plotter(liverDataFrangi, liverData, 150)
plotter.draw()

