import re


def remove_comment(filename: str):
    with open(filename, 'r+', encoding='utf-8') as file:
        # if len(line) > 8 and line[:8] == 'include:':
        # self.read_from_file(DomainTrie.DATA_PATH + line[8:])
        content = file.read()
        # remove comment and empty lines
        # pattern = re.compile('(?<=\n)\s*#\s*[^\n]*\n|(?<!\S)\n')
        pattern = re.compile('(#.*(?=\n)|\x20*)')
        output = pattern.sub('', content)

        file.seek(0)
        file.truncate()
        file.write(output)


def test_re():
    with open('reg_test_field', 'r', encoding='utf-8') as f:
        content = f.read()
        # print(content)
        pattern = re.compile(r'^.*$', re.MULTILINE)
        res = pattern.findall(content)
        print(res)

if __name__ == '__main__':
    # remove_comment('lru_test.py')
    test_re()
