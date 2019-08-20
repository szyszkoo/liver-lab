import nrrd
import numpy as np
from fileNames import FileNames
from plotter import Plotter

sampleNumber = "02"
fileNames = FileNames()

liverData, liverHeader = nrrd.read(fileNames.getLiverCubeFileName(sampleNumber))
roiData, roiHeader =  nrrd.read(fileNames.getRoiCubeFileName(sampleNumber))
roiData = roiData/255
liver = np.multiply(liverData, roiData)

Plotter(roiData, liver, 41)