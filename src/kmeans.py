from sklearn.cluster import KMeans
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import time
import numpy as np
import nrrd
from liverDataUtils.n4BiasFieldCorretion import n4BiasFieldCorrection3D
from liverDataUtils.resultChecker import checkVascular

# init
liverReader = LiverReader()
start_time = time.time()

# # ===================== feature vectors ============================
# # read liver data
# featureVectorPath = "results/gabor/gaborFeatureVector_n4_FrequencyTheaBandwith.nrrd"
# featureVectorPathLbp = "results/localBinaryPattern/radius_nPoints_method_noVar.nrrd"

# featureVectors = liverReader.readNrrdData(featureVectorPath)
# print(featureVectors.shape)
# # get data in proper format (proper dimensions)
# data = featureVectors.reshape(-1, featureVectors.shape[2])
# print(data.shape)
# # kmeans
# kmeans = KMeans(n_clusters=4)
# labels = kmeans.fit_predict(data)

# labelsImg = labels.reshape((featureVectors.shape[0], featureVectors.shape[1]))
# checkVascular(labelsImg, "16")

# print("------ Execution time: %s seconds ------" % (time.time() - start_time))

# Plotter(featureVectors[..., 0], labelsImg)


# ===================== single slice ===============================
# read liver data
liverWholeDataFilePath = "results/base/liverCube16.nrrd"
liverRoiFilePath = "results/base/LIVER_roiLiver16.nrrd"

liverRoi = liverReader.readNrrdData(liverRoiFilePath)/255
liverWholeData = liverReader.readNrrdData(liverWholeDataFilePath)

liver = np.multiply(liverRoi, liverWholeData)

# get single slice
img = liver[:, :, 56]

# perform N4
# imgN4 = n4BiasFieldCorrection3D(img)

# get data in proper format (proper dimensions) - in this case, we need a vector, as we have just one value for each voxel for now
imgFlattened = img.reshape(-1,1)

# kmeans
kmeans = KMeans(n_clusters=4)
labels = kmeans.fit_predict(imgFlattened)

labelsImg = labels.reshape(img.shape)

checkVascular(labelsImg, "16")
print("------ Execution time: %s seconds ------" % (time.time() - start_time))

liverVascularFilePath = f"results/base/VASCULAR_roiLiver16.nrrd"
template = liverReader.readNrrdData(liverVascularFilePath)/255
template = template[..., 56]

Plotter(template, labelsImg)
