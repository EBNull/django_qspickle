import django.db.models
from django.db.models.query import QuerySet
from django.db.models.loading import get_model
from pickle import Pickler, Unpickler, dumps, loads, UnpicklingError

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

__all__ = ('pickle_qs', 'unpickle_qs')


class _DjangoQueryPickler(Pickler):
    def persistent_id(self, obj):
        try:
            if issubclass(obj, django.db.models.Model):
                return "model/%s/%s"%(obj._meta.app_label, obj.__name__)
        except Exception as e:
            pass
        return None

class _DjangoQueryUnpickler(Unpickler):
    white_modules = [
        'django.utils.datastructures',
        'django.db.models'
    ]
    white_objects = [
        '__builtin__.object',
        '__builtin__.dict',
        '__builtin__.list',
        '__builtin__.tuple',
        '__builtin__.set',
        '__builtin__.frozenset',
        'copyreg._reconstructor',
        'copy_reg._reconstructor'
    ]

    def persistent_load(self, persid):
        if persid and len(persid.split('/')) == 3 and persid.split('/')[0] == 'model':
            persid = persid.split('/')
            return get_model(persid[1], persid[2])
        else:
            raise UnpicklingError('Invalid persistent id')
            
    def find_class(self, module, name):
        ok = False
        for wm in _DjangoQueryUnpickler.white_modules:
            if module.startswith(wm):
                ok = True
                break
        if "%s.%s"%(module, name) in _DjangoQueryUnpickler.white_objects:
            ok = True
        if not ok:
            print UnpicklingError("Unsafe class to unpickle %s.%s"%(module, name))
        return Unpickler.find_class(self, module, name)

def pickle_qs(qs):
    file = StringIO()
    p = _DjangoQueryPickler(file)
    p.dump((qs.__class__, qs.query))
    return file.getvalue()
    
def unpickle_qs(str):
    file = StringIO(str)
    up = _DjangoQueryUnpickler(file)
    (klass, query) = up.load()
    #query.model = get_model(query.model[0], query.model[1])
    qs = klass(model=query.model,query=query)
    return qs