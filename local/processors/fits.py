__author__ = 'civa'

from astropy.io import fits
import matplotlib.pyplot as plt

class FITSProcessor():

    hdulist = None

    def open(self, filename):
        self.hdulist = fits.open(filename)
        return True

    def get_image(self):
        hdu = self.hdulist[0]
        img_data = hdu.data[0,:,:]

        plt.imshow(img_data, origin='lower')
        #plt.imshow(img_data)
        plt.imsave('test.png', img_data)