from typing import Any, Literal

_PathSegType = Literal['index', 'prop']
_PathSeg = tuple[_PathSegType, Any]
_Path = list[_PathSeg]

class Ref:
    
    val: Any
    pth: _Path
    
    def __init__( self, val: Any, path: _Path = None ):
        object.__setattr__(self, 'val', val)
        object.__setattr__(self, 'pth', path or [])
        
    def __getattribute__(self, name: str) -> 'Ref':
        return Ref(_val(self), _pth(self)+[('prop',name)])
    
    def __getattr__(self, name: str) -> 'Ref':
        return Ref(_val(self), _pth(self)+[('prop',name)])
    
    def __set__(self, name: str, value: Any):
        return Ref(_val(self), _pth(self)+[('prop',name)]) >> value
    
    def __setattr__(self, name: str, value: Any):
        return Ref(_val(self), _pth(self)+[('prop',name)]) >> value
    
    def __getitem__(self, index: Any):
        return Ref(_val(self), _pth(self)+[('index',index)])
    
    def __setitem__(self, index: Any, value: Any):
        return Ref(_val(self), _pth(self)+[('index',index)]) >> value
    
    def __rshift__(self, other: Any):
        val = _val(self)
        pth = _pth(self)
        if not len(pth):
            raise IndexError('Empty ref access')
        _assign(_resolve(val, pth[:-1]), pth[-1], other)
        
    def __invert__(self):
        return _resolve(_val(self), _pth(self))

def _assign(tgt: Any, seg: _PathSeg, val: Any):
    t, k = seg
    if t == 'index':
        tgt[k] = val
    elif t == 'prop':
        setattr(tgt, k, val)
    else:
        raise TypeError('Invalid assign kind "%s"'%(t,))

def _resolve(val: Any, path: _Path) -> Any:
    for t, k in path:
        if t == 'index':
            val = val[k]
        elif t == 'prop':
            val = getattr(val, k)
        else:
            raise TypeError('Invalid access kind "%s"'%(t,))
    return val

def _val( r: Ref ) -> Any:
    return object.__getattribute__(r, 'val')
    
def _pth( r: Ref ) -> _Path:
    return object.__getattribute__(r, 'pth')
