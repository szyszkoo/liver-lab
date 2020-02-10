import numpy as np
import nrrd
from liverDataUtils.fileNames import FileNames
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter

sampleNumber = "02"
liverReader = LiverReader()
fileNames = FileNames()

wholeData = liverReader.readInterpolatedWholeData(sampleNumber)
roiData = liverReader.readInterpolatedRoiData(sampleNumber)

liver = np.multiply(wholeData, roiData)
Plotter(liver, roiData,150)
nrrd.write(fileNames.getInterpolatedCubeFileName(sampleNumber), liver)