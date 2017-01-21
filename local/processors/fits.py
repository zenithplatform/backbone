__author__ = 'civa'

import json
from astropy.io import fits
from astropy.utils.data import download_file
import matplotlib.pyplot as plt
from local.processors.base import BaseProcessor

class FITSProcessor(BaseProcessor):
    def __init__(self, **kwargs):
        self.hdulist = None
        super(FITSProcessor, self).__init__(**kwargs)

    def open(self, URI):
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

    def process(self, json_input=''):
        input_dict = {}

        if json_input:
            input_dict = json.loads(json_input)
        else:
            input_dict = self.kwargs

        uri = input_dict['uri']
        req_id = input_dict['req_id']
        method = input_dict['method']
        output = input_dict['output']

        result = {}

        result_template = {
            'result': result,
            'req_id': req_id
        }

        if self.open(URI=uri):
            if method == "Image":
                self.get_image(output)
                result = {'processor' : 'FITSProcessor', 'img_path': output}
                result_template['result'] = result

        return result_template

    def get_image(self, save_to=''):
        hdu = self.hdulist[0]
        img_data = hdu.data[0,:,:]

        img = plt.imshow(img_data, origin='lower')
        plt.colorbar(img, orientation="vertical")

        if not save_to:
            save_to = 'temp.png'

        plt.savefig(save_to, transparent=True)