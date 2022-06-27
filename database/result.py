import types

def _get_method_names(obj):
    if type(obj) == types.InstanceType:
        return _get_method_names(obj.__class__)
    elif type(obj) == types.ClassType:
        result = []
        for name, func in obj.__dict__.items():
            if type(func) == types.FunctionType:
                result.append((name, func))
        for base in obj.__bases__:
            result.extend(_get_method_names(base))
        return result


class _SynchronizedMethod:
    def __init__(self, method, obj, lock):
        self.__method = method
        self.__obj = obj
        self.__lock = lock

    def __call__(self, *args, **kwargs):
        self.__lock.acquire()
        try:
            return self.__method(self.__obj, *args, **kwargs)
        finally:
            self.__lock.release()


class QueryResult:
    __result__ =  {}
    __count__ = 0

    def __init__(self, obj, ignore=[], lock=None):
        import threading

        self.__result__ = {}
        self.__count__ = 0

        # You must access __dict__ directly to avoid tickling __setattr__
        self.__dict__['_SynchronizedObject__methods'] = {}
        self.__dict__['_SynchronizedObject__obj'] = obj
        if not lock:
            lock = threading.RLock()
        for name, method in _get_method_names(obj):
            if not name in ignore and not self.__methods.has_key(name):
                self.__methods[name] = _SynchronizedMethod(method, obj, lock)

    def __getattr__(self, name):
        try:
            return self.__methods[name]
        except KeyError:
            return getattr(self.__obj, name)

    def __setattr__(self, name, value):
        setattr(self.__obj, name, value)

    def get_index_result(self):
        self.__count__ += 1
        return self.__count__
    
    def update_result(self, key, value):
        self.__result__[key] = value
    
    def get_result(self, key):
        return self.__result__[key]

    def release(self, key):
        del self.__result__[key]
