
from __future__ import absolute_import, division, \
                       print_function, unicode_literals
import re
from crushlib.crushmap.rules import Rule, Steps
from crushlib.crushmap.buckets import Bucket


def parse_raw(crushmap, map_obj):
    parsed = _raw_to_dict(crushmap)
    parse_tunables(map_obj, parsed['tunable'])
    parse_devices(map_obj, parsed['device'])
    parse_types(map_obj, parsed['type'])
    parse_buckets(map_obj, parsed['bucket'])
    parse_rules(map_obj, parsed['rule'])


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
                    raise ValueError("CRUSH Parsing error")
                in_block = True
                block = [l]
                block_type = 'rule' if head == 'rule' else 'bucket'
                raw_dict.setdefault(block_type, [])
    return raw_dict


def parse_tunables(map_obj, tun_list):
    for raw in tun_list:
        line = raw.split()
        if line[0] != 'tunable':
            raise ValueError("Tunable Parsing error: Line should begin "
                             "with 'tunable'")
        try:
            name = line[1]
            value = int(line[2])
        except IndexError:
            raise ValueError("Tunable Parsing error: Tunable declaration "
                             " is incomplete!")
        except ValueError:
            raise ValueError("Tunable Parsing error: Tunable value expected "
                             "to be an integer!")
        map_obj.tunables.update_setting(name, value)


def parse_devices(map_obj, dev_list):
    for raw in dev_list:
        line = raw.split()
        if line[0] != 'device':
            raise ValueError("Device parsing error: Line should begin "
                             "with 'device'")

        try:
            num = int(line[1])
            name = line[2]
        except IndexError:
            raise ValueError("Device parsing error: Device declaration "
                             "is incomplete!")
        except ValueError:
            raise ValueError("Device parsing error: Device number expected "
                             "to be an integer!")

        if name == ('osd.{}'.format(num)):
            map_obj.devices.add(num)
        else:
            continue


def parse_types(map_obj, types_list):
    for string in types_list:
        line = string.split()
        if line[0] != 'type':
            raise ValueError(
                "Types Parsing error: Line shoudl begin with 'type'")

        try:
            id = int(line[1])
            name = line[2]
        except IndexError:
            raise ValueError("Types Parsing error: Type declaration "
                             " is incomplete!")
        except ValueError:
            raise ValueError("Type Parsing error: Type ID expected "
                             "to be an integer!")

        map_obj.types.add(name, id)


def parse_buckets(crushmap, buckets_list):

    def parse_bucket(bucket_raw):
        items = []
        for string in bucket_raw:
            line = string.split()
            head = line[0]
            value = line[1]

            if line[-1] == '{':  # First line: open bucket declaration
                type_obj = crushmap.types.get(name=head)
                name = value
            elif head == 'item':
                item = (crushmap.get_item(name=value), float(line[3]))
                items.append(item)
            elif head == 'id':
                id = int(value)
            elif head == 'alg':
                alg = value
            elif head == 'hash':
                if value == '0':
                    hash = 'rjenkins1'
                else:
                    raise ValueError("Unknown hash {}".format(value))
            else:
                raise ValueError("Unknown property {}".format(head))

        bucket = Bucket(name, type_obj, id, alg, hash)
        for i in items:
            bucket.add_item(i[0], i[1])
        return bucket

    for bucket_raw in buckets_list:
        crushmap.buckets.add(parse_bucket(bucket_raw))


def parse_rules(map_obj, rules_list):
    for rule_list in rules_list:
        steps = Steps()

        for line in rule_list:
            l = line.split()
            head = l[0]
            value = l[1]

            if head == 'rule':
                name = value
            elif head == 'ruleset':
                ruleset = int(value)
            elif head == 'type':
                rule_type = value
            elif head == 'min_size':
                min_size = int(value)
            elif head == 'max_size':
                max_size = int(value)
            elif head == 'step':
                op = value
                if op == 'take':
                    item = map_obj.get_item(name=l[2])
                    steps.add(op, item=item)
                elif op in ('choose', 'chooseleaf'):
                    scheme = l[2]
                    num = int(l[3])
                    type_obj = map_obj.types.get(name=l[5])
                    steps.add(op, scheme=scheme, num=num, type=type_obj)
                elif op == 'emit':
                    steps.add(op)
                else:
                    raise ValueError("Unknown operation {}".format(op))
            else:
                raise ValueError("Unknown key {}".format(head))

        rule = Rule(name, ruleset=ruleset, rule_type=rule_type,
                    steps=steps, min_size=min_size, max_size=max_size)
        map_obj.rules.add(rule)
