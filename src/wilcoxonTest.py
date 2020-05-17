from sklearn.cluster import KMeans
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import time
import numpy as np
import nrrd
from liverDataUtils.n4BiasFieldCorretion import n4BiasFieldCorrection3D
from liverDataUtils.resultChecker import checkVascular
from scipy.stats import ranksums

# init
liverReader = LiverReader()
start_time = time.time()
sampleNumber = "16" # 16 / 18
sliceNumber = 56 # 56 / 47

# ===================== single slice ===============================
# read liver data
liverWholeDataFilePath = f"results/base/liverCube{sampleNumber}.nrrd"
liverRoiFilePath = f"results/base/LIVER_roiLiver{sampleNumber}.nrrd"

liverRoi = liverReader.readNrrdData(liverRoiFilePath)/255
liverWholeData = liverReader.readNrrdData(liverWholeDataFilePath)

liverVascularFilePath = f"results/base/VASCULAR_roiLiver{sampleNumber}.nrrd"
template = liverReader.readNrrdData(liverVascularFilePath)/255
template = template[..., sliceNumber]

liver = np.multiply(liverRoi, liverWholeData)

# get single slice
img = liver[:, :, sliceNumber]

# wilcoxon
templateValues = np.multiply(img, template)
print(templateValues.shape)
vascularValues = templateValues[templateValues != 0]
nonVascularValues = templateValues[templateValues == 0]
print(vascularValues.shape)
print(nonVascularValues.shape)


statistics, pvalue = ranksums(vascularValues, nonVascularValues)
print(statistics)
print(pvalue)

# # ===================== feature vectors ============================
# read liver data
featureVectorPath = "results/gabor/gaborFeatureVector_n4_FrequencyTheaBandwith.nrrd"

featureVectors = liverReader.readNrrdData(featureVectorPath)
# print(featureVectors.shape)
featuresToExclude = [1,2]
for featureSlice in np.arange(1, featureVectors.shape[2]):
    templateValues = np.multiply(featureVectors[..., featureSlice], template)
    vascularValues = templateValues[templateValues != 0]
    nonVascularValues = templateValues[templateValues == 0]

    statistics, pvalue = ranksums(vascularValues, nonVascularValues)
    if(pvalue > 0.05):
        print(f"Feature no {featureSlice}: stats: {statistics}, pvalue: {pvalue}")
    # featuresToExclude.append(featureSlice)

features = np.ma.array(featureVectors, mask=False)

features.mask[...,featuresToExclude] = True
# features = featureVectors[mask]
features = features.compressed()
print(features.shape)
print("------ Execution time: %s seconds ------" % (time.time() - start_time))

# Plotter(img, labelsImg)
# Plotter(incorrectPixels, incorrectPixels)
