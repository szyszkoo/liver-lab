import numpy as np

class CubeInterpolator:
    def interpolateCube(self, dataCube, numSlices = 2):
        """Adds additional layers between each existing z-position layer in the dataCube

        Attributes:
            numSlices     Number of slices to add between each slice of data in dataCube. Default value is 2.
            dataCube    Data to which the additional slices will be added.
        """

        fullIterationNumber = numSlices + 1
        originalShape = dataCube.shape
        interpolatedSlicesNumber = originalShape[2] * 3 - 2
        interpolatedDataCube = np.zeros((originalShape[0], originalShape[1], interpolatedSlicesNumber))

        for i in range(originalShape[0]):
            for j in range(originalShape[1]):
                for k in range(interpolatedSlicesNumber):
                    if (k % fullIterationNumber == 0):
                        interpolatedDataCube[i, j, k] = dataCube[i, j, int(k/fullIterationNumber)]
                        continue

                    initialValue = dataCube[i, j, int(np.floor(k/fullIterationNumber))]
                    endValue = dataCube[i, j, int(np.ceil(k/fullIterationNumber))]

                    interpolatedDataCube[i, j, k] = np.linspace(initialValue, endValue, numSlices + 2)[k % fullIterationNumber]

        return interpolatedDataCube