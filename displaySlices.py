import matplotlib.pyplot as plt
import nrrd
import numpy as np

class plotter:
    def __init__(self, im, i=0):
        self.im = im
        self.i = i
        self.vmin = im.min()
        self.vmax = im.max()
        self.fig = plt.figure()
        plt.gray()
        self.ax = self.fig.add_subplot(111)
        self.fig.canvas.mpl_connect('key_release_event', self)
        self.draw()

    def draw(self):
        if self.im.ndim is 2:
            im = self.im
        if self.im.ndim is 3:
            im = self.im[...,self.i]
            self.ax.set_title('image {0}'.format(self.i))

        if len(self.ax.images) > 0:
            self.ax.images.pop()
        self.ax.imshow(np.flip(np.rot90(im,k=3)))  
        # TODO: fix the maximum recursion depth exceeded in comparison issue
        plt.pause(0.1) 
        plt.show()

    def __call__(self, event):
        old_i = self.i
        if event.key=='right':
            self.i = min(self.im.shape[2]-1, self.i+1)
        elif event.key == 'left':
            self.i = max(0, self.i-1)
        if old_i != self.i:
            self.draw()

def slice_show(im, i=0):
    plotter(im, i)

# liverData, liverHeader = nrrd.read("./myTestLiverCube2.nrrd")
# roiData, roiHeader =  nrrd.read("./myROI_LIVER2.nrrd")

# plotter(np.multiply(liverData,roiData), 63)
# plotter(roiData, 50)
# plotter(liverData, 50)