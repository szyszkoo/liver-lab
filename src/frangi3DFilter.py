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
# from skimage.filters import frangi, hessian
import frangi as fr
from fr import frangi



sampleNumber = "01"
liverReader = LiverReader()
liverData = liverReader.readLiverData(sampleNumber)
roiData = liverReader.readLiverROIData(sampleNumber)


liver01 = liverData / np.max(liverData)  #normalised Liver

livfrang = np.zeros((liverData.shape[0], liverData.shape[1], liverData.shape[2]), dtype=float)

livfrang = frangi(liverData)
liverFrangi = np.multiply(livfrang, roiData)