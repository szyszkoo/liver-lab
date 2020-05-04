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
sampleNumber = "18"
sliceNumber = 44

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

# data scaling 
# scaler = MinMaxScaler()
# imgScaledMinMax = scaler.fit_transform(img) 
# imgZScore = zscore(img, axis=1)
# Plotter(imgScaledMinMax, imgZScore)

# variance elimination
# selector = VarianceThreshold(threshold=1.0)
# imgVarianceThres = selector.fit_transform(img)
# mask_train = selector.get_support()
# # Plotter(imgVarianceThres, imgVarianceThres)
# # get data in proper format (proper dimensions) - in this case, we need a vector, as we have just one value for each voxel for now
# # imgFlattened = imgScaledMinMax.reshape(-1,1)
# imgFlattened = imgVarianceThres.reshape(-1,1)
imgFlattened = img.reshape(-1,1)

# kmeans
kmeans = KMeans(n_clusters=4)
labels = kmeans.fit_predict(imgFlattened)

# # spectral clustering
# if LooseVersion(skimage.__version__) >= '0.14':
#     rescale_params = {'anti_aliasing': False, 'multichannel': False}
# else:
#     rescale_params = {}
# smoothened = gaussian_filter(img, sigma=2)
# # rescaled = rescale(smoothened, 0.2, mode="reflect", **rescale_params)

# # Convert the image into a graph with the value of the gradient on the
# # edges.
# graph = image.img_to_graph(smoothened)

# # Take a decreasing function of the gradient: an exponential
# # The smaller beta is, the more independent the segmentation is of the
# # actual image. For beta=1, the segmentation is close to a voronoi
# beta = 20
# eps = 1e-6
# graph.data = np.exp(-beta * graph.data / graph.data.std()) + eps

# # labels = spectral_clustering(img, n_clusters=4)

# spectralClustering = SpectralClustering(n_clusters=4)
# spectralClustering.fit(imgFlattened)
# labels = spectralClustering.labels_

labelsImg = labels.reshape(img.shape)

(results, incorrectPixels) = checkVascular(labelsImg, sampleNumber, sliceNumber)

print("------ Execution time: %s seconds ------" % (time.time() - start_time))

liverVascularFilePath = f"results/base/VASCULAR_roiLiver{sampleNumber}.nrrd"
template = liverReader.readNrrdData(liverVascularFilePath)/255
template = template[..., sliceNumber]

Plotter(template, labelsImg)
# Plotter(incorrectPixels, incorrectPixels)
