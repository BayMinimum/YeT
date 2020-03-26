# singleton dict-like containers

__all__ = ['Command', 'Environment']


DELIM_R_TO_L = {
    '}': '{',
    ']': '[',
}

DELIM_MATH = ['$', '$$']


def separate_tail_args(s: str):
    idx = len(s)
    while idx > 0 and s[idx - 1] in DELIM_R_TO_L and DELIM_R_TO_L[s[idx - 1]] in s:
        idx = s.rindex(DELIM_R_TO_L[s[idx - 1]])
    return s[:idx], s[idx:]


class _Container(object):
    def __init__(self, key, value):
        self.key = str(key)
        self.value = value


class Command(_Container):
    def __str__(self):
        if self.key in DELIM_MATH:
            ret = f'{self.key}{self.value}{self.key}'
        elif self.key.startswith('_'):
            # treat value as-is
            ret = f'\\{self.key[1:]}' if len(self.key) > 1 else ''
            ret += str(self.value)
        else:
            v, v_args = separate_tail_args(self.value)
            ret = f'\\{self.key}{v_args}'
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
