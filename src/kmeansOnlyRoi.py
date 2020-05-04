from sklearn.cluster import KMeans, SpectralClustering, spectral_clustering
from sklearn.feature_extraction import image
from sklearn.feature_selection import VarianceThreshold
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import time
import numpy as np
import nrrd
from liverDataUtils.n4BiasFieldCorretion import n4BiasFieldCorrection3D
from liverDataUtils.resultChecker import checkVascular
from scipy.ndimage.filters import gaussian_filter
from distutils.version import LooseVersion
import skimage
from skimage.transform import rescale
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import zscore

# init
liverReader = LiverReader()
start_time = time.time()
sampleNumber = "18" # 16
sliceNumber = 47 # 56

# # # ===================== feature vectors ============================
# # read liver data
# featureVectorPath = "results/gabor/gaborFeatureVector_n4_FrequencyTheaBandwith.nrrd"
# featureVectorPathLbp = "results/localBinaryPattern/radius_nPoints_method_noVar.nrrd"

# featureVectors = liverReader.readNrrdData(featureVectorPath)
# print(featureVectors.shape)

# # get data in proper format (proper dimensions)
# data = featureVectors.reshape(-1, featureVectors.shape[2])
# print(data.shape)

# # min max scale
# scaler = MinMaxScaler()
# imgScaledMinMax = scaler.fit_transform(data) 
# print(f"img scaled shape: {imgScaledMinMax.shape}")

# # variance elimination
# selector = VarianceThreshold(threshold=1.0)
# data = selector.fit_transform(data)
# print(f"Img variance thres shape: {data.shape}")

# # kmeans
# kmeans = KMeans(n_clusters=4)
# labels = kmeans.fit_predict(data)

# labelsImg = labels.reshape((featureVectors.shape[0], featureVectors.shape[1]))
# checkVascular(labelsImg, "16")

# print("------ Execution time: %s seconds ------" % (time.time() - start_time))

# Plotter(featureVectors[..., 0], labelsImg)


# ===================== single slice ===============================
# read liver data
liverWholeDataFilePath = f"results/base/liverCube{sampleNumber}.nrrd"
liverRoiFilePath = f"results/base/LIVER_roiLiver{sampleNumber}.nrrd"

liverRoi = liverReader.readNrrdData(liverRoiFilePath)/255
liverWholeData = liverReader.readNrrdData(liverWholeDataFilePath)

liver = np.multiply(liverRoi, liverWholeData)

# get single slice
img = liver[:, :, sliceNumber]

# perform N4
img = n4BiasFieldCorrection3D(img)

imgFlattened = img.reshape(-1,1)

# get auxiliary vectors to process only pixels inside the ROI
roiPixelsIndices = np.empty((np.count_nonzero(imgFlattened)), dtype=object)
roiPixelValues = np.empty((np.count_nonzero(imgFlattened)))

iterator = 0
for (i, j), value in np.ndenumerate(img):
    if(value != 0):
        roiPixelValues[iterator] = value
        roiPixelsIndices[iterator] = (i,j)
        iterator += 1

roiPixelValues = roiPixelValues.reshape(-1,1)
liverVascularFilePath = f"results/base/VASCULAR_roiLiver{sampleNumber}.nrrd"
template = liverReader.readNrrdData(liverVascularFilePath)/255
template = template[..., sliceNumber]

for clusters in np.arange(3, 9, 1):
    print()
    print(f"******* {clusters} clusters *******")
    # kmeans
    kmeans = KMeans(n_clusters=clusters)
    labels = kmeans.fit_predict(roiPixelValues)

    # recreate liver image
    labelsImg = np.zeros_like(img)
    for index, (i, j) in np.ndenumerate(roiPixelsIndices):
        labelsImg[i,j] = labels[index] 

    (results, incorrectPixels) = checkVascular(labelsImg, sampleNumber, sliceNumber)
    Plotter(template, labelsImg)

print("------ Execution time: %s seconds ------" % (time.time() - start_time))

# Plotter(img, labelsImg)
# Plotter(incorrectPixels, incorrectPixels)
