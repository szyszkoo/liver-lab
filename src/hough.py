import numpy as np
import matplotlib.pyplot as plt
import nrrd

from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage.morphology import binary_closing, binary_opening

from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter

liverReader = LiverReader()
vascular = img_as_ubyte(liverReader.readNrrdData("results/kmeans/3_0.nrrd"))
# vascular = liverReader.readNrrdData("results/kmeans/3_0.nrrd")
# vascular = img_as_ubyte(binary_closing(vascular))

sampleNumber = "16" # 16/ 18 / 03
sliceNumber = 56 # 56 / 47 / 183

# read liver data
liverWholeDataFilePath = f"results/base/liverCube{sampleNumber}.nrrd"
liverRoiFilePath = f"results/base/roiLiver{sampleNumber}.nrrd"

liverRoi = liverReader.readNrrdData(liverRoiFilePath)/255
liverWholeData = liverReader.readNrrdData(liverWholeDataFilePath)
liver = np.multiply(liverRoi, liverWholeData)
# liver = liverReader.readNrrdData("results/base_interpolated_linear/interpolatedCube03.nrrd")

# get single slice
img = liver[:, :, sliceNumber]
# img = vascular
edges = canny(img, sigma=3)
Plotter(edges, img)
hough_radii = np.arange(10, 50, 1)
hough_res = hough_circle(edges, hough_radii)

accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=1)

# Draw them
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
img3d = color.gray2rgb(img)

for center_y, center_x, radius in zip(cy, cx, radii):
    circy, circx = circle_perimeter(center_y, center_x, radius,
                                    shape=vascular.shape)
    # print(f"circ y: {circy} circ x: {circx }")
    img3d[circy, circx] = (220, 20, 20)

# Plotter(vascular, edges)
ax.imshow(np.fliplr(np.rot90(img3d, k=3)))
plt.show()