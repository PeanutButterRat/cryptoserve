import numpy as np
from numpy import integer, uint16, uint32

np.seterr(over="ignore")


def to_bytes(x: integer, byteorder="big") -> bytes:
    dtype = np.dtype(type(x))
    size_bytes = dtype.itemsize
    return int(x).to_bytes(size_bytes, byteorder)


def from_bytes(b: bytes, dtype: integer = uint16, byteorder="big") -> integer:
    value = int.from_bytes(b, byteorder)
    return dtype(value)
