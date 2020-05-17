from sklearn.cluster import KMeans
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
from sklearn.decomposition import PCA
import time
import numpy as np
import nrrd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from liverDataUtils.resultChecker import checkVascular

# init
liverReader = LiverReader()
start_time = time.time()
pca = PCA(10)

# read liver data
featureVectorPath = "results/gabor/gaborFeatureVector_FrequencyTheaBandwith.nrrd"
featureVectorN4Path = "results/gabor/gaborFeatureVector_n4_FrequencyTheaBandwith.nrrd"
featureVectorPathLbp = "results/localBinaryPattern/radius_nPoints_method_noVar.nrrd"

featureVectorsGabor = liverReader.readNrrdData(featureVectorPath)
featureVectorsLbp = liverReader.readNrrdData(featureVectorPathLbp)
# featureVectors = np.concatenate((featureVectorsGabor, featureVectorsLbp[...,1:]), axis=2)

print(featureVectorsGabor.shape)
# get data in proper format (proper dimensions)
data = featureVectorsGabor.reshape(-1, featureVectorsGabor.shape[2])
print(data.shape)

# pca (data is automatically centered but not scaled)
# scaledData = preprocessing.scale(data)
reducedData = pca.fit_transform(data)
print(reducedData.shape)

# kmeans
kmeans = KMeans(n_clusters=4)
labels = kmeans.fit_predict(reducedData)

labelsImg = labels.reshape((featureVectorsGabor.shape[0], featureVectorsGabor.shape[1]))


# Scree plot
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
 
plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal Component')
plt.title('Scree Plot')
plt.show()

# img = reducedData.reshape((featureVectors.shape[0], featureVectors.shape[1]))
# checkVascular(labelsImg, "16")
print("------ Execution time: %s seconds ------" % (time.time() - start_time))

Plotter(featureVectorsGabor[..., 0], labelsImg)

# # nrrd.write("results/kmeans/liver16_singleSlice_featureVectors_gabor_pca.nrrd", labelsImg)