from __future__ import annotations
from threading import Lock


class CacheData:
    data: any
    prev: CacheData
    next: CacheData

    def __init__(
        self,
        data: any = None,
        prev_node: CacheData | None = None,
        next_node: CacheData | None = None
    ):
        self.data = data
        self.prev = prev_node
        self.next = next_node


class LRU:
    """
    BTP enforce a 210s timeout while the time has a 30s fluctuation
    compared with the real time which means a valid package received
    240s before can be still valid on received again.
    The lru stores 240000 previous received package, a package received
    240s before cannot be replay unless server received more then
    240000 VALID btp connection in 240s to push it out, the qps under
    this condition is 240000/240 = 1000, exceeding target performance
    When the lru size is 200000, __cache takes 8388824 (8M) memory,
    Total memory taken under 240000 data will be 90~MB, acceptable!
    """
    __instance: LRU = None
    __cache: set = set()
    __lock: Lock = Lock()

    __head: CacheData  # newest
    __tail: CacheData  # oldest

    __max_size: int = 240000
    __size: int = 0

    def __init__(self, max_size: int | None = 240000):
        self.__max_size = max_size
        assert max_size > 0

        self.__head = CacheData()
        self.__tail = CacheData(None, self.__head)
        self.__head.next = self.__tail

    @classmethod
    def get_instance(cls):
        # NOT thread safe
        if cls.__instance is None:
            cls.__instance = LRU()
        return cls.__instance

    def add(self, data):
        self.__lock.acquire()

        if data in self.__cache:
            raise Exception('digest existed!')

        self.__cache.add(data)

        new_data = CacheData(data,
                             self.__head,
                             self.__head.next)

        self.__head.next = new_data
        if new_data.next is not None:
            new_data.next.prev = new_data
        self.__size += 1

        if self.__size == self.__max_size:  # delete oldest
            del_node = self.__tail.prev
            self.__cache.remove(del_node.data)

            prev_node = del_node.prev
            self.__tail.prev = prev_node
            prev_node.next = self.__tail
            self.__size -= 1

        self.__lock.release()
