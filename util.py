from typing import List, Iterator

# Formats a bunch of lines into a list of lines<2000 chars
def long_print(lines: List[str]) -> Iterator[str]:
    s = ''
    for l in lines:
        if len(s) + len(l) + 1 < 2000:
            s += l + '\n'
        else:
            yield s
            s = l + '\n'
    if len(s) != 0:
        yield s
