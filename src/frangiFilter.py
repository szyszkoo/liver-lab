import numpy as np
import matplotlib.pyplot as plt
import nrrd

from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter

import skimage as sk
from skimage import exposure

from skimage.filters import (threshold_otsu, threshold_niblack, threshold_sauvola)

from skimage.morphology import disk
from skimage.filters import rank
from skimage.filters import frangi, hessian




sampleNumber = "01"
liverReader = LiverReader()
liverData = liverReader.readLiverData(sampleNumber)
roiData = liverReader.readLiverROIData(sampleNumber)


liver01 = liverData / np.max(liverData)  #normalised Liver

livfrang = np.zeros((liverData.shape[0], liverData.shape[1], liverData.shape[2]), dtype=float)
for index in np.arange(0, liverData.shape[2], 1):
    livfrang[:, :, index] = frangi(liverData[:, :, index])
liverFrangi = np.multiply(livfrang, roiData)

# Plotter(liverData, liverFrangi, 50)



# Contrast stretching
p2, p98 = np.percentile(liverData, (2, 98))
img_rescale = exposure.rescale_intensity(liverData, in_range=(p2, p98))

for index in np.arange(0, liverData.shape[2], 1):
    livfrang[:, :, index] = frangi(img_rescale[:, :, index])
liverFrangi_ImRescale = np.multiply(livfrang, roiData)

# Plotter(img_rescale,liverFrangi_ImRescale, 50)


# gamma corr
gamma_corrected = exposure.adjust_gamma(liverData, 1.2)
for index in np.arange(0, liverData.shape[2], 1):
    livfrang[:, :, index] = frangi(gamma_corrected[:, :, index])
liverFrangi_gamma = np.multiply(livfrang, roiData)

# Plotter(img_rescale,liverFrangi_gamma, 50)




# Equalization (Global)
img_eq = exposure.equalize_hist(liverData)

for index in np.arange(0, liverData.shape[2], 1):
    livfrang[:, :, index] = frangi(img_eq[:, :, index])
liverFrangi_imgeq = np.multiply(livfrang, roiData)

# Plotter(img_rescale,liverFrangi_imgeq, 50)


filename = 'liverFrangi' + sampleNumber + '.nrrd'
nrrd.write(filename, liverFrangi)

filename = 'liverFrangi_ImRescale' + sampleNumber + '.nrrd'
nrrd.write(filename, liverFrangi_ImRescale)

filename = 'liverFrangi_gamma' + sampleNumber + '.nrrd'
nrrd.write(filename, liverFrangi_gamma)

filename = 'liverFrangi_imgeq' + sampleNumber + '.nrrd'
nrrd.write(filename, liverFrangi_imgeq)



#
# # Equalization (Global each slice)
# img_eqII = np.zeros((liver.shape[0], liver.shape[1], liver.shape[2]), dtype=int)
# for index in np.arange(0, liver.shape[2], 1):
#     img_eqII[:, :, index] = exposure.equalize_hist(liver[:, :, index])
# Plotter(img_eqII,liver, 50)
#
#
# # Equalization Local
# selem = disk(30)
#
# img_eqLocal = np.zeros((liver.shape[0], liver.shape[1], liver.shape[2]), dtype=int)
# for index in np.arange(0, liver.shape[2], 1):
#     img_eqLocal[:, :, index] = rank.equalize(liver01[:, :, index], selem=selem)
# Plotter(img_eqLocal,liver, 50)
#
#
# # Adaptive Equalization
#
# # img_adapteq = exposure.equalize_adapthist(liver01, clip_limit=0.9)
# # plotter(img_adapteq, 50)
#
# img_adapteq = np.zeros((liver.shape[0], liver.shape[1], liver.shape[2]), dtype=int)
# for index in np.arange(0, liver.shape[2], 1):
#     img_adapteq[:, :, index] = exposure.equalize_adapthist(liver01[:, :, index], clip_limit=0.09)
# Plotter(img_adapteq,liver, 50)
#


