__all__ = [
            'FaultArgumentException'
          ]


## base class for all exceptions.
#
class Error(Exception):

    ## the constructor of the exception.
    #
    # @param self the object pointer.
    def __init__(self): pass


## class for a specific exception.
#
class SpecificException(Error):

    ## the constructor of the exception.
    #
    # @param self the object pointer.
    # @param value informative exception value.
    def __init__(self, value):
        Error.__init__(self)

        self.value = value

    ## the string representation of the exception.
    #
    # @param self the object pointer.
    def __str__(self):
        return repr(self.value)


## class exception for a fault argument.
#
class FaultArgumentException(SpecificException):

    ## the constructor of the exception.
    #
    # @param self the object pointer.
    # @param value informative exception value.
    def __init__(self, value):
        SpecificException.__init__(self, value)
