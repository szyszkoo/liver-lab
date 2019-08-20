from sklearn.mixture import GaussianMixture
import nrrd
import numpy as np


liverData, liverHeader = nrrd.read("./myTestLiverCube2.nrrd")
roiData, roiHeader =  nrrd.read("./myROI_LIVER2.nrrd")
roiData = np.asarray(roiData).astype(bool)
liverData = (np.multiply(roiData, liverData))

# closedRoi = np.zeros((320, 260, 96), dtype=int)
# for x in liverData: 
#     switch(x) {
#         case x < 
#     }

# gmm = GaussianMixture(n_components=3).fit(liverData)
# labels = gmm.predict(liverData)

# print(labels)
# plt.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis');