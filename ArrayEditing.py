
import numpy as np


def remDubFromArray(array):
    if array is not None:
        ass=set(array)
        ar=[]
        [ar.append(i) for i in ass]
        return ar


