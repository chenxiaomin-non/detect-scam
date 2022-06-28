import threading

class QueryResult:
    __result__ = {}
    index = 0

    def __init__(self) -> None:
        self.__result__ = {}
        self.index = 0
        self.lock = threading.Lock()
    
    def get_index(self) -> int:
        self.lock.acquire()
        self.index += 1
        self.lock.release()
        return self.index
    
    def get_result(self, index: int):
        self.lock.acquire()
        result = self.__result__.pop(index)
        self.lock.release()
        return result
    
    def update_result(self, index: int, result: object):
        self.lock.acquire()
        self.__result__[index] = result
        self.lock.release()

result_bag = QueryResult()