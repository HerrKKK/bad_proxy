import sys
sys.path.append("../src")

from proxy.domain_trie import DomainTrie

trie = DomainTrie()

DomainTrie.DATA_PATH = '../domains/'
trie.read_from_files('geolocation-cn')

print('baidu.com' in trie,
      'google.com' in trie,
      trie.has_domain('bilibili.bilipala.baidu.com'))
trie.add('google.com')
print('google.com' in trie)
