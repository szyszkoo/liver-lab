import numpy as np
from liverDataUtils.cubeInterpolator import CubeInterpolator
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter

sampleNumber = "01"
liverReader = LiverReader()
cubeInterpolator = CubeInterpolator()

# # real shit
# liverData = liverReader.readLiverData(sampleNumber)
# interpolated = cubeInterpolator.interpolateCube(liverData, 1)
# print("eloelo320")
# Plotter(interpolated, interpolated, 100)

# temporary, for tests
x_ = np.linspace(0, 10, 11)
y_ = np.linspace(10, 20, 11)
z_ = np.linspace(10, 40, 11)

_, _, z = np.meshgrid(x_, y_, z_, indexing='ij')

print("Printing the z cube")
print(z[..., 0])
print(z[..., 1])
print(z[..., 2])
print(z[..., 3])

myAwesomeInterpolatedCube = cubeInterpolator.interpolateCube(z)

print("Printing the myAwesomeInterpolatedCube cube")
print(myAwesomeInterpolatedCube[..., 0])
print(myAwesomeInterpolatedCube[..., 1])
print(myAwesomeInterpolatedCube[..., 2])
print(myAwesomeInterpolatedCube[..., 3])
print(myAwesomeInterpolatedCube[..., 4])
print(myAwesomeInterpolatedCube[..., 5])
print(myAwesomeInterpolatedCube[..., 6])
print(myAwesomeInterpolatedCube[..., 7])
print(myAwesomeInterpolatedCube[..., 8])
print(myAwesomeInterpolatedCube[..., 9])
print(myAwesomeInterpolatedCube[..., 10])
print(myAwesomeInterpolatedCube[..., 11])
print(myAwesomeInterpolatedCube[..., 12])
print(myAwesomeInterpolatedCube[..., 13])


assert (myAwesomeInterpolatedCube[..., 0] == z[...,0]).all(), "First slice should remain the same"
assert (myAwesomeInterpolatedCube[..., 11] != np.zeros((myAwesomeInterpolatedCube.shape[0], myAwesomeInterpolatedCube.shape[1]))).all(), "The first slice after the original slices number is just full of zeros"
