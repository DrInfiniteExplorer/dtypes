import ctypes


def offsetof(struct_instance, member_name : str) -> int:
    """
    A manual implementation of offsetof which is consistent?
    It counts and *returns* bits instead of bytes, or False if nothing found.
    """
    mro = struct_instance.__class__.__mro__[:-3]
    fields = []
    for typ in reversed(mro):
        stuff = getattr(typ, '_fields_', None)
        if stuff is None:
            continue
        fields.extend(stuff)

    def align(bits, alignment):
        if bits % alignment == 0:
            return bits
        return bits + (alignment - (bits % alignment))

    bit_sum = 0
    for field_tuple in fields:
        key, _type = field_tuple[0:2]
        bitfield = len(field_tuple) == 3
        bytealigned = bit_sum % 8 == 0
        if not bitfield:
            alignment = ctypes.alignment(_type)
            #alignment = 8

            #print(f"Aligning {bit_sum} to {alignment*8} -> {align(bit_sum, alignment*8)}")
            bit_sum = align(bit_sum, alignment*8)
        
        if key == member_name or (key.startswith("_") and key[1:] == member_name):
            #print(f"{name} at bitsum {bit_sum} ({bit_sum // 8} bytes)")
            return bit_sum
        
        if bitfield:
            bit_sum += field_tuple[2]
        else:
            bit_sum += ctypes.sizeof(_type) * 8
    
    assert False, f"Wanted to know offset of {name} among fields {fields}"


def Enum(name, basetype, enums):
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
        raise RuntimeException(f"No matching enum in {enums} for value {value}")
    
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
