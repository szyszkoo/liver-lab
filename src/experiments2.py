import numpy as np
import nrrd
from liverDataUtils.fileNames import FileNames
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter

sampleNumber = "02"
liverReader = LiverReader()
fileNames = FileNames()

wholeData = liverReader.readNrrdData(f"results/base_interpolated_nearest/nearest_interpolatedWholeData_{sampleNumber}.nrrd")
roiData = liverReader.readNrrdData(f"results/base_interpolated_nearest/nearest_interpolatedROIData_{sampleNumber}_corrected.nrrd")/255

liver = np.multiply(wholeData, roiData)
# Plotter(liver, roiData,150)
nrrd.write(f"results/base_interpolated_nearest/nearest_interpolatedCube{sampleNumber}_corrected.nrrd", liver)