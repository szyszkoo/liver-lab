from liverDataUtils.regionGrowing import RegionGrowing
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage.filters import threshold_otsu, median

def normalize(self, value, maxValue, minValue):
    return 255*(value-minValue)/(maxValue - minValue)

def regionGrowingWithUnsharpMasking(self, dataCube, seed, neighbourhood, gaussSigma):
    regionGrowing = RegionGrowing()
    # Gaussian blur
    liverDataGauss = gaussian_filter(dataCube, sigma=gaussSigma)
    # unsharp masking
    origMinusBlurred = dataCube - liverDataGauss
    unsharpened = dataCube + origMinusBlurred * 1.5
    # unsharpenedNorm = np.array([normalize(x, maxValue, minValue) for x in unsharpened]) * roi
    regionMask = regionGrowing.grow(unsharpened, seed, neighbourhood) # make sure to use a proper condition inside 'grow' method

    return regionMask

def otsuThreshold(self, dataCube):
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