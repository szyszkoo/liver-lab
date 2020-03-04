import numpy as np
from skimage.filters import median

def medianFilter(dataCube):
     dataCube = np.array(dataCube)
     filtered = np.zeros(dataCube.shape)

     for index in np.arange(0, dataCube.shape[2], 1):
         filtered[:,:,index] = median(dataCube[:,:,index])

     return filtered