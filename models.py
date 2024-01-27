import numpy as np


class BinaryMessage(np.ndarray):
    """Represents a binary message. 
    Inherits from np.ndarray and enforces that the array contains only 0s and 1s.

    Parameters:
        input_array (array-like): The input array to be converted into a BinaryMessage
            object. Creation fails if input array contains values other than 0 and 1.
    """

    def __new__(cls, input_array):
        """Creates a new BinaryMessage object from the given array. Checks that the array
        contains only 0s and 1s."""
        obj = np.asarray(input_array).astype(int).view(cls)
        if not np.all(np.isin(obj, [0, 1])):
            raise ValueError("Array must contain only 0s and 1s")
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
