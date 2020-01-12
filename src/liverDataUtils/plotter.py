import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self, imageCube1, imageCube2, i=0):
        self.imageCube1 = imageCube1
        self.imageCube2 = imageCube2
        self.i = i
        self.fig = plt.figure()
        # plt.gray()
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.fig.canvas.mpl_connect('key_release_event', self)
        self.draw()

    def draw(self):
        if self.imageCube1.ndim is 2:
            image1 = self.imageCube1
            image2 = self.imageCube2
        if self.imageCube1.ndim is 3:
            image1 = self.imageCube1[...,self.i]
            image2 = self.imageCube2[...,self.i]
            self.ax1.set_title('slice {0}'.format(self.i))
            self.ax2.set_title('slice {0}'.format(self.i))

        if len(self.ax1.images) > 0:
            self.ax1.images.pop()
            
        if len(self.ax2.images) > 0:
            self.ax2.images.pop()

        self.ax1.imshow(np.fliplr(np.rot90(image1, k=3)))  
        self.ax2.imshow(np.fliplr(np.rot90(image2, k=3)))  
        # TODO: fix the maximum recursion depth exceeded in comparison issue
        plt.pause(0.1) 
        plt.show()

    def __call__(self, event):
        old_i = self.i
        if event.key=='right':
            self.i = min(self.imageCube1.shape[2]-1, self.imageCube2.shape[2]-1, self.i+1)
        elif event.key == 'left':
            self.i = max(0, self.i-1)
        if old_i != self.i:
            self.draw()