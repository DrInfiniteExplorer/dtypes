import ctypes
from typing import List, Tuple, Union


def offsetof(struct_instance: ctypes.Structure, member_name : str) -> int:
    """
    A manual implementation of offsetof which is consistent?
    It counts and *returns* bits instead of bytes, or False if nothing found.
    """
    mro = struct_instance.__class__.__mro__[:-3]
    fields: List[Union[Tuple[str, type], Tuple[str, type, int]]] = []
    for typ in reversed(mro):
        stuff = getattr(typ, '_fields_', None)
        if stuff is None:
            continue
        fields.extend(stuff)

    def align(bits: int, alignment: int) -> int:
        if bits % alignment == 0:
            return bits
        return bits + (alignment - (bits % alignment))

    bit_sum: int = 0
    key: str
    for field_tuple in fields:
        key, _type = field_tuple[0:2]
        bitfield = len(field_tuple) == 3

        if not bitfield:
            alignment = ctypes.alignment(_type)
            bit_sum = align(bit_sum, alignment*8)
        
        if key == member_name or (key.startswith("_") and key[1:] == member_name):
            #print(f"{name} at bitsum {bit_sum} ({bit_sum // 8} bytes)")
            return bit_sum
        
        if bitfield:
            bit_sum += field_tuple[2]
        else:
            bit_sum += ctypes.sizeof(_type) * 8
    
    assert False, f"Wanted to know offset of {member_name} among fields {fields}"


def Enum(name: str, basetype: type, enums: List[Union[str, Tuple[str, int]]]) -> type:
    """
    Shitty hacky enum for displaying enum-values from ctypes.
    Use like
    > MyEnum = Enum("MyEnum", ctypes.c_int, [ ("UseConfigDefault", 0), ("AlwaysUpdate", 1) ])
    """
    def __str__(self):
        value = self.value
        prev_value = -1
        for entry in enums:
            name, value = entry, prev_value + 1
            if isinstance(entry, tuple):
                name, value = entry
            if value == value:
                return name
            prev_value = value
        raise RuntimeError(f"No matching enum in {enums} for value {value}")
    
    E = type(name, (basetype,), dict(__str__ = __str__, __repr__ = __str__))
    return E

def cmp_ptr(ptr1, ptr2):
    """
    Sometimes you just want to compare addresses
    """
    return ctypes.addressof(ptr1.contents) == ctypes.addressof(ptr2.contents)

class BitfieldFlags(ctypes.Structure):
    """
    Inherit from this and declare as normal bitfield structs. Will print as "A | C" if set.
    """
    def __repr__(self):
        set_flags = [x[0] for x in self._fields_ if getattr(self, x[0]) == 1]
        return " | ".join(set_flags)
