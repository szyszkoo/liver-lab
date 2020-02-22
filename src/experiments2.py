import numpy as np
import nrrd
from liverDataUtils.fileNames import FileNames
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter

sampleNumber = "15"
liverReader = LiverReader()
fileNames = FileNames()

wholeData = liverReader.readNrrdData(f"nearest_interpolatedWholeData_{sampleNumber}.nrrd")
roiData = liverReader.readNrrdData(f"nearest_interpolatedROIData_{sampleNumber}.nrrd")/255

liver = np.multiply(wholeData, roiData)
# Plotter(liver, roiData,150)
nrrd.write(f"nearest_interpolatedCube{sampleNumber}.nrrd", liver)