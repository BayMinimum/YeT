import argparse
import sys

import yaml


DELIM_R_TO_L = {
    '}': '{',
    ']': '[',
}


def separate_tail_args(s: str):
    idx = len(s)
    while idx > 0 and s[idx - 1] in DELIM_R_TO_L and DELIM_R_TO_L[s[idx - 1]] in s:
        idx = s.rindex(DELIM_R_TO_L[s[idx - 1]])
    return s[:idx], s[idx:]


# singleton dict-like containers

class _Container(object):
    def __init__(self, key, value):
        self.key = str(key)
        self.value = value


class Command(_Container):
    def __str__(self):
        ret = f'\\{self.key}'
        v, v_args = separate_tail_args(self.value)
        ret += v_args
        if v:
            ret += f'{{{v}}}'
        return ret

    def __repr__(self):
        return f'<Command object of {{{self.key}: {self.value}}}>'


class Environment(_Container):
    def __str__(self):
        k, k_args = separate_tail_args(self.key)
        ret = f'\\begin{{{k}}}{k_args}\n'

        assert isinstance(self.value, list)
        v_lst = [str(v) if isinstance(v, (str, Command, Environment))
                 else str(v[0]) if isinstance(v, list) and len(v) == 1
                 else None for v in self.value]
        if None in v_lst:
            raise TypeError('''Incompatible type in children of Environment.
            This might be a package bug if there's no YAML error.''')
        ret += '\n\n'.join(v_lst)

        ret += f'\n\\end{{{k}}}'
        return ret

    def __repr__(self):
        return f'<Environment object of {{{self.key}: {self.value}}}>'


# Handle YAML

class YeTLoader(yaml.SafeLoader):
    """
    Customized YAML loader to accommodate YeT style.
    Use 'list of singleton dict-like container'
    instead of returning single dict for everything.
    Advantages: handle duplicate keys, preserve order.
    """
    def __init__(self, stream):
        self.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            self._construct_mapping)
        super(YeTLoader, self).__init__(stream)

    @staticmethod
    def _construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return [Command(k, v) if isinstance(v, str)
                else Environment(k, v)
                for k, v in loader.construct_pairs(node)]


def yet_stream_to_tex_str(stream):
    yet = yaml.load(stream, Loader=YeTLoader)
    return '\n'.join([str(v) for v in yet])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input',
                        metavar='FILE',
                        type=str)
    parser.add_argument('--output',
                        metavar='FILE',
                        type=str,
                        default=None)
    args = parser.parse_args()

    if args.input == '-':
        # read from stdin
        tex_str = yet_stream_to_tex_str(sys.stdin)
    else:
        # read from given file
        with open(args.input) as f:
            tex_str = yet_stream_to_tex_str(f)

    if args.output == '-' or args.input == '-':
        # print to stdout
        print(tex_str)
    else:
        output_path = args.output
        if output_path is None:
            # change YAML extension to .tex
            if args.input.endswith('.yaml'):
                output_path = f'{args.input[:-5]}.tex'
            elif args.input.endswith('.yml'):
                output_path = f'{args.input[:-4]}.tex'
            # or append .tex if appropriate extension is not found
            else:
                output_path = f'{args.input}.tex'

        with open(output_path, 'w') as f:
            print(tex_str, file=f)


if __name__ == '__main__':
    main()
