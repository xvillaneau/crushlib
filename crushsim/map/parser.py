
from crushsim.map.tunables import Tunables
from crushsim.map.devices import Devices
import re


def parse_raw(crushmap, map_obj):
    parsed = _raw_to_dict(crushmap)
    map_obj.tunables = parse_tunables(parsed['tunable'])
    map_obj.devices = parse_devices(parsed['device'])


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


def parse_tunables(tun_list):
    tun_obj = Tunables()
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
        tun_obj.update_setting(name, value)
    return tun_obj


def parse_devices(dev_list):
    dev_obj = Devices()
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
            dev_obj.add(num)
        elif name == ('device{}'.format(num)):
            continue
        else:
            raise ValueError("Device parsing error: Unrecognized name {} for "
                             "number {}".format(name, num))

    return dev_obj
