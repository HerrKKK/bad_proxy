from __future__ import annotations

import sys
from threading import Lock


class ListNode:
    prev: any = None
    next: any = None

    def __init__(self, prev_node: any, next_node: any):
        self.prev = prev_node
        self.next = next_node


class CacheData:
    data: any
    node: ListNode

    def __init__(self,
                 data: any = None,
                 prev_node: CacheData | None = None,
                 next_node: CacheData | None = None):
        self.data = data
        self.node = ListNode(prev_node, next_node)


class LRU:
    __cache: set = set()
    __lock: Lock = Lock()

    __head: CacheData  # newest
    __tail: CacheData  # oldest
    """
    BTP enforce a 210s timeout while the time has a 30s fluctuation
    compared with the real time which means a valid package received
    240s before can be still valid on received again.
    The lru stores 240000 previous received package, a package received
    240s before cannot be replay unless server received more then
    240000 VALID btp connection in 240s to push it out, the qps under
    this condition is 240000/240 = 1000, exceeding target performance
    When the lru size is 200000, __cache takes 8388824 (8M) memory,
    a CacheData or ListNode takes 48 Bytes; Total memory taken under
    240000 data will be: ((48*2+32)*200000+8M)*1.2 ~= 38MB, acceptable!
    """
    __max_size: int = 240000
    __size: int = 0

    def __init__(self, max_size: int | None = 240000):
        self.__max_size = max_size
        assert max_size > 0

        self.__head = CacheData()
        self.__tail = CacheData(None, self.__head)
        self.__head.node.next = self.__tail

    def debug(self):
        print(sys.getsizeof(self.__cache),
              sys.getsizeof(self.__head.node.next),
              sys.getsizeof(self.__head.node.next.node))

    def add(self, data):
        self.__lock.acquire()

        if data in self.__cache:
            raise Exception('digest existed!')

        self.__cache.add(data)

        new_data = CacheData(data,
                             self.__head,
                             self.__head.node.next)

        self.__head.node.next = new_data
        if new_data.node.next is not None:
            new_data.node.next.node.prev = new_data
        self.__size += 1

        if self.__size == self.__max_size:  # delete oldest
            prev_node = self.__tail.node.prev.node.prev
            self.__tail.node.prev = prev_node
            prev_node.node.next = self.__tail
            self.__size -= 1

        self.__lock.release()
