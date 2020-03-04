import numpy as np
import nrrd
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
from liverDataUtils.fileNames import FileNames
from liverDataUtils.binaryMaskToRgb import BinaryMaskToRgb
from frangi.frangi import frangi
import time 
from liverDataUtils.regionGrowing import RegionGrowing
from liverDataUtils.filters import medianFilter

def fwhm2sigma(fwhm):
    # https://matthew-brett.github.io/teaching/smoothing_intro.html
    return fwhm / np.sqrt(8 * np.log(2))

start_time = time.time()

sampleNumber = "01"
liverReader = LiverReader()
fileNames = FileNames()
binaryToRgb = BinaryMaskToRgb()
sigma = fwhm2sigma(5)
relativeFrangiPath_nearest = "results/frangi_interpolated_nearest/nearest_liverFrangi2D_02.nrrd"
relativeLiverPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedCube02.nrrd"
relativeRoiPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedROIData_15.nrrd"
relativeFrangiPath_linear = "results/frangi_interpolated_linear/liverFrangi2D_02.nrrd"
relativeLiverPath_linear = "results/base_interpolated_linear/interpolatedCube02.nrrd"
relativeRoiPath_linear = "results/base_interpolated_linear/interpolatedROI02.nrrd"

path = "regionGrowing_linear_02_085.nrrd"


roi = liverReader.readNrrdData(relativeRoiPath_nearest)
filteredRoi = medianFilter(roi)
# mask = regionGrowingWithUnsharpMasking(frangiData, (140, 191, 165), 4, sigma)
print("------ Execution time: %s seconds ------" % (time.time() - start_time))
# liverData[:,191,165] = 1
# liverData[140,:,165] = 1

Plotter(roi, filteredRoi, 141)
nrrd.write("results/base_interpolated_nearest/nearest_interpolatedROIData_15_corrected.nrrd", filteredRoi.astype(int)*255)