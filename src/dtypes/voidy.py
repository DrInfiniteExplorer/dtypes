
"""
c_void_p is returned as a "int" when accessed inside structs, losing the type 😒

Thus the empty struct `Voidy`, and `VoidyPtr` which can be used instead of `c_void_p`.

"""


import ctypes

class Voidy(ctypes.Structure):
    pass

VoidyPtr = ctypes.POINTER(Voidy)

