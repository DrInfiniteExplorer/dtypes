# dtypes

Yo yo what's this?

Well it's ✨`dtypes`✨ which is extra stuff to make `ctypes` usable.

Who wants to do

```py
class Yolo(ctypes.structure):
    _fields_ = [
        ("a", ctypes.c_int),
        ("b", ctypes.c_float),
        ("c", ctypes.c_double),
    ]
```

when you can do

```py
from dtypes.structify import structify
@structify
class Yolo(ctypes.structure):
    a : ctypes.c_int
    b : ctypes.c_float
    c : ctypes.c_double
```

And then, who wants to deal with the messy and incomplete way of working with forward declarations in pure ctypes?

```py
class Yeet(ctypes.structure):
    pass

class Chonko(ctypes.structure):
    _fields_ = [
        ("yeet", ctypes.POINTER(Yeet)),
    ]

Yeet._fields_ =[
    ("chonker", Chonko),
    ("this", ctypes.POINTER(Yeet),
]
```

when you can do

```py

from dtypes.structify import structify
from dtypes.fwd import fwd, ThisPtr, Pointer

Yeet = fwd()

@structify
class Chonko(ctypes.structure):
    yeet : Pointer(Yeet)

@structify
class Yeet(ctypes.structure):
    chonker : Chonko
    this    : ThisPtr
]
```
