import nrrd
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import binary_closing
from liverDataUtils.plotter import Plotter
from sklearn.cluster import KMeans
from scipy import ndimage
from liverDataUtils.fileNames import FileNames

sampleNumber = "01"
fileNames = FileNames()

liverData, liverHeader = nrrd.read(fileNames.getLiverCubeFileName(sampleNumber))
roiData, roiHeader =  nrrd.read(fileNames.getRoiCubeFileName(sampleNumber))
roiData = np.asarray(roiData).astype(bool)
# liver = np.multiply(liverData, roiData)

# closing 
index = 0
closedRoi = np.zeros((320, 260, 96), dtype=int)

# while i < 95:
#     closedRoi[:,:,i] = closing(closing(closing(closing(closing(roiData[..., i])))))
#     i = i+1
# mask = np.zeros((21, 21), dtype=int)
# mask[1:20, 1:20] = 1
# mask[20,20] = 1 
# mask[0,20] = 1 
# mask[0,0] = 1 
# mask[20,0] = 1 
# mask = np.array([[0, 0, 1, 0, 0],
#        [1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1],
#        [0, 0, 1, 0, 0]], dtype=bool)

# mask = ndimage.generate_binary_structure(2, 1)

# mask = np.array([[1,0,1],
#         [0,1,0],
#         [1,0,1]], dtype=bool)
# mask = ndimage.iterate_structure(mask, 10)

# while index < 95:
#     closedSlice = binary_closing(roiData[..., index], selem=mask)
#     binary_closing(closedSlice, selem=mask, out=closedSlice)
#     binary_closing(closedSlice, selem=mask, out=closedSlice)
#     binary_closing(closedSlice, selem=mask, out=closedSlice)
#     binary_closing(closedSlice, selem=mask, out=closedSlice)
#     binary_closing(closedSlice, selem=mask, out=closedSlice)

#     closedRoi[..., index] = closedSlice
#     index = index + 1



# plt.subplot(131)
# plt.imshow(closedSlice)
# plt.subplot(132)
# plt.imshow(roiData[..., sliceNumber])
# plt.subplot(133)
# plt.imshow(mask)

# plt.show()
liverDataClosed = (np.multiply(roiData, liverData)).reshape(3, -1)
# plotter(closedRoi, 43)

# K Means clustering 
# testSlice = liverDataClosed[..., 63] # just for the testing purposes

kmeans = KMeans(n_clusters=3)
# Fitting the input data
kmeans = kmeans.fit(liverDataClosed)
# Getting the cluster labels
labels = kmeans.predict(liverDataClosed)
# Centroid values
centroids = kmeans.cluster_centers_

print(centroids)
print(centroids.shape)
# plt.scatter(df['x'], df['y'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()
plt.imshow(labels)
