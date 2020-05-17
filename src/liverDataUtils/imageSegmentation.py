from liverDataUtils.regionGrowing import RegionGrowing
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage.filters import threshold_otsu, median, gabor

def normalize(value, maxValue, minValue):
    return 255*(value-minValue)/(maxValue - minValue)

def regionGrowingWithUnsharpMasking(dataCube, seed, sensitivity, neighbourhood, gaussSigma):
    regionGrowing = RegionGrowing()
    # Gaussian blur
    liverDataGauss = gaussian_filter(dataCube, sigma=gaussSigma)
    # unsharp masking
    origMinusBlurred = dataCube - liverDataGauss
    unsharpened = dataCube + origMinusBlurred * 1.5
    # unsharpenedNorm = np.array([normalize(x, maxValue, minValue) for x in unsharpened]) * roi
    regionMask = regionGrowing.grow(unsharpened, seed, sensitivity, neighbourhood) # make sure to use a proper condition inside 'grow' method

    return regionMask

def unsharpMasking(dataCube, gaussSigma):
    # Gaussian blur
    liverDataGauss = gaussian_filter(dataCube, sigma=gaussSigma)
    # unsharp masking
    origMinusBlurred = dataCube - liverDataGauss
    unsharpened = dataCube + origMinusBlurred * 1.5
    # unsharpenedNorm = np.array([normalize(x, maxValue, minValue) for x in unsharpened]) * roi

    return unsharpened

def regionGrowing(dataCube, seed, sensitivity, neighbourhood):
    regionGrowing = RegionGrowing()
    regionMask = regionGrowing.grow(dataCube, seed, sensitivity, neighbourhood) # make sure to use a proper condition inside 'grow' method

    return regionMask

def otsuThreshold(dataCube):
    sum = 0
    counter = 0
    for index in np.arange(0, dataCube.shape[2], 1):
        if dataCube[:, :, index].min() != dataCube[:, :, index].max(): # avoid analysing slices outside of roi (whole slice of zeros)
            thr = threshold_otsu(dataCube[:, :, index])
            if(thr>0):
                sum += thr
                counter +=1
    thres = sum/counter
    print(f"Thres: {thres}")

    return dataCube < thres

def gaborFilter(dataCube, frequency=0.6):
    dataCube = np.array(dataCube)
    filtered = np.zeros(dataCube.shape)

    for index in np.arange(0, dataCube.shape[2], 1):
        filtered[:,:,index], _ = gabor(dataCube[:,:,index], frequency=frequency)
        # filtered[:,:,index] = gabor(dataCube[:,:,index])

    return filtered