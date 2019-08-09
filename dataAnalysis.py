import nrrd
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import closing
from sklearn.cluster import KMeans

liverData, liverHeader = nrrd.read("./myTestLiverCube2.nrrd")
roiData, roiHeader =  nrrd.read("./myROI_LIVER2.nrrd")
roiData = roiData/255
liver = np.multiply(liverData, roiData)

test = np.ravel(liver)
test = [x for x in test if x != 0] # can be changed to only select the pixels inside the ROI 
# to avoid losing the 0s inside the ROI

# histogram = np.histogram(test)

# # An "interface" to matplotlib.axes.Axes.hist() method
# n, bins, patches = plt.hist(x=test, bins=np.arange(0, 512, 1), color='#0504aa',
#                             alpha=0.7, rwidth=0.85)
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Liver data histogram')
# maxfreq = n.max()
# # Set a clean upper y-axis limit.
# plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
# plt.show()
#
# print(np.amax(test))
# print(np.amin(test))



liverROI = np.ravel(liver)

# kmeans = KMeans( n_clusters=4, init='k-means++', n_init=10, random_state=0 )
# kmeans = kmeans.fit(liverROI.reshape(-1, 1))
# labb=kmeans.labels_
# # np.disp( kmeans.labels_ )
#
#
#
# labels = kmeans.predict( liverROI.reshape(-1, 1) )
# # np.disp( labels )
# # plt.plot(labels)
#
# centers = kmeans.cluster_centers_
# np.disp( centers )
#
# # np.disp(liverROI.shape)
#
# result=labels.reshape(320, 260, 96)
#
#
# plt.imshow(result[:, :, 76])
# plt.show()

# plt.scatter( centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5 )


liverROI = liverROI.reshape(320, 260, 96)
rows = 320
columns = 260
slices = 96

resultt = np.zeros((320, 260, 96))

for i in range(rows):
    for j in range(columns):
        for k in range(slices):
            if liverROI[i][j][k]< 1:
                resultt[i][j][k] = 0
            elif liverROI[i][j][k] >= 1 and liverROI[i][j][k] < 160:
                resultt[i][j][k] = 1
            elif liverROI[i][j][k] >= 170 and liverROI[i][j][k] < 205:
                resultt[i][j][k] = 2
            else:
                resultt[i][j][k] = 3


plt.imshow(resultt[:, :, 76])
plt.show()
