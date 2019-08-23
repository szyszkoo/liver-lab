import numpy as np
from scipy.interpolate import RegularGridInterpolator


# config 
numberOfSlicesToAdd = 2

# init
elCuberinhoOriginale = np.zeros((3,3,3))
elCuberinhoOriginale[...,0] = np.ones((3,3))
elCuberinhoOriginale[...,1] = np.ones((3,3)) * 4
elCuberinhoOriginale[...,2] = np.ones((3,3)) * 7

elCuberinho = np.zeros((3,3,7))

fullIterationNumber = numberOfSlicesToAdd + 1

for i in range(elCuberinho.shape[0]):
    for j in range(elCuberinho.shape[1]):
        for k in range(elCuberinho.shape[2]):
            if(k % fullIterationNumber == 0):
                elCuberinho[i,j,k] = elCuberinhoOriginale[i, j, int(k/fullIterationNumber)]
                continue

            firstSlice = elCuberinhoOriginale[..., int(np.floor(k/fullIterationNumber))]
            secondSlice = elCuberinhoOriginale[..., int(np.ceil(k/fullIterationNumber))]

            elCuberinho[i,j,k] = np.linspace(firstSlice[i,j], secondSlice[i,j], numberOfSlicesToAdd + 2)[k % fullIterationNumber]

print("elo")