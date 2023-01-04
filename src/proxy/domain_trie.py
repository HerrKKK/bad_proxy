from __future__ import annotations
import re

"""
This file filtrate domains from CN used meta data from
https://github.com/v2fly/domain-list-community/blob/master/data/geolocation-cn
"""


class DomainTrie:
    DATA_PATH = 'domains/'
    LEN: int = 128  # ascii
    __nodes: list[DomainTrie | None]  # None means not exist

    def __init__(self):
        self.__nodes = DomainTrie.LEN * [None]

    def __contains__(self, domain: str):
        return self.has(domain)

    def add(self, s: str):
        if s is None or len(s) == 0:
            return
        # use iteration to improve performance
        idx, pos, length, __nodes = 0, 0, len(s), self.__nodes
        while idx < length:
            pos = ord(s[idx])
            if __nodes[pos] is None:
                __nodes[pos] = DomainTrie()
            __nodes = __nodes[pos].__nodes
            idx += 1  # idx is index of s, pos is position of char in map

    def has(self, s: str) -> bool:
        if s is None or len(s) == 0:
            return False

        idx, pos, length, __nodes = 0, 0, len(s), self.__nodes
        while idx < length:
            pos = ord(s[idx])
            if __nodes[pos] is None:
                return False
            __nodes = __nodes[pos].__nodes
            idx += 1

        return True

    def has_domain(self, domain: str):
        try:
            domains = domain.split('.')
            return self.has(f'{domains[-2]}.{domains[-1]}')
        except Exception as e:
            print(e)
            return False

    def read_from_files(self, filename: str):
        filename = DomainTrie.DATA_PATH + filename
        file = open(filename, 'r', encoding='utf-8')
        content = file.read()
        # remove comment and empty lines
        comment_pattern = re.compile('(#.*(?=\n)|\x20*)', re.MULTILINE)
        content = comment_pattern.sub('', content)
        # domains start with include:
        include_pattern = re.compile(r'(?<=include:).*', re.MULTILINE)
        included_files = include_pattern.findall(content)
        # lines without include:
        domain_pattern = re.compile(r'^(?!include).+$', re.MULTILINE)
        domains = domain_pattern.findall(content)

        file.close()

        for domain in domains:
            self.add(domain)
        for fn in included_files:
            self.read_from_files(fn)
