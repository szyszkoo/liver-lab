import numpy as np
import nrrd
from liverDataUtils.liverReader import LiverReader
import time 
import matplotlib.pyplot as plt

def getClustersMeans(labelsImg, originalImg):
    minClassValue = labelsImg.min().astype(int)
    maxClassValue = labelsImg.max().astype(int) + 1
    classes = np.arange(minClassValue, maxClassValue, 1)
    results = np.empty((classes.size), dtype=object)

    for classNo in classes:
        classImage = labelsImg == classNo
        origImgInsideClass = np.multiply(originalImg, classImage)
        results[classNo] = (classNo, (origImgInsideClass[origImgInsideClass != 0]).mean())

    return results

def checkVascular(img, sampleNumber, sliceNumber):
    # init
    liverReader = LiverReader()
    start_time = time.time()

    # get template (original, correct ROI for vascular part)
    liverVascularFilePath = f"results/base/VASCULAR_roiLiver{sampleNumber}.nrrd"
    # liverFilePath = f"results/base/LIVER_roiLiver{sampleNumber}.nrrd"
    template = liverReader.readNrrdData(liverVascularFilePath)/255
    # liverRoi = liverReader.readNrrdData(liverFilePath)/255
    template = template[..., sliceNumber]
    # liverRoi = liverRoi[..., sliceNumber]

    # compare each class from given pic with template
    minClassValue = img.min().astype(int)
    maxClassValue = img.max().astype(int) + 1
    classes = np.arange(minClassValue, maxClassValue, 1)
    results = np.empty((classes.size, 2))
    incorrectPixelsForClasses = np.empty((img.shape[0], img.shape[1], classes.size))

    for classNo in classes:
        classImage = img == classNo
        correctPixels = 0
        for (i,j), value in np.ndenumerate(classImage):
            if (value != template[i,j]):
                incorrectPixelsForClasses[i,j,classNo] = 1
            if (value == template[i,j] and template[i,j] == 1):
                correctPixels += 1
        pixelsCount = np.count_nonzero(template)
        percentCorrect = correctPixels*100/pixelsCount
        results[classNo] = (classNo, percentCorrect)
        print(f"CLASS {classNo}: {correctPixels} out of {pixelsCount} are correct ({correctPixels*100/pixelsCount}%)")
    
    # return tuple of matrix containing percentage accordance with the template for each class
    # format: [classNo, percentage]
    # and a matrix of incorrect pixels for each class 
    print("------ Execution time: %s seconds ------" % (time.time() - start_time))

    return (results, incorrectPixelsForClasses)
