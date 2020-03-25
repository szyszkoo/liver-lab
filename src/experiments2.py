import numpy as np
import nrrd
from liverDataUtils.fileNames import FileNames
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
from liverDataUtils.n4BiasFieldCorretion import n4BiasFieldCorrection3D
import time
import constants.seeds
from liverDataUtils.imageSegmentation import otsuThreshold, regionGrowingWithUnsharpMasking, regionGrowing

liverReader = LiverReader()
fileNames = FileNames()
seeds = constants.seeds

def readApplyFunctionWriteToFile(sampleNumber, interpolationMethod, seed, regionGrowingSensitivity = 86, neighbourhood = 4, gaussSigma = 5):
    fileNamePrefix = "nearest_" if interpolationMethod == "nearest" else ""
    liver = liverReader.readNrrdData(f"results/base_interpolated_{interpolationMethod}/{fileNamePrefix}interpolatedCube{sampleNumber}.nrrd")
    n4 = liverReader.readNrrdData(f"results/n4_{interpolationMethod}/{interpolationMethod}_n4_liver{sampleNumber}.nrrd")
    roi = liverReader.readNrrdData(f"results/base_interpolated_{interpolationMethod}/{fileNamePrefix}interpolatedROI{sampleNumber}.nrrd")

    # calculate for liver
    result = regionGrowingWithUnsharpMasking(liver, seed, regionGrowingSensitivity, neighbourhood, gaussSigma)
    result = np.multiply(result, roi)

    # calculate for each liver after n4 filtering
    resultN4 = regionGrowingWithUnsharpMasking(n4, seed, regionGrowingSensitivity, neighbourhood, gaussSigma)
    resultN4 = np.multiply(resultN4, roi)

    # write results to files
    nrrd.write(f"results/regionGrowingWithUnsharpMasking_{regionGrowingSensitivity}/{sampleNumber}/{interpolationMethod}_regionGrowing{regionGrowingSensitivity}_liver{sampleNumber}.nrrd", result)
    nrrd.write(f"results/regionGrowingWithUnsharpMasking_{regionGrowingSensitivity}/{sampleNumber}/n4_{interpolationMethod}_regionGrowing{regionGrowingSensitivity}_liver{sampleNumber}.nrrd", resultN4)

start_time = time.time()
sampleNumbersWithSeeds = [("01", seeds.SEED01), ("02", seeds.SEED02), ("03", seeds.SEED03), ("15", seeds.SEED15)]
interpolationMethods = ["linear", "nearest"]
regionGrowingSensitivity = 92
errors = ""
# readApplyFunctionWriteToFile("15", "nearest")

# test = liverReader.readNrrdData(f"results/base_interpolated_nearest/nearest_interpolatedCube02.nrrd")
# nrrd.write("results/base_interpolated_nearest/nearest_interpolatedCube02.nrrd", test/255)

# apply n4 (or some other function) on each interpolated liver
for sampleNumber, seed in sampleNumbersWithSeeds:
    for interpolationMethod in interpolationMethods:
        print(f"Applying region growing on liver {sampleNumber} interpolated by {interpolationMethod} method")
        try:
            readApplyFunctionWriteToFile(sampleNumber, interpolationMethod, seed, regionGrowingSensitivity)
        except:
            errors += f"Could not apply region growing on liver {sampleNumber}, method {interpolationMethod} \n" 
        print("------ Execution time: %s seconds ------" % (time.time() - start_time))

print(errors)


