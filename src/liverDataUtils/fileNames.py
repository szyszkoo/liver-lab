class FileNames:
    LIVER_CUBE = "liverCube"
    ROI_CUBE = "roiLiver"
    INTERPOLATED_LIVER_CUBE = "interpolatedCube"
    NRRD_FILE_EXTENSION = ".nrrd"

    def getLiverCubeFileName(self, sampleNumber):
        return self.LIVER_CUBE + sampleNumber + self.NRRD_FILE_EXTENSION

    def getRoiCubeFileName(self, sampleNumber):
        return self.ROI_CUBE + sampleNumber + self.NRRD_FILE_EXTENSION

    def getInterpolatedCubeFileName(self, sampleNumber):
        return self.INTERPOLATED_LIVER_CUBE + sampleNumber + self.NRRD_FILE_EXTENSION