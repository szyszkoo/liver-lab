from skimage.filters import roberts, sobel
import numpy as np
import matplotlib.pyplot as plt
import nrrd
from displaySlices import plotter

liverData, liverHeader = nrrd.read("./liverCube01.nrrd")
roiData, roiHeader =  nrrd.read("./ROILIVER01.nrrd")
roiData = roiData/255
liver = np.multiply(liverData, roiData)
singleSlice = liver[:,:,50]
liverEdges = np.zeros((liver.shape[0], liver.shape[1], liver.shape[2]), dtype=int)
test= np.rollaxis(liver,2)


for index, singleSlice in enumerate(np.rollaxis(liver, 2)):
    liverEdges[:,:, index] = sobel(singleSlice)
# plt.imshow(sobel(singleSlice))
    
# plt.show()
plotter(liverEdges, 50)