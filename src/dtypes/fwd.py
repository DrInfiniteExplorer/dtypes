"""
Yeety

>>> from dtypes.structify import structify
>>> from dtypes.fwd import fwd, ThisPtr
>>> Dsa = fwd() # Forward declare
>>> @structify
... class Asd(ctypes.Structure):
...     asd : ThisPtr            # Pointer to own type
...     dsa : Pointer(Dsa)       # Pointer to forward-declared Dsa
>>>
>>> @structify
... class Dsa(ctypes.Structure, Dsa): # Dsa inherits&replaces the forward declaration
...     next : ThisPtr             # Pointer to own type
...     asd  : ctypes.POINTER(Asd) # Regular pointer to Asd
>>>
>>> asd = Asd()
>>> asd.a = 5
>>> print(asd.a)
5

>>> print(asd)
<dtypes.fwd.Asd object at 0x...>

>>> print(asd.asd)
<dtypes.fwd.LP_Asd object at 0x...>

>>> print(bytes(asd.asd))      # null-pointer of own type
b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'



At the same time you can access the raw underlying pointer
>>> print(asd._asd)
<dtypes.voidy.LP_Voidy object at 0x...>

>>> asd.asd = ctypes.pointer(asd)  # <spiderman pointing at self meme>

>>> ctypes.addressof(asd.asd.contents) == ctypes.addressof(asd)
True

>>> asd.dsa = ctypes.pointer(Dsa())
>>> asd.dsa.contents.asd = ctypes.pointer(asd)
>>> print(ctypes.addressof(asd.dsa.contents.asd.contents) == ctypes.addressof(asd))
True

"""

import ctypes

from dtypes.voidy import VoidyPtr

class Pointer:
    def __init__(self, typ = None):
        self.typ = typ

ThisPtr = Pointer(None)

class FWD:
    """
    This class is a "common ancestor" to recognize that a type
     should be fixed "later".     
    """
    ...

def fwd():
    """
    Return a type to use as a forward-declaration for pointers.
    A struct needs to inherit from it later though.
    """
    class _FWD(FWD):
        ...
    return _FWD


need_fixup = []

def late_bind(cls, name, rest):
    """
    If the name/type -pair is a `Pointer`, turn it into a voidy
     pointer prefixed with `_` and supply casting properties
     with the original name.
    The casting properties can do 'late' type-binding in the
     properties.
    This allows us to refer to our own class (using
     the ThisType marker), to use a manually premade Pointer
     instance that is populated later, or to use with `fwd`
     to allow automagic later binding.
    """
    oname = name
    orest = rest
    name = '_' + name
    if rest is ThisPtr:
        orest = Pointer(cls)
    else:
        Typ = rest.typ
        if issubclass(Typ, FWD):
            need_fixup.append(orest)
    rest = VoidyPtr
    def getty_cast(self):
        voidy_ptr = getattr(self, name)
        return ctypes.cast(voidy_ptr, ctypes.POINTER(orest.typ))
    def setty_cast(self, val):
        assert isinstance(val, ctypes.POINTER(orest.typ))
        setattr(self, name, ctypes.cast(val, VoidyPtr))
    proppy = property(fget = getty_cast, fset = setty_cast)
    setattr(cls, oname, proppy)
    #print(getattr(cls, oname))
    return name, rest


