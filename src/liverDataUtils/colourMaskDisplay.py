from liverDataUtils.binaryMaskToRgb import convertBinaryToRgb
from liverDataUtils.plotter import Plotter

def displayColouredMask(mask, liver, startSlice):
    colouredMask = convertBinaryToRgb(mask, True)
    print("Mask coloured.")
    liver4D = convertBinaryToRgb(liver, False)

    Plotter(colouredMask + liver4D, liver, startSlice)

    return colouredMask + liver4D