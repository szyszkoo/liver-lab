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
from liverDataUtils.barPlotter import showPercentageBarPlot
from liverDataUtils.resultChecker import checkVascularDiceMethod

# init
liverReader = LiverReader()
start_time = time.time()
sampleNumber = "16" # 16/ 18 / 03
sliceNumber = 56 # 56 / 47 / 183

# # read liver data
# liverWholeDataFilePath = "results/base/liverCube03.nrrd"
# liverRoiFilePath = "results/base/roiLiver03.nrrd"

# liverRoi = liverReader.readNrrdData(liverRoiFilePath)/255
# liverWholeData = liverReader.readNrrdData(liverWholeDataFilePath)

# liver = np.multiply(liverRoi, liverWholeData)
# nrrd.write("results/base/liverCube03_liver.nrrd", liver)

vascular = liverReader.readNrrdData("results/kmeans/3_0.nrrd")
tumor = liverReader.readNrrdData(f"results/base/TUMOR_roiLiver{sampleNumber}.nrrd")[..., sliceNumber]/255
roi = liverReader.readNrrdData(f"results/base/roiLiver{sampleNumber}.nrrd")[..., sliceNumber]/255
template = liverReader.readNrrdData(f"results/base/VASCULAR_roiLiver{sampleNumber}.nrrd")[..., sliceNumber]/255

vascularWithoutTumor = np.multiply(vascular, ~tumor.astype(bool))/255
vascular = vascular/255
# Plotter(vascular, tumor)
print(vascular.dtype)
print(np.max(vascular))
print(np.min(vascular))
resultWithoutTumor = checkVascularDiceMethod(vascularWithoutTumor, roi, template)
result = checkVascularDiceMethod(vascular, roi, template)
print(result)
print(resultWithoutTumor)
# showPercentageBarPlot("", result[1,1], result[1,2], result[1,3], "")

# get single slice
# img = liver[:, :, 56]

# # perform N4
# imgN4 = n4BiasFieldCorrection3D(img)
# imgN4 = np.multiply(imgN4, liverRoi[...,56])

# # create Gabor feature vector
# gaborFeatureVector = createGaborFeatureVector(imgN4)

# # results
# nrrd.write("results/gabor/gaborFeatureVector_n4_FrequencyTheaBandwith.nrrd", gaborFeatureVector)
# print("------ Execution time: %s seconds ------" % (time.time() - start_time))