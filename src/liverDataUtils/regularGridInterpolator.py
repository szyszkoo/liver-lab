import numpy as np
import scipy.interpolate as spint
from liverDataUtils.fileNames import FileNames
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter

RGI = spint.RegularGridInterpolator

x = np.linspace(1, 320, 320)
y = np.linspace(1, 260, 260)
z = np.linspace(1, 80, 80)

sampleNumber = "03"
liverReader = LiverReader()
fileNames = FileNames()

liverData = liverReader.readLiverData(sampleNumber)

testPoint = (80,125,60.25)

rgi = RGI(points=[x,y,z], values=liverData)
interpolatedPointValue = rgi(testPoint)
print(interpolatedPointValue)