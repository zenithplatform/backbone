__author__ = 'civa'

class ProviderException(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(ProviderException, self).__init__(message)
        self.errors = errors
