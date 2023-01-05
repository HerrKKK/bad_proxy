from __future__ import annotations
import re

"""
This file filtrate domains from CN used meta data from
https://github.com/v2fly/domain-list-community/blob/master/data/geolocation-cn
"""


class DomainTrie:
    __DATA_FOLDER = 'domains/'
    __LEN: int = 128  # ascii
    __nodes: list[DomainTrie | None]  # None means not exist
    __is_end: bool = False
    __instance: DomainTrie = None

    def __init__(self):
        self.__nodes = DomainTrie.__LEN * [None]

    def __contains__(self, domain: str):
        return self.has(domain)

    @classmethod
    def get_instance(cls):
        # NOT thread safe
        if cls.__instance is None:
            cls.__instance = DomainTrie()
            cls.__instance.__read_from_file()
        return cls.__instance

    def __read_from_file(self, filename: str | None = 'geolocation-cn'):
        filename = DomainTrie.__DATA_FOLDER + filename
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
            self.__add(domain)
        for fn in included_files:
            self.__read_from_file(fn)

    def __add(self, s: str):
        # NOT thread safe
        if s is None or len(s) == 0:
            return
        # use iteration to improve performance
        idx, pos, length, this = 0, 0, len(s), self
        while idx < length:
            pos = ord(s[idx])
            if this.__nodes[pos] is None:
                this.__nodes[pos] = DomainTrie()
            this = this.__nodes[pos]
            idx += 1  # idx is index of s, pos is position of char in map
        this.__is_end = True

    def has(self, s: str) -> bool:
        if s is None or len(s) == 0:
            return False

        idx, pos, length, this = 0, 0, len(s), self
        while idx < length:
            pos = ord(s[idx])
            if this.__nodes[pos] is None:
                return False
            this = this.__nodes[pos]
            idx += 1

        return this.__is_end

    def has_domain(self, domain: str):
        try:
            domains = domain.split('.')
            return self.has(f'{domains[-2]}.{domains[-1]}')
        except Exception as e:
            print(e)
            return False
