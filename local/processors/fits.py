__author__ = 'civa'

import sys, os, json
from astropy.io import fits
from astropy.utils.data import download_file
import matplotlib.pyplot as plt
from local.processors.base import BaseProcessor

class FITSProcessor(BaseProcessor):
    def __init__(self, **kwargs):
        self.hdulist = None
        super(FITSProcessor, self).__init__(**kwargs)

    def process(self, processing_input):
        input_dict = {}

        try:
            if not processing_input:
                input_dict = self.kwargs
            else:
                if isinstance(processing_input, basestring):
                    input_dict = json.loads(processing_input)
                else:
                    input_dict = processing_input

            self.request_id = input_dict['request_id']
            uri = input_dict['uri']
            method = input_dict['method']
            location = input_dict['output']

            result = {}

            if self._open(URI=uri):
                if method == 'image':
                    filename = self._extract_image(location)
                    result = {'processor' : 'FITSProcessor', 'result': filename}
                elif method == 'table':
                    table_data = {}
                    result = {'processor' : 'FITSProcessor', 'result': table_data}

            return result
        except:
            raise
        finally:
            pass

    def _open(self, URI):
        self.uri = URI

        if 'http' in self.uri:
            return self._download(url=self.uri)
        else:
            return self._open_local(filepath=self.uri)

    def _download(self, url):
        download_file(url, cache=True)
        return True

    def _open_local(self, filepath):
        self.hdulist = fits.open(filepath)
        return True

    def _get_hdu_data(self, method):
        if method == 'image':
            hdu = self.hdulist[0]
            return hdu.data[0,:,:]

    def _create_filename(self, directory, prefix):
        name = prefix + '_' + 'extracted.png'
        return os.path.join(directory, name)

    def _extract_image(self, save_to=''):
        img_data = self._get_hdu_data('image')
        filename = self._create_filename(save_to, self.request_id)

        if img_data.any():
            self.log.info('processing image {0}'.format(filename))
            img = plt.imshow(img_data, origin='lower')
            plt.colorbar(img, orientation="vertical")
            plt.savefig(filename, transparent=True)
            plt.close()
            self.log.info('done')
            return filename