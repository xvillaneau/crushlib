
import re


def parse_raw(crushmap):
    return _raw_to_dict(crushmap)


def _raw_to_dict(raw_str):
    lines = raw_str.split('\n')
    raw_dict = {}

    block_type = ''
    in_block = False
    block = []
    for line in lines:
        l = re.sub('#.*$', '', line).strip()

        if not l:
            continue
        head = l.split()[0]

        if in_block:
            if head == '}':
                raw_dict[block_type].append(block)
                in_block = False
            else:
                block.append(l)
        else:
            if head in ('tunable', 'device', 'type'):
                raw_dict.setdefault(head, [])
                raw_dict[head].append(l)
            else:
                if not l.endswith('{'):
                    raise IOError("CRUSH Parsing error")
                in_block = True
                block = [l]
                block_type = 'rule' if head == 'rule' else 'bucket'
                raw_dict.setdefault(block_type, [])
    return raw_dict
