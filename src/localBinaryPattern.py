from skimage.feature import local_binary_pattern
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import time
import numpy as np
import nrrd


# init
liverReader = LiverReader()
start_time = time.time()

# lbp settings
radiusValues = np.arange(5, 55, 5)
n_pointsValues = np.arange(5, 55, 5)
methods = ['default', 'ror', 'uniform', 'nri_uniform']

# read liver data
liverRoiFilePath = "results/base/LIVER_roiLiver16.nrrd"
liverWholeDataFilePath = "results/base/liverCube16.nrrd"

liverRoi = liverReader.readNrrdData(liverRoiFilePath)/255
liverWholeData = liverReader.readNrrdData(liverWholeDataFilePath)

liver = np.multiply(liverRoi, liverWholeData)

# get single slice
img = liver[:, :, 56]

# single lbp
# lbp = local_binary_pattern(img, 30, 15)

# =============================================================
# iterate over params lbp

# create the empty output cube
featureVectorLen = radiusValues.size * n_pointsValues.size * len(methods)
output = np.empty((img.shape[0], img.shape[1], featureVectorLen+1))

# iterate over each params vector value, apply gabor filter and save single result slice as a new slice in the output cube
output[:,:,0] = img
currentSlice = 1

for radius in radiusValues:
    for n_points in n_pointsValues:
        for method in methods:
            print(f"Radius: {radius}, n_points: {n_points}, method: {method}")
            output[..., currentSlice] = local_binary_pattern(img, radius, n_points, method=method)
            currentSlice += 1

# ================================================================

# Plotter(np.multiply(lbp, liverRoi[:, :, 56]), img)
# nrrd.write("results/localBinaryPattern/radius_nPoints_method_noVar.nrrd", output)
Plotter(output, output)