import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

def n4BiasFieldCorrection3D(dataCube, maximumNumberOfIterations = 50):
    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    # corrector.SetMaximumNumberOfIterations(50)
    # dataCube = np.array(dataCube)
    # dataCube = dataCube.astype(float)
    # output = sitk.GetImageFromArray

    if(dataCube.ndim > 2):
        output = np.zeros(dataCube.shape)
        
        for index in np.arange(0, dataCube.shape[2], 1):
            print(f"{index}/{dataCube.shape[2]}")
            singleSlice = sitk.GetImageFromArray(dataCube[:,:,index])
            output[:,:,index] = sitk.GetArrayFromImage(corrector.Execute(singleSlice))

        return output
    else: 
        singleSlice = sitk.GetImageFromArray(dataCube)
        return sitk.GetArrayFromImage(corrector.Execute(singleSlice))
