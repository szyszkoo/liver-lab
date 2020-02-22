import numpy as np
import matplotlib.pyplot as plt
import nrrd

from liverDataUtils.liverReader import LiverReader
import sys
sys.path.append("~/repo/liver-lab/frangi/")

from frangi.frangi import frangi
from liverDataUtils.plotter import Plotter

from skimage.filters import frangi as frangi2D

def writeFrangi2Dand3DToNrrdFiles(sampleNumber, liverData, roiData):
    livfrang = frangi(liverData)
    liverFrangi3D = np.multiply(livfrang, roiData)
    livfrang = np.zeros((liverData.shape[0], liverData.shape[1], liverData.shape[2]), dtype=float)

    for index in np.arange(0, liverData.shape[2], 1):
        livfrang[:, :, index] = frangi2D(liverData[:, :, index])

    liverFrangi2D = np.multiply(livfrang, roiData)
    # Plotter(liverFrangi3D, liverFrangi2D, 150)
    
    filename2D = 'nearest_liverFrangi2D_' + sampleNumber + '.nrrd'
    filename3D = 'nearest_liverFrangi3D_' + sampleNumber + '.nrrd'
    nrrd.write(filename2D, liverFrangi2D)
    nrrd.write(filename3D, liverFrangi3D)

sampleNumber = "01"
liverReader = LiverReader()
# liverData = liverReader.readInterpolatedLiverData(sampleNumber)
# roiData = liverReader.readInterpolatedRoiData(sampleNumber)
liverData = liverReader.readNrrdData(f"nearest_interpolatedCube{sampleNumber}.nrrd")
roiData = liverReader.readNrrdData(f"nearest_interpolatedROIData_{sampleNumber}.nrrd")/255

writeFrangi2Dand3DToNrrdFiles(sampleNumber, liverData, roiData)


sampleNumber = "02"
liverReader = LiverReader()
# liverData = liverReader.readInterpolatedLiverData(sampleNumber)
# roiData = liverReader.readInterpolatedRoiData(sampleNumber)
liverData = liverReader.readNrrdData(f"nearest_interpolatedCube{sampleNumber}.nrrd")
roiData = liverReader.readNrrdData(f"nearest_interpolatedROIData_{sampleNumber}.nrrd")/255

writeFrangi2Dand3DToNrrdFiles(sampleNumber, liverData, roiData)


sampleNumber = "03"
liverReader = LiverReader()
# liverData = liverReader.readInterpolatedLiverData(sampleNumber)
# roiData = liverReader.readInterpolatedRoiData(sampleNumber)
liverData = liverReader.readNrrdData(f"nearest_interpolatedCube{sampleNumber}.nrrd")
roiData = liverReader.readNrrdData(f"nearest_interpolatedROIData_{sampleNumber}.nrrd")/255

writeFrangi2Dand3DToNrrdFiles(sampleNumber, liverData, roiData)


sampleNumber = "15"
liverReader = LiverReader()
# liverData = liverReader.readInterpolatedLiverData(sampleNumber)
# roiData = liverReader.readInterpolatedRoiData(sampleNumber)
liverData = liverReader.readNrrdData(f"nearest_interpolatedCube{sampleNumber}.nrrd")
roiData = liverReader.readNrrdData(f"nearest_interpolatedROIData_{sampleNumber}.nrrd")/255

writeFrangi2Dand3DToNrrdFiles(sampleNumber, liverData, roiData)
