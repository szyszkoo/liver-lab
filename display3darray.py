import pylab
import nrrd
import numpy as np

class plotter:
    def __init__(self, im, i=0):
        self.im = im
        self.i = i
        self.vmin = im.min()
        self.vmax = im.max()
        self.fig = pylab.figure()
        pylab.gray()
        self.ax = self.fig.add_subplot(111)
        self.fig.canvas.mpl_connect('key_press_event', self.test)
        self.draw()

    def draw(self):
        if self.im.ndim is 2:
            im = self.im
        if self.im.ndim is 3:
            im = self.im[...,self.i]
            self.ax.set_title('image {0}'.format(self.i))

        if len(self.ax.images) > 0:
            self.ax.images.pop()
        self.ax.imshow(im, vmin=self.vmin, vmax=self.vmax, interpolation=None)
        pylab.show()

    def test(self, event):
        old_i = self.i
        if event.key=='right':
            self.i = min(self.im.shape[2]-1, self.i+1)
        elif event.key == 'left':
            self.i = max(0, self.i-1)
        if old_i != self.i:
            self.draw()
            self.fig.canvas.draw()

def slice_show(im, i=0):
    plotter(im, i)

liverData, liverHeader = nrrd.read("./myTestLiverCube.nrrd")
roiData, roiHeader =  nrrd.read("./myROI_LIVER.nrrd")

plotter(np.multiply(liverData,roiData), 50)