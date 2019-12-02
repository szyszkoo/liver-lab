import numpy as np
import matplotlib.pyplot as plt
import nrrd

from liverDataUtils.liverReader import LiverReader
import sys
sys.path.append("~/repo/liver-lab/frangi/")

from frangi.frangi import frangi
from liverDataUtils.plotter import Plotter

from skimage.filters import frangi as frangi2D

# import skimage as sk
# from skimage import exposure

# from skimage.filters import (threshold_otsu, threshold_niblack, threshold_sauvola)

# from skimage.morphology import disk
# from skimage.filters import rank
# from skimage.filters import frangi, hessian
# import frangi as fr
# from fr import frangi



sampleNumber = "03"
liverReader = LiverReader()
interp_liverData = liverReader.readInterpolatedLiverData(sampleNumber)
liverData = liverReader.readLiverData(sampleNumber)
roiData = liverReader.readLiverROIData(sampleNumber)



# Plotter(liverData, interp_liverData, 100)

#
# liver01 = liverData / np.max(liverData)  #normalised Liver
#
# livfrang = np.zeros((liverData.shape[0], liverData.shape[1], liverData.shape[2]), dtype=float)
#
livfrang = frangi(liverData)
liverFrangi3D = np.multiply(livfrang, roiData)

# plotter = Plotter(liverData, liverFrangi, 50)
# plotter.draw()

livfrang = np.zeros((liverData.shape[0], liverData.shape[1], liverData.shape[2]), dtype=float)
for index in np.arange(0, liverData.shape[2], 1):
    livfrang[:, :, index] = frangi2D(liverData[:, :, index])
liverFrangi2D = np.multiply(livfrang, roiData)

plotter = Plotter(liverFrangi3D, liverFrangi2D, 50)
plotter.draw()


filename2D = 'liverFrangi2D_' + sampleNumber + '.nrrd'
filename3D = 'liverFrangi3D_' + sampleNumber + '.nrrd'
nrrd.write(filename2D, liverFrangi2D)
nrrd.write(filename3D, liverFrangi3D)


liverFrangi2_3 = np.multiply(liverFrangi2D , liverFrangi3D)

plotter = Plotter(liverData, liverFrangi2_3, 50)
plotter.draw()

filename2_3 = 'liverFrangi2_3_' + sampleNumber + '.nrrd'
nrrd.write(filename2_3, liverFrangi2_3)

