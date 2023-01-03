import sys
sys.path.append("../src")

from protocols.btp_lru import LRU


lru = LRU()

for i in range(200000):  # 200000: 8388824 Bytes(8M), 48Bytes for a single data
    lru.add(i.to_bytes(32, 'big'))

lru.debug()

