from __future__ import annotations
import re

"""
This file filtrate domains from CN used meta data from
https://github.com/v2fly/domain-list-community/blob/master/data/geolocation-cn
"""


class DomainCache:
    __DATA_FOLDER = 'domains/'
    __set: set[str]
    __instance: DomainCache = None

    def __init__(self):
        self.__set = set()

    def __contains__(self, domain: str):
        return domain in self.__set

    @classmethod
    def get_instance(cls):
        # NOT thread safe
        if cls.__instance is None:
            cls.__instance = DomainCache()
            cls.__instance.__read_from_file()
        return cls.__instance

    def __read_from_file(self, filename: str | None = 'geolocation-cn'):
        filename = DomainCache.__DATA_FOLDER + filename
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
        self.__set.add(s)

    def has_domain(self, domain: str):
        try:
            domains = domain.split('.')
            return f'{domains[-2]}.{domains[-1]}' in self.__set
        except Exception as e:
            print(e)
            return False
