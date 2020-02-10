import numpy as np
import nrrd
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
# from regionGrowing import RegionGrowing
from liverDataUtils.fileNames import FileNames
# from skimage.filters import gaussian
from frangi.frangi import frangi
import time 
from scipy.ndimage import gaussian_filter
from liverDataUtils.regionGrowing import RegionGrowing
from skimage.filters import threshold_otsu, median

def fwhm2sigma(fwhm):
    # https://matthew-brett.github.io/teaching/smoothing_intro.html
    return fwhm / np.sqrt(8 * np.log(2))

def normalize(value, maxValue, minValue):
    return 255*(value-minValue)/(maxValue - minValue)

start_time = time.time()

sampleNumber = "15"
liverReader = LiverReader()
fileNames = FileNames()
# cubeInterpolator = CubeInterpolator()
regionGrowing = RegionGrowing()
sigma = fwhm2sigma(5)
print(sigma)
liverData = liverReader.readInterpolatedLiverData(sampleNumber)

# Test data

# nx = 61; ny = 51; nz = 71

# tx = np.linspace(-3,3,nx)
# ty = np.linspace(-3,3,ny)
# tz = np.linspace(-3,3,nz)

# x,y,z = np.meshgrid(tx,ty,tz)

# w = x**4 - 5*x**2 + y**4 - 5*y**2 + z**4 - 5*z**2

# vol = -np.ones_like(w)
# vol[np.logical_and(w >= 5, w<=20)] = 1.
# vol[w <= -11] = 1.
# vol = vol +2
# Plotter(vol, vol, 1)


# src = mlab.pipeline.scalar_field(w)

roi = liverReader.readInterpolatedLiverData("15")
# frangi = liverReader.readNrrdData("testFrangi2D.nrrd")
# liverData = np.multiply(frangi, roi) # comment this to process the operations on the whole liver pic

# Gaussian blur
liverDataGauss = gaussian_filter(liverData, sigma=sigma)
# unsharp masking
origMinusBlurred = liverData - liverDataGauss
unsharpened = liverData + origMinusBlurred * 2.5
# print(np.min(origMinusBlurred))
maxValue = np.max(unsharpened)
minValue = np.min(unsharpened)
# unsharpenedNorm = np.array([normalize(x, maxValue, minValue) for x in unsharpened]) * roi
# (120, 145)
# mask = threshold_otsu(unsharpened)
# mask = np.zeros((liverData.shape[0], liverData.shape[1], liverData.shape[2]), dtype=float)

# otsu threshold 
sum = 0
counter = 0
for index in np.arange(0, unsharpened.shape[2], 1):
    if unsharpened[:, :, index].min() != unsharpened[:, :, index].max():
        thr = threshold_otsu(unsharpened[:, :, index])
        if(thr>0):
            sum += thr
            counter +=1
thres = sum/counter
print(thres)
thres+=100

# # median filter and region growing for thresholded data
# output = unsharpened<thres
# for index in np.arange(0, output.shape[2], 1):
#     output[:,:,index] = median(output[:,:,index])
# output = output*roi
# regionMask = regionGrowing.grow(output, (120,145,150), 2) # make sure to use a proper condition inside 'grow' method
# unsharpened = liverReader.readNrrdData("regionGrowing_sensitivity90.nrrd")
unsharpened[:,191,166] = 0
unsharpened[151,:,166] = 0
# regionMask = regionGrowing.grow(unsharpened, (120,145,150), 4)
# regionMask=regionMask * roi
print("------ Execution time: %s seconds ------" % (time.time() - start_time))
Plotter(unsharpened, liverData, 150)
# nrrd.write("regionGrowing_sensitivity90_connected.nrrd", (regionMask).astype(int)*255)

