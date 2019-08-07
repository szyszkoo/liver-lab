import nrrd
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import closing

liverData, liverHeader = nrrd.read("./myTestLiverCube2.nrrd")
roiData, roiHeader =  nrrd.read("./myROI_LIVER2.nrrd")
roiData = roiData/255
liver = np.multiply(liverData, roiData)

test = np.ravel(liver)
test = [x for x in test if x != 0] # can be changed to only select the pixels inside the ROI 
# to avoid losing the 0s inside the ROI

histogram = np.histogram(test)

# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(x=test, bins=np.arange(0, 512, 1), color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Liver data histogram')
maxfreq = n.max()
# Set a clean upper y-axis limit.
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.show()

print(np.amax(test))
print(np.amin(test))

