class FileNames:
    LIVER_CUBE = "liverCube"
    ROI_CUBE = "roiLiver"
    INTERPOLATED_LIVER_CUBE = "interpolatedCube"
    INTERPOLATED_ROI = "interpolatedROI"
    INTERPOLATED_WHOLE_DATA = "interpolatedWholeData"
    NRRD_FILE_EXTENSION = ".nrrd"

    def getLiverCubeFileName(self, sampleNumber):
        return self.LIVER_CUBE + sampleNumber + self.NRRD_FILE_EXTENSION

    def getRoiCubeFileName(self, sampleNumber):
        return self.ROI_CUBE + sampleNumber + self.NRRD_FILE_EXTENSION

    def getInterpolatedCubeFileName(self, sampleNumber):
        return self.INTERPOLATED_LIVER_CUBE + sampleNumber + self.NRRD_FILE_EXTENSION

    def getInterpolatedRoiFileName(self, sampleNumber):
        return self.INTERPOLATED_ROI + sampleNumber + self.NRRD_FILE_EXTENSION

    def getInterpolatedWholeDataFileName(self, sampleNumber):
        return self.INTERPOLATED_WHOLE_DATA + sampleNumber + self.NRRD_FILE_EXTENSION