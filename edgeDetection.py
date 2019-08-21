from skimage.filters import roberts, sobel, frangi
import numpy as np
import matplotlib.pyplot as plt
import nrrd
from liverDataUtils.plotter import Plotter
from liverDataUtils.liverReader import LiverReader

sampleNumber = "01"
liverReader = LiverReader()

liver = liverReader.readLiverData(sampleNumber)
liverEdges = np.zeros(liver.shape, dtype=int)

# Frangi 
for index, singleSlice in enumerate(np.rollaxis(liver, 2)):
    liverEdges[..., index] = frangi(singleSlice) # not working yet - why? (black picture)
    
Plotter(liverEdges, liver, 50)