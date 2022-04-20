
import ctypes
from .fwd import FWD, Pointer, late_bind, need_fixup

def structify(cls):
    """
    A decorator that can turn simpler class definitions into the more line-noisy
     format that ctypes parses.
    Usable with dtypes.fwd for forward declarations

    >>> from .typedefs import uint16_t
    >>> @structify
    ... class BigHeader(ctypes.Structure):
    ...     magic: ctypes.c_char
    ...     page_size: uint16_t
    ...     free_page_map: uint16_t
    ...     pages_used: uint16_t
    ...     directory_size_in_bytes: uint16_t
    ...     _reserved: uint16_t
    >>> print(bytes(BigHeader(b'1',2,3,4,5,6)))
    b'1\\x00\\x02\\x00\\x03\\x00\\x04\\x00\\x05\\x00\\x06\\x00'

    Also supports bitfields
    >>> @structify
    ... class TypeProperty(Structy):
    ...     packed: (uint16_t, 1)
    ...     ctor: (uint16_t, 1)
    ...     overloaded_operators: (uint16_t, 1)
    >>> print(bytes(TypeProperty(True, False, True)))
    b'\\x05\\x00'

    """
    if issubclass(cls, FWD):
        for fixy in need_fixup:
            if issubclass(cls, fixy.typ):
                fixy.typ = cls
                need_fixup.remove(fixy)
                break

    fields = []
    for data in cls.__annotations__.items():
        name = data[0]
        rest = data[1]        
        if isinstance(rest, Pointer):
            name, rest = late_bind(cls, name, rest)
        rest = rest if isinstance(rest, tuple) else (rest,)
        fields.append((name, *rest))
    cls._fields_ = fields

    return cls


def get_name_adjusted_fields(struct):
    fields = list(struct._fields_)
    for idx, field in enumerate(fields):
        name = field[0]
        if name.startswith('_') and hasattr(struct, name[1:]):
            fields[idx] = (name[1:], *field[1:])
    return fields

class Structy(ctypes.Structure):
    """
    Helper baseclass that prints contents of fields in repr (no py members tho)

    >>> from .typedefs import uint16_t
    >>> @structify
    ... class PrintyTesty(Structy):
    ...     packed: (uint16_t, 1)
    ...     ctor: (uint16_t, 1)
    ...     overloaded_operators: (uint16_t, 1)
    >>> print(PrintyTesty(True, False, True))
    PrintyTesty{'packed': 1, 'ctor': 0, 'overloaded_operators': 1}
    """
    def __repr__(self):
        names = [f[0] for f in get_name_adjusted_fields(self)]
        names += list(self.__dict__.keys())
        return type(self).__name__ + str({name : getattr(self, name) for name in names})
