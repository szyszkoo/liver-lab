import nrrd
import numpy as np
from fileNames import FileNames

class LiverReader:
    def readLiverData(self, sampleNumber):
        fileNames = FileNames()
        liverData, _ = nrrd.read(fileNames.getLiverCubeFileName(sampleNumber))
        roiData, _ =  nrrd.read(fileNames.getRoiCubeFileName(sampleNumber))
        roiData = roiData/255

        return np.multiply(liverData, roiData)