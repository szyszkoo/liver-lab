import numpy as np
import nrrd
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import time 
from liverDataUtils.regionGrowing import RegionGrowing
from liverDataUtils.filters import medianFilter
from liverDataUtils.n4BiasFieldCorretion import n4BiasFieldCorrection3D
from liverDataUtils.imageSegmentation import otsuThreshold, regionGrowingWithUnsharpMasking, regionGrowing, gaborFilter
from skimage.filters import gabor
from liverDataUtils.gaborFeatureVector import createGaborFeatureVector

# init
liverReader = LiverReader()
start_time = time.time()

# read liver data
liverWholeDataFilePath = "results/base/liverCube16.nrrd"
liverRoiFilePath = "results/base/LIVER_roiLiver16.nrrd"

liverRoi = liverReader.readNrrdData(liverRoiFilePath)/255
liverWholeData = liverReader.readNrrdData(liverWholeDataFilePath)

liver = np.multiply(liverRoi, liverWholeData)

# get single slice
img = liver[:, :, 56]

# perform N4
imgN4 = n4BiasFieldCorrection3D(img)
imgN4 = np.multiply(imgN4, liverRoi[...,56])

# create Gabor feature vector
gaborFeatureVector = createGaborFeatureVector(imgN4)

# results
nrrd.write("results/gabor/gaborFeatureVector_n4_FrequencyTheaBandwith.nrrd", gaborFeatureVector)
print("------ Execution time: %s seconds ------" % (time.time() - start_time))