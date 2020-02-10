import numpy as np

class RegionGrowing:
    
    def grow(self, img, seed, t):
        """
        img: ndarray, ndim=3
            An image volume.
        
        seed: tuple, len=3
            Region growing starts from this point.

        t: int
            The image neighborhood radius for the inclusion criteria.
        """
        output = np.zeros(img.shape, dtype=np.bool)
        checked = np.zeros_like(output)

        output[seed] = True
        checked[seed] = True
        needs_check = self.getNeighbourhood(seed, checked, img.shape)

        while len(needs_check) > 0:
            currentPoint = needs_check.pop()

            # Its possible that the point was already checked and was
            # put in the needs_check stack multiple times.
            if checked[currentPoint]: 
                continue

            checked[currentPoint] = True

            # Handle borders.
            imin = max(currentPoint[0]-t, 0)
            imax = min(currentPoint[0]+t, img.shape[0]-1)
            jmin = max(currentPoint[1]-t, 0)
            jmax = min(currentPoint[1]+t, img.shape[1]-1)
            kmin = max(currentPoint[2]-t, 0)
            kmax = min(currentPoint[2]+t, img.shape[2]-1)

            # print("==============================================")
            # print("Aktualny punkt: ", currentPoint)
            # print("i min: ", imin)
            # print("i max: ", imax)
            # print("j min: ", jmin)
            # print("j max: ", jmax)
            # print("k min: ", kmin)
            # print("k max: ", kmax)


            # print("Wartosc aktualnego piksela: ", img[currentPoint])
            # print("Wartosc srednia sasiedztwa: ", img[imin:imax+1, jmin:jmax+1, kmin:kmax+1].mean())
            # print("==============================================")

            if img[currentPoint] <= (img[imin:imax+1, jmin:jmax+1, kmin:kmax+1].mean()*0.75):
            # if img[currentPoint] == 255:
                # Include the voxel in the segmentation and
                # add its neighbors to be checked.
                output[currentPoint] = True
                # print("Punkt zakwalifikowany!")
                # print("==============================================")

                needs_check += self.getNeighbourhood(currentPoint, checked, img.shape)

        return output

    def getNeighbourhood(self, currentPoint, checked, dims):
        nbhd = []

        if (currentPoint[0] > 0) and not checked[currentPoint[0]-1, currentPoint[1], currentPoint[2]]:
            nbhd.append((currentPoint[0]-1, currentPoint[1], currentPoint[2]))
        if (currentPoint[1] > 0) and not checked[currentPoint[0], currentPoint[1]-1, currentPoint[2]]:
            nbhd.append((currentPoint[0], currentPoint[1]-1, currentPoint[2]))
        if (currentPoint[2] > 0) and not checked[currentPoint[0], currentPoint[1], currentPoint[2]-1]:
            nbhd.append((currentPoint[0], currentPoint[1], currentPoint[2]-1))

        if (currentPoint[0] < dims[0]-1) and not checked[currentPoint[0]+1, currentPoint[1], currentPoint[2]]:
            nbhd.append((currentPoint[0]+1, currentPoint[1], currentPoint[2]))
        if (currentPoint[1] < dims[1]-1) and not checked[currentPoint[0], currentPoint[1]+1, currentPoint[2]]:
            nbhd.append((currentPoint[0], currentPoint[1]+1, currentPoint[2]))
        if (currentPoint[2] < dims[2]-1) and not checked[currentPoint[0], currentPoint[1], currentPoint[2]+1]:
            nbhd.append((currentPoint[0], currentPoint[1], currentPoint[2]+1))

        return nbhd