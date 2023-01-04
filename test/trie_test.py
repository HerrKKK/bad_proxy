import sys
import os
sys.path.append("../src")

from proxy.domain_trie import DomainTrie

os.chdir('../')

trie = DomainTrie.get_instance()

assert 'baidu.com' in trie
assert 'google.com' not in trie
assert trie.has_domain('bilibili.bilipala.baidu.com')
assert 'wwr-blog.com' in trie
