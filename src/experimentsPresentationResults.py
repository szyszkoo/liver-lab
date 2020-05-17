import numpy as np
import nrrd
from liverDataUtils.liverReader import LiverReader
from liverDataUtils.plotter import Plotter
import time 
from liverDataUtils.regionGrowing import RegionGrowing
from liverDataUtils.filters import medianFilter
from liverDataUtils.n4BiasFieldCorretion import n4BiasFieldCorrection3D
from liverDataUtils.imageSegmentation import otsuThreshold, regionGrowingWithUnsharpMasking, regionGrowing, gaborFilter, unsharpMasking
from skimage.filters import gabor
from liverDataUtils.gaborFeatureVector import createGaborFeatureVector

# init
liverReader = LiverReader()
start_time = time.time()

# read liver data
liverPath = "results/base_interpolated_linear/interpolatedCube03.nrrd"

liver = liverReader.readNrrdData(liverPath).astype(float)

unsharpened = unsharpMasking(liver, 5)
Plotter(liver, unsharpened, 150)
Plotter(liver, liver-unsharpened, 150)

n4 = n4BiasFieldCorrection3D(liver[...,150])
Plotter(liver[...,150], n4 )
Plotter(liver[...,150], liver[...,150] - n4 )
# nrrd.write("results/presentation/liver03_unsharpMasking.nrrd", liver)