import sys
import os
import time
sys.path.append("../src")

from proxy.domain_cache import DomainCache

os.chdir('../')

trie = DomainCache.get_instance()

assert 'baidu.com' in trie
assert 'google.com' not in trie
assert trie.has_domain('bilibili.bilipala.baidu.com')
assert 'wwr-blog.com' in trie

before = time.time()
for i in range(0, 1000):
    assert 'baidu.com' in trie
    assert 'google.com' not in trie
    assert trie.has_domain('bilibili.bilipala.baidu.com')
after = time.time()
print(f'consumed {after - before}')
