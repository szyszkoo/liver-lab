import numpy as np
import nrrd
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
from liverDataUtils.fileNames import FileNames
from frangi.frangi import frangi
import time 
from liverDataUtils.regionGrowing import RegionGrowing
from liverDataUtils.filters import medianFilter
from liverDataUtils.n4BiasFieldCorretion import n4BiasFieldCorrection3D

def fwhm2sigma(fwhm):
    # https://matthew-brett.github.io/teaching/smoothing_intro.html
    return fwhm / np.sqrt(8 * np.log(2))

start_time = time.time()

sampleNumber = "01"
liverReader = LiverReader()
fileNames = FileNames()
sigma = fwhm2sigma(5)
relativeFrangiPath_nearest = "results/frangi_interpolated_nearest/nearest_liverFrangi2D_02.nrrd"
relativeLiverPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedCube15.nrrd"
relativeRoiPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedROIData_15.nrrd"
relativeWholeDataPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedWholeData_15.nrrd"
relativeFrangiPath_linear = "results/frangi_interpolated_linear/liverFrangi2D_02.nrrd"
relativeLiverPath_linear = "results/base_interpolated_linear/interpolatedCube03.nrrd"
relativeRoiPath_linear = "results/base_interpolated_linear/interpolatedROI02.nrrd"
n4_nearest_liver15 = "results/base_interpolated_nearest/nearest_interpolatedCube15_n4.nrrd"

n4 = liverReader.readNrrdData(n4_nearest_liver15)
path = "regionGrowing_linear_02_085.nrrd"
otsuWithRegionGrowingPath = "results/other_results/otsu_with_regionGrowing.nrrd"
regionGrowingPath = "results/other_results/regionGrowing_sensitivity90.nrrd"

roi = liverReader.readNrrdData(relativeRoiPath_nearest)
wholeData = liverReader.readNrrdData(relativeWholeDataPath_nearest)
filtered = medianFilter(roi)
liver = filtered * wholeData / 255

# liverCorrected = n4BiasFieldCorrection3D(liver)
Plotter(n4 - liver, liver, 150)
print("------ Execution time: %s seconds ------" % (time.time() - start_time))

# Plotter(liverCorrected, liver, 150)
# nrrd.write("results/base_interpolated_nearest/nearest_interpolatedCube15_n4.nrrd", liverCorrected)