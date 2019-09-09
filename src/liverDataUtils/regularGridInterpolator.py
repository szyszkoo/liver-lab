import numpy as np
import scipy.interpolate as spint
from liverDataUtils.fileNames import FileNames
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import nrrd

RGI = spint.RegularGridInterpolator

sampleNumber = "03"
liverReader = LiverReader()
fileNames = FileNames()
pixelSpacing = 1.1875 # x and y position
sliceThickness = 3 # z position

liverData = liverReader.readLiverData(sampleNumber)
xDimension = int(np.ceil(liverData.shape[0] * pixelSpacing))
yDimension = int(np.ceil(liverData.shape[1] * pixelSpacing))
zDimension = int(np.ceil(liverData.shape[2] * sliceThickness))

x = np.linspace(1, liverData.shape[0], liverData.shape[0])
y = np.linspace(1, liverData.shape[1], liverData.shape[1])
z = np.linspace(1, liverData.shape[2], liverData.shape[2])

rgi = RGI(points=[x,y,z], values=liverData)
print(rgi((1.6842105263157894,1.6842105263157894,27.0)))
interpolatedDataCube = np.zeros((int(np.ceil(xDimension)), int(np.ceil(yDimension)), int(np.ceil(zDimension))), dtype=int)

for i in range(1, xDimension):
    print(f"i was: {i}")
    for j in range(1, yDimension):
        for k in range(1, zDimension):
            iAdjusted = i/pixelSpacing
            jAdjusted = j/pixelSpacing
            kAdjusted = k/sliceThickness

            if(iAdjusted>=1 and jAdjusted >= 1 and kAdjusted >= 1):
                interpolatedDataCube[i, j, k] = rgi((iAdjusted, jAdjusted, kAdjusted))
            else:
                pass # just to handle borders - they are all zeros anyway

nrrd.write(fileNames.getInterpolatedCubeFileName(sampleNumber), interpolatedDataCube)

Plotter(liverData, interpolatedDataCube)