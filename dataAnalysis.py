import nrrd
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import closing
from liverDataUtils.liverReader import LiverReader

sampleNumber = "01"
liverReader = LiverReader()
liver = liverReader.readLiverData(sampleNumber)

liverVector = np.ravel(liver)
liverVector = [x for x in liverVector if x != 0] # can be changed to only select the pixels inside the ROI 
# to avoid losing the 0s inside the ROI

histogram = np.histogram(liverVector)

# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(x=liverVector, bins=np.arange(0, 512, 1), color='#0504aa',
                            alpha=0.7, rwidth=1)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Liver data histogram')
maxfreq = n.max()
# Set a clean upper y-axis limit.
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.show()

print(np.amax(liverVector))
print(np.amin(liverVector))

