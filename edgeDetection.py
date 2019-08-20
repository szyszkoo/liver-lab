from skimage.filters import roberts, sobel
import numpy as np
import matplotlib.pyplot as plt
import nrrd
from plotter import Plotter
from fileNames import FileNames

sampleNumber = "01"
fileNames = FileNames()

liverData, liverHeader = nrrd.read(fileNames.getLiverCubeFileName(sampleNumber))
roiData, roiHeader =  nrrd.read(fileNames.getRoiCubeFileName(sampleNumber))
roiData = roiData/255
liver = np.multiply(liverData, roiData)
liverEdges = np.zeros(liver.shape, dtype=int)

for index, singleSlice in enumerate(np.rollaxis(liver, 2)):
    liverEdges[..., index] = sobel(singleSlice)
    
Plotter(liverEdges, liver, 50)