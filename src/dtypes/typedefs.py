import ctypes

class BasicWrapperBase(ctypes.Structure):
    pass

def BasicWrapper(Type, name):
    """
    Given `Type`, returns a ctypes-structure containing only that type.
    This allows us to access the variable in a structure, without losing
     the binding/address of the variable, as it works if you work with
     the plain ctype

    >>> from dtypes.structify import structify
    >>> @structify
    ... class Example(ctypes.Structure):
    ...    plain   : uint32_t
    ...    wrapped : uint32_tw

    >>> example = Example()
    >>> type(example.plain)
    <class 'int'>
    >>> type(example.wrapped)
    <class 'dtypes.typedefs.uint32_tw'>

    >>> ctypes.addressof(example.plain)
    Traceback (most recent call last):
        ...
    TypeError: invalid type

    >>> ctypes.addressof(example.wrapped) - ctypes.addressof(example)
    4
    
    """
    return type(name, (BasicWrapperBase,), dict(
            __str__ = lambda self: str(self.value),
            _fields_ = (("value", Type),)
        )
    )

# These are for allowing "getting" from a struct without py-typifying and losing address of the thing.
# suffix "w" is for "wrapper"
int8_tw = BasicWrapper (ctypes.c_int8,  "int8_tw")
int16_tw = BasicWrapper(ctypes.c_int16, "int16_tw")
int32_tw = BasicWrapper(ctypes.c_int32, "int32_tw")
int64_tw = BasicWrapper(ctypes.c_int64, "int64_tw")
uint8_tw = BasicWrapper (ctypes.c_uint8,  "uint8_tw")
uint16_tw = BasicWrapper(ctypes.c_uint16, "uint16_tw")
uint32_tw = BasicWrapper(ctypes.c_uint32, "uint32_tw")
uint64_tw = BasicWrapper(ctypes.c_uint64, "uint64_tw")

int8_t = ctypes.c_int8
int16_t = ctypes.c_int16
int32_t = ctypes.c_int32
int64_t = ctypes.c_int64
uint8_t = ctypes.c_uint8
uint16_t = ctypes.c_uint16
uint32_t = ctypes.c_uint32
uint64_t = ctypes.c_uint64

float32_t = ctypes.c_float
float64_t = ctypes.c_double

