import numpy as np
import nrrd
from liverDataUtils.liverReader import LiverReader
import time 
import matplotlib.pyplot as plt


def checkVascular(img, sampleNumber):
    # init
    liverReader = LiverReader()
    start_time = time.time()

    # get template (original, correct ROI for vascular part)
    liverVascularFilePath = f"results/base/VASCULAR_roiLiver{sampleNumber}.nrrd"
    liverFilePath = f"results/base/LIVER_roiLiver{sampleNumber}.nrrd"
    template = liverReader.readNrrdData(liverVascularFilePath)/255
    liverRoi = liverReader.readNrrdData(liverFilePath)/255
    template = template[..., 56]
    liverRoi = liverRoi[..., 56]
    
    # compare each class from given pic with template
    minClassValue = img.min()
    maxClassValue = img.max() + 1
    classes = np.arange(minClassValue, maxClassValue, 1)

    for classNo in classes:
        classImage = img == classNo
        correctPixels = 0
        for (i,j), value in np.ndenumerate(classImage):
            if (value == template[i,j] and template[i,j] == 1):
                correctPixels += 1
        pixelsCount = np.count_nonzero(template)
        print(f"CLASS {classNo}: {correctPixels} out of {pixelsCount} are correct ({correctPixels*100/pixelsCount}%)")
    
    # return matrix containing percentage accordance with the template for each class
    # format: [classNo, percentage]

    print("------ Execution time: %s seconds ------" % (time.time() - start_time))