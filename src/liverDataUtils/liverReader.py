import pydicom
import nrrd
import os
import numpy as np
from matplotlib.path import Path
from liverDataUtils.fileNames import FileNames

class LiverReader:
    def readLiverData(self, sampleNumber):
        fileNames = FileNames()
        liverData, _ = nrrd.read(fileNames.getLiverCubeFileName(sampleNumber))
        roiData, _ =  nrrd.read(fileNames.getRoiCubeFileName(sampleNumber))
        roiData = roiData/255

        return np.multiply(liverData, roiData)

    def readInterpolatedLiverData(self, sampleNumber):
        fileNames = FileNames()
        liverData, _ = nrrd.read(fileNames.getInterpolatedCubeFileName(sampleNumber))

        return liverData

    def readLiverROIData(self, sampleNumber):
        fileNames = FileNames()
        roiData, _ =  nrrd.read(fileNames.getRoiCubeFileName(sampleNumber))
        roiData = roiData/255

        return roiData
