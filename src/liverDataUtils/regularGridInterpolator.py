import numpy as np
import scipy.interpolate as spint
from liverDataUtils.fileNames import FileNames
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import nrrd
import time 

def interpolate(sampleNumber):
    start_time = time.time()
    RGI = spint.RegularGridInterpolator 
    liverReader = LiverReader()
    fileNames = FileNames()
    pixelSpacing = 1.1875 # x and y position
    sliceThickness = 3 # z position
    liverData = liverReader.readWholeLiverData(sampleNumber)

    xDimension = int(np.ceil(liverData.shape[0] * pixelSpacing))
    yDimension = int(np.ceil(liverData.shape[1] * pixelSpacing))
    zDimension = int(np.ceil(liverData.shape[2] * sliceThickness))

    x = np.linspace(1, liverData.shape[0], liverData.shape[0])
    y = np.linspace(1, liverData.shape[1], liverData.shape[1])
    z = np.linspace(1, liverData.shape[2], liverData.shape[2])

    rgi = RGI(points=[x,y,z], values=liverData)
    previ=-1
    # print(rgi((1.6842105263157894,1.6842105263157894,27.0)))
    # in order to interpolate a ROI file, change below array type to "bool". Otherwise, its type should be "int"
    interpolatedDataCube = np.zeros((int(np.ceil(xDimension)), int(np.ceil(yDimension)), int(np.ceil(zDimension))), dtype=int)
    for (i,j,k), value in np.ndenumerate(interpolatedDataCube):
        if(previ != i):
            print(f"{i}/{xDimension}") # just to keep the progress visible
            if(i == 40 or i== 80 or i == 140):
                nrrd.write(f"TMP_testInterpolatedFull{sampleNumber}_{i}.nrrd", interpolatedDataCube)#.astype(int)*255)
                print("------ Execution time: %s seconds ------" % (time.time() - start_time))
        
        previ = i

        iAdjusted = i/pixelSpacing
        jAdjusted = j/pixelSpacing
        kAdjusted = k/sliceThickness
        if(iAdjusted>=1 and jAdjusted >= 1 and kAdjusted >= 1):
            interpolatedDataCube[i, j, k] = rgi((iAdjusted, jAdjusted, kAdjusted))
        else:
            pass # just to handle borders - they are all zeros anyway

    # for i in range(1, xDimension):
    #     print(f"{i}/{xDimension}")
    #     if(i == 40 or i== 80 or i == 140):
    #         nrrd.write("testInterpolated03.nrrd", interpolatedDataCube.astype(int)*255)
    #     for j in range(1, yDimension):
    #         for k in range(1, zDimension):
    #             iAdjusted = i/pixelSpacing
    #             jAdjusted = j/pixelSpacing
    #             kAdjusted = k/sliceThickness
    #             if(iAdjusted>=1 and jAdjusted >= 1 and kAdjusted >= 1):
    #                 interpolatedDataCube[i, j, k] = rgi((iAdjusted, jAdjusted, kAdjusted))
    #             else:
    #                 pass # just to handle borders - they are all zeros anyway

    # nrrd.write("testInterpolated03.nrrd", interpolatedDataCube.astype(int)*255)
    nrrd.write(fileNames.getInterpolatedWholeDataFileName(sampleNumber), interpolatedDataCube)#.astype(int)*255)
    print("------ Execution time: %s seconds ------" % (time.time() - start_time))
# Plotter(liverData, interpolatedDataCube)

print(f"Time strted: {time.time()}")
interpolate("01")
interpolate("02")
interpolate("15")
print(f"Finished at {time.time()}")