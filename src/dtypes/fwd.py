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
from typing import Any, List

from dtypes.voidy import VoidyPtr


class Pointer:
    def __init__(self, typ: type):
        self.typ = typ

class __SelfPtrSentineType:
    ...
ThisPtr = Pointer(__SelfPtrSentineType)

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


need_fixup: List[Pointer]= []

def late_bind(cls: type, member_name: str, member_ptr_type: Pointer):
    """
    If the name/type -pair is a `Pointer`, turn it into a
     void* prefixed with `_` and supply casting properties
     with the original name.

    This allows us to refer to our own class (using
     the ThisType marker), to use a manually premade Pointer
     instance that is populated later, or to use with `fwd`
     to allow automagic later binding.

    `member_ptr_type` is used as an indirector. When we access
      the type through the generated properties, the void*
      is cast to the late-ly assigned actual type.
    """
    original_member_name = member_name
    member_name = '_' + member_name
    if member_ptr_type is ThisPtr:
        member_ptr_type = Pointer(cls)
    else:
        Typ = member_ptr_type.typ
        if issubclass(Typ, FWD):
            need_fixup.append(member_ptr_type)

    def getty_cast(self: ctypes.Structure):
        voidy_ptr = getattr(self, member_name)
        return ctypes.cast(voidy_ptr, ctypes.POINTER(member_ptr_type.typ))
    def setty_cast(self: ctypes.Structure, val: Any): # Can't lock down type of val, since we don't know it ¯\_(ツ)_/¯
        assert isinstance(val, ctypes.POINTER(member_ptr_type.typ))
        setattr(self, member_name, ctypes.cast(val, VoidyPtr))
    proppy = property(fget = getty_cast, fset = setty_cast)
    setattr(cls, original_member_name, proppy)

    # The final field type should be the name, and a generic void*
    return member_name, VoidyPtr


