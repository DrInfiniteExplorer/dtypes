
import ctypes
from typing import List, Tuple, Union
from .fwd import FWD, Pointer, late_bind, need_fixup

def structify[T: type[ctypes.Structure]](cls: T) -> T:
    """
    A decorator that can turn simpler class definitions into the more line-noisy
     format that ctypes parses.
    Usable with dtypes.fwd for forward declarations

    >>> from .typedefs import uint16_t
    >>> @structify
    ... class BigHeader(ctypes.Structure):
    ...     magic:                   ctypes.c_char
    ...     page_size:               uint16_t
    ...     free_page_map:           uint16_t
    ...     pages_used:              uint16_t
    ...     directory_size_in_bytes: uint16_t
    ...     _reserved:               uint16_t
    >>> print(bytes(BigHeader(b'1',2,3,4,5,6)))
    b'1\\x00\\x02\\x00\\x03\\x00\\x04\\x00\\x05\\x00\\x06\\x00'

    Also supports bitfields
    >>> @structify
    ... class TypeProperty(Structy):
    ...     packed:               (uint16_t, 1)
    ...     ctor:                 (uint16_t, 1)
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

    fields: List[Union[Tuple[str, type], Tuple[str, type, int]]] = []
    for name, typ in cls.__annotations__.items():
        if isinstance(typ, Pointer):
            name, void_type = late_bind(cls, name, typ)
            fields.append((name, void_type))
        elif isinstance(typ, tuple):
            s : Tuple[type, int] = typ # type: ignore
            fields.append((name, s[0], s[1]))
        else:
            fields.append((name, typ))
    cls._fields_ = fields

    return cls


def get_name_adjusted_fields(struct: ctypes.Structure):
    """
    A structified class will have the Pointer members prefixed with `_`
    This function returns a ctypes-like field-list with the original names
     for property/value enumeration that follows those pointers in their
     typed versions.
    """
    fields = list(struct._fields_)
    for idx, field in enumerate(fields):
        name = field[0]
        if name.startswith('_') and hasattr(struct, name[1:]):
            fields[idx] = (name[1:], *field[1:])
    return fields

class ReprStructureMembers:
    """
    Helper mixin that prints contents of fields in repr (no py members tho)

    >>> from .typedefs import uint16_t
    >>> @structify
    ... class PrintyTesty(ctypes.Structure, ReprStructureMembers):
    ...     packed: (uint16_t, 1)
    ...     ctor: (uint16_t, 1)
    ...     overloaded_operators: (uint16_t, 1)
    >>> print(PrintyTesty(True, False, True))
    PrintyTesty{'packed': 1, 'ctor': 0, 'overloaded_operators': 1}
    """
    def __repr__(self):
        assert isinstance(self, ctypes.Structure)
        names = [f[0] for f in get_name_adjusted_fields(self)]
        names += list(self.__dict__.keys())
        return type(self).__name__ + str({name : getattr(self, name) for name in names})

class Structy(ctypes.Structure, ReprStructureMembers):
    """
    Helper baseclass using the ReprStructureMembers mixin

        >>> from .typedefs import uint16_t
    >>> @structify
    ... class PrintyTesty(Structy):
    ...     packed: (uint16_t, 1)
    ...     ctor: (uint16_t, 1)
    ...     overloaded_operators: (uint16_t, 1)
    >>> print(PrintyTesty(True, False, True))
    PrintyTesty{'packed': 1, 'ctor': 0, 'overloaded_operators': 1}
    """
    ...