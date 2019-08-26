import numpy as np
from liverDataUtils.cubeInterpolator import CubeInterpolator

# given
cubeInterpolator = CubeInterpolator()
x_ = np.linspace(0, 10, 11)
y_ = np.linspace(10, 20, 11)
z_ = np.linspace(10, 40, 11)

_, _, z = np.meshgrid(x_, y_, z_, indexing='ij')

# when
interpolatedCube = cubeInterpolator.interpolateCube(z)

# then
assert (interpolatedCube[..., 0] == z[...,0]).all(), "First slice should remain the same"
assert (interpolatedCube[..., 11] != np.zeros((interpolatedCube.shape[0], interpolatedCube.shape[1]))).all(), "The first slice after the original slices number is just full of zeros"
assert (interpolatedCube[..., -1] == z[..., -1]).all(), "The last slice is not the same as the original last one"
