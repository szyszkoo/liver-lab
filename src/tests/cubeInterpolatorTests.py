import numpy as np
from src.liverDataUtils.cubeInterpolator import CubeInterpolator

# given
cubeInterpolator = CubeInterpolator()
x_ = np.linspace(0, 10, 11)
y_ = np.linspace(10, 20, 11)
z_ = np.linspace(10, 40, 11)

_, _, z = np.meshgrid(x_, y_, z_, indexing='ij')

# when
myAwesomeInterpolatedCube = cubeInterpolator.interpolateCube(z)

# then
assert (myAwesomeInterpolatedCube[..., 0] == z[...,0]).all(), "First slice should remain the same"
assert (myAwesomeInterpolatedCube[..., 11] != np.zeros((myAwesomeInterpolatedCube.shape[0], myAwesomeInterpolatedCube.shape[1]))).all(), "The first slice after the original slices number is just full of zeros"
assert (myAwesomeInterpolatedCube[..., -1] == z[..., -1]).all(), "The first slice after the original slices number is just full of zeros"
