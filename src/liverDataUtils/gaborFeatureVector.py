import numpy as np
from skimage.filters import gabor

def createGaborFeatureVector(image):
    # create params vectors for each parameter: frequency, theta, bandwidth, n_stds
    freq = np.arange(0.1, 1.1, 0.05)
    theta = np.arange(0, 360, 30)
    bandwith = np.arange(0.5, 1.6, 0.1)
    # n_stds = np.arange(3, 50, 2)

    # small values just to see the results quickly 
    # freq = np.arange(0.3, 0.5, 0.1)
    # theta = np.arange(0, 360, 90)
    # bandwith = np.arange(0.5, 1.6, 0.5)
    # n_stds = np.arange(3, 17, 6)

    # create the empty output cube
    featureVectorLen = freq.size * theta.size * bandwith.size
    output = np.empty((image.shape[0], image.shape[1], featureVectorLen+1))

    # iterate over each params vector value, apply gabor filter and save single result slice as a new slice in the output cube
    output[:,:,0] = image
    currentSlice = 1

    for freqValue in freq:
        for thetaValue in theta: 
            for bandwithValue in bandwith: 
                print(f"{freqValue}, {thetaValue}, {bandwithValue}")
                print(f"{currentSlice}/{featureVectorLen}")
                output[:,:,currentSlice], _ = gabor(image, frequency=freqValue, theta=thetaValue, bandwidth=bandwithValue)
                currentSlice += 1

    return output