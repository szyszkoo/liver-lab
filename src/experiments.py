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
from liverDataUtils.imageSegmentation import otsuThreshold, regionGrowingWithUnsharpMasking, regionGrowing, gaborFilter
from skimage.filters import gabor
def fwhm2sigma(fwhm):
    # https://matthew-brett.github.io/teaching/smoothing_intro.html
    return fwhm / np.sqrt(8 * np.log(2))

start_time = time.time()

sampleNumber = "01"
interpolationMethod = "linear"
liverReader = LiverReader()
fileNames = FileNames()
sigma = fwhm2sigma(5)
relativeFrangiPath_nearest = "results/frangi_interpolated_nearest/nearest_liverFrangi2D_02.nrrd"
relativeLiverPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedCube15.nrrd"
relativeRoiPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedROIData_15_corrected.nrrd"
relativeWholeDataPath_nearest = "results/base_interpolated_nearest/nearest_interpolatedWholeData_15.nrrd"
relativeFrangiPath_linear = "results/frangi_interpolated_linear/liverFrangi2D_02.nrrd"
relativeLiverPath_linear = "results/base_interpolated_linear/interpolatedCube03.nrrd"
relativeRoiPath_linear = "results/base_interpolated_linear/interpolatedROI02.nrrd"

n4 = f"results/n4_{interpolationMethod}/{interpolationMethod}_n4_liver{sampleNumber}.nrrd"

# n4 = liverReader.readNrrdData(n4_nearest_liver15)
path = "regionGrowing_linear_02_085.nrrd"
otsuWithRegionGrowingPath = "results/other_results/otsu_with_regionGrowing.nrrd"
regionGrowingPath = "results/other_results/regionGrowing_sensitivity90.nrrd"
regionGrowing86 = "results/other_results/regionGrowing_086_nearest_15.nrrd"

data = liverReader.readNrrdData(relativeLiverPath_linear)
# roi = liverReader.readNrrdData(relativeRoiPath_nearest)/255
# wholeData = liverReader.readNrrdData(relativeWholeDataPath_nearest)
# filtered = medianFilter(roi)
# liver = filtered * wholeData / 255
singleSlice = data[:,:,120]
singleSliceFiltered, _ = gabor(singleSlice, 0.4)
Plotter(singleSlice, singleSliceFiltered)
# filtered = gaborFilter(data, 3)
# Plotter(filtered, data, 120)
# Plotter(connected, data, 120)
print("------ Execution time: %s seconds ------" % (time.time() - start_time))

# Plotter(liverCorrected, liver, 150)
# nrrd.write("results/other_results/regionGrowing_086_connected_nearest_15.nrrd", output.astype(int))