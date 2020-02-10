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

    def readWholeLiverData(self, sampleNumber):
        fileNames = FileNames()
        liverData, _ = nrrd.read(fileNames.getLiverCubeFileName(sampleNumber))

        return liverData

    def readInterpolatedLiverData(self, sampleNumber):
        fileNames = FileNames()
        liverData, _ = nrrd.read(fileNames.getInterpolatedCubeFileName(sampleNumber))

        return liverData

    def readInterpolatedWholeData(self, sampleNumber):
        fileNames = FileNames()
        data, _ = nrrd.read(fileNames.getInterpolatedWholeDataFileName(sampleNumber))

        return data

    def readInterpolatedRoiData(self, sampleNumber):
        fileNames = FileNames()
        roiData, _ = nrrd.read(fileNames.getInterpolatedRoiFileName(sampleNumber))

        return roiData

    def readLiverROIData(self, sampleNumber):
        fileNames = FileNames()
        roiData, _ =  nrrd.read(fileNames.getRoiCubeFileName(sampleNumber))
        roiData = roiData/255

        return roiData

    def readNrrdData(self, fileName):
        data, _ = nrrd.read(fileName)
        return data