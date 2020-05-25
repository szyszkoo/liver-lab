from sklearn.cluster import KMeans, SpectralClustering, spectral_clustering
from sklearn.feature_extraction import image
from sklearn.feature_selection import VarianceThreshold
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import time
import numpy as np
import nrrd
from liverDataUtils.n4BiasFieldCorretion import n4BiasFieldCorrection3D
from liverDataUtils.resultChecker import checkVascular, getClustersMeans, checkVascularDiceMethod, getFirstClasses
from scipy.ndimage.filters import gaussian_filter
from distutils.version import LooseVersion
import skimage
from skimage.transform import rescale
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import zscore
import matplotlib.pyplot as plt
from itertools import permutations

# init
liverReader = LiverReader()
start_time = time.time()
sampleNumber = "16" # 16/ 18
sliceNumber = 56 # 56 / 47

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

numberOfClassesStart = 3
numberOfClassesEnd = 20
diceResults = []

for clusters in np.arange(numberOfClassesStart, numberOfClassesEnd + 1, 1):
    print(f"{clusters}/{numberOfClassesEnd}")
    # print(f"```````````````````````````````````````` {clusters} clusters ``````````````````````````````````````````")
    # kmeans
    kmeans = KMeans(n_clusters=clusters)
    labels = kmeans.fit_predict(roiPixelValues)

    # recreate liver image
    labelsImg = np.zeros_like(img)
    for index, (i, j) in np.ndenumerate(roiPixelsIndices):
        labelsImg[i,j] = labels[index] 

    # assign new labels for the classes, based on class values mean
    clusterMeans = getClustersMeans(labelsImg, img)
    sortedByCluseterMean = sorted(clusterMeans, key=lambda labelNoMeanPair: labelNoMeanPair[1])
    newLabels = np.zeros_like(labelsImg)

    for index, (labelNo, mean) in enumerate(sortedByCluseterMean):
        newLabels[labelsImg == labelNo] = index
    
    # evaluation
    # join first n-1 classes together and evaluate the Dice coefficient (n - number of clusters in kmeans)
    # i.e. join classes: (0), (0,1), ..., (0,1, ..., n-1)
    for classNo in np.arange(1, clusters):
        # print()
        # print(f"************* Joined first {classNo} cluster(s) *************")
        
        vascular = getFirstClasses(classNo, newLabels)
        vascular = np.multiply(vascular, liverRoi[...,sliceNumber])
        result = checkVascularDiceMethod(vascular, sampleNumber, sliceNumber)
        # Plotter(template, vascular)
        if(result[1,1] > 0.6):
            diceResults.append([(clusters, classNo), result[1,1]])

    # vascular = getCustomClasses(4, newLabels)
    # checkVascular(vascular, sampleNumber, sliceNumber)

# print(diceResults)
values = [x[1] for x in diceResults]
labels = [','.join(map(str, x[0])) for x in diceResults]
test = sorted(diceResults, key=lambda labelValuePair: labelValuePair[1], reverse=True)[0]
print(f"Max value: {test}")
print("------ Execution time: %s seconds ------" % (time.time() - start_time))

plt.bar(labels, values)
plt.show()
# Plotter(img, labelsImg)
# Plotter(incorrectPixels, incorrectPixels)
