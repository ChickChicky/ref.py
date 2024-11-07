#!/usr/bin/env python3

from ref import Ref

class foo:
    def __init__(self):
        self.bar = 42

x = foo()
y = Ref(x)

print(x.bar)
y.bar = 41
print(x.bar)
