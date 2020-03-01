import numpy as np
import nrrd
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
from liverDataUtils.fileNames import FileNames
from liverDataUtils.binaryMaskToRgb import BinaryMaskToRgb
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

def regionGrowingWithUnsharpMasking(dataCube, seed, neighbourhood, gaussSigma):
    # Gaussian blur
    liverDataGauss = gaussian_filter(dataCube, sigma=gaussSigma)
    # unsharp masking
    origMinusBlurred = dataCube - liverDataGauss
    unsharpened = dataCube + origMinusBlurred * 1.5
    # unsharpenedNorm = np.array([normalize(x, maxValue, minValue) for x in unsharpened]) * roi
    regionMask = regionGrowing.grow(unsharpened, seed, neighbourhood) # make sure to use a proper condition inside 'grow' method

    return regionMask

def otsuThreshold(dataCube):
    sum = 0
    counter = 0
    for index in np.arange(0, dataCube.shape[2], 1):
        if dataCube[:, :, index].min() != dataCube[:, :, index].max():
            thr = threshold_otsu(dataCube[:, :, index])
            if(thr>0):
                sum += thr
                counter +=1
    thres = sum/counter
    print(f"Thres: {thres}")

    return dataCube < thres


start_time = time.time()

sampleNumber = "01"
liverReader = LiverReader()
fileNames = FileNames()
regionGrowing = RegionGrowing()
binaryToRgb = BinaryMaskToRgb()
sigma = fwhm2sigma(5)
relativeFrangiPath_nearest = "results/frangi_interpolated_nearest/nearest_liverFrangi2D_02.nrrd"
relativeLiverPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedCube02.nrrd"
relativeRoiPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedROIData_02.nrrd"
relativeFrangiPath_linear = "results/frangi_interpolated_linear/liverFrangi2D_02.nrrd"
relativeLiverPath_linear = "results/base_interpolated_linear/interpolatedCube02.nrrd"
relativeRoiPath_linear = "results/base_interpolated_linear/interpolatedROI02.nrrd"

path = "regionGrowing_linear_02_085.nrrd"

test = liverReader.readNrrdData(path)

frangiData = liverReader.readNrrdData(relativeFrangiPath_linear)


liverData = liverReader.readNrrdData(relativeLiverPath_linear)
roi = liverReader.readNrrdData(relativeRoiPath_linear)/255
print(roi.shape)
maskRgb = binaryToRgb.convert(test, True)
liverRgb = binaryToRgb.convert(liverData, False)
print(liverRgb.shape)
print(np.max(liverRgb))
print(np.min(liverRgb))
# mask = regionGrowingWithUnsharpMasking(frangiData, (140, 191, 165), 4, sigma)
print("------ Execution time: %s seconds ------" % (time.time() - start_time))
# liverData[:,191,165] = 1
# liverData[140,:,165] = 1

Plotter(maskRgb + liverRgb, liverData, 150)
# nrrd.write("regionGrowing_linearFrangi_02_15.nrrd", (np.multiply(mask, roi)).astype(int)*255)