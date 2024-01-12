# dtypes

`dtypes` provides decorators to make it easier to work with `ctypes`.

## Installing

`pip install dtypes`

## Using

This example showcases how to use type annotations to declare structs for a HalfEdge data structure.
It uses type annotations and simplified forward declarations.

```py
from dtypes.structify import structify
from dtypes.fwd import fwd, ThisPtr, Pointer

HalfEdge = fwd()
Face = fwd()

@structify
class Vertex(ctypes.structure):
    pos       : ctypes.c_float * 3
    edge      : Pointer(HalfEdge)

@structify
class Face(ctypes.structure, Face):
    edge      : Pointer(HalfEdge)

@structify
class HalfEdge(ctypes.structure, HalfEdge):
    vertex    : Pointer(Vertex)
    face      : Pointer(Face)
    next_edge : ThisPtr
    reverse   : ThisPtr  

```


### Other utilities

#### ReprStructureMembers
Helper mixin that prints contents of fields in repr (no py members tho)
```py
    >>> from .typedefs import uint16_t
    >>> @structify
    ... class PrintyTesty(ctypes.Structure, ReprStructureMembers):
    ...     packed: (uint16_t, 1)
    ...     ctor: (uint16_t, 1)
    ...     overloaded_operators: (uint16_t, 1)
    >>> print(PrintyTesty(True, False, True))
    PrintyTesty{'packed': 1, 'ctor': 0, 'overloaded_operators': 1}
```

There is also `Structy` to inherit from directly that mixes this into `ctypes.structure`

```py 
class Structy(ctypes.Structure, ReprStructureMembers):
```

#### BasicWrapper
Given `Type`, returns a ctypes-structure containing only that type.
This allows us to access the variable in a structure, without losing
 the binding/address of the variable, as it works if you work with
 the plain ctype

```py
    >>> from dtypes.typedef import BasicWrapper, uint32_t
    >>> from dtypes.structify import structify
    >>> @structify
    ... class Example(ctypes.Structure):
    ...    plain   : uint32_t
    ...    wrapped : BasicWrapper(uint32_t)

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
```

#### VoidyPtr
c_void_p is returned as a "int" when accessed inside structs, losing the type 😒

Thus there is `dtypes.voidy.Voidy` which is an empty struct, and `dtypes.voidy.VoidyPtr`
 which is a pointer to that empty struct. It can be used as a better way to preserve 
 the pointer-ness of the type, and like with `BasicWrapper` it preserves the address
 of members when accessed.

#### offsetof
`dtypes.offsetof` returns the number of **bits** of offset from the start of a structure to a member.

#### cmp_ptr
Comparing pointer address values is slightly tricky in ctypes.
Thus there is `dtypes.cmp_ptr` to make it easier.
```py
def cmp_ptr(ptr1, ptr2):
    return ctypes.addressof(ptr1.contents) == ctypes.addressof(ptr2.contents)
```
