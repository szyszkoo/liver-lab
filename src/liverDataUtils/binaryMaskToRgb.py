import numpy as np

class BinaryMaskToRgb: 
    def convert(self, dataCube, shouldConvertToRed: bool):
        dataCube = np.array(dataCube)
        if(dataCube.ndim != 3):
            print("Array should have 3 dimensions")
            return
        if(shouldConvertToRed == True):
            mapper = lambda value: [value*255, 0, 0]
        else: 
            maxVal = np.max(dataCube)
            mapper = lambda value: [value/maxVal, value/maxVal, value/maxVal]

        mapped = np.zeros((380, 309, 240,3))
        for (i,j,k), value in np.ndenumerate(dataCube):
            mapped[i,j,k] = list(mapper(value))
        # print(mapped)

        return mapped
