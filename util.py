from typing import List

# Formats a bunch of lines into a list of lines<2000 chars
def long_print(lines: str) -> List[str]:
    s = ''
    out = []
    for l in lines.split('\n'):
        if len(s) + len(l) + 1 < 2000:
            s += l + '\n'
        else:
            out.append(s)
            s = l + '\n'

    return out
