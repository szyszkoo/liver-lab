from liverDataUtils.liverReader import LiverReader
from liverDataUtils.fileNames import FileNames
from liverDataUtils.regionGrowing import RegionGrowing
from liverDataUtils.plotter import Plotter
import nrrd
import time

start_time = time.time()
sampleNumber = "03"
liverReader = LiverReader()
fileNames = FileNames()
regionGrowing = RegionGrowing()

liverDataFrangi = liverReader.readNrrdData("testFrangi3D.nrrd")
liverData = liverReader.readInterpolatedLiverData(sampleNumber)
regionMask = regionGrowing.grow(liverData,(121,148,147), 6)

print("Execution time [s]: ", time.time() - start_time)


plotter = Plotter(regionMask, liverData, 150)
plotter.draw()

# nrrd.write("testRegionGrowingMask.nrrd", regionMask)
