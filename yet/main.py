import argparse
import logging
import os
import sys

from yet.loader import load_yet

logger = logging.getLogger()


def convert_extension(filename, extensions=('yaml', 'yml',)):
    """
    Convert YeT extension in filename to .tex

    :param filename: string of file name. validity not checked.
    :param extensions: tuple of extensions (without dot) to treat as YeT
    """
    # change YAML extension to .tex
    if '.' in filename:
        ext = filename.split('.')[-1]
        if ext in extensions:
            idx = filename.rindex('.')
            return f'{filename[:idx]}.tex'
    # or append .tex if appropriate extension is not found
    return f'{filename}.tex'


def process_dir(in_path, out_path, extensions=('yaml', 'yml',)):
    """
    Read from in_path, convert YeT to TeX, and write to out_path

    :param in_path: string of existent directory path
    :param out_path: string of valid directory path, or sys.stdout
    :param extensions: tuple of extensions (without dot) to treat as YeT
    """
    if isinstance(out_path, str):
        os.makedirs(out_path, mode=0o644, exist_ok=True)

    for root, _, files in os.walk(in_path):
        logger.info(f'entering directory {root}')
        for name in files:
            if '.' in name and name.split('.')[-1] in extensions:
                _in_path = os.path.join(root, name)
                logger.info(f'found YeT file {_in_path}')
                if out_path is sys.stdout:
                    _out_path = sys.stdout
                else:
                    _out_path = os.path.join(root.replace(in_path, out_path, 1),
                                             convert_extension(name, extensions))
                process_file(_in_path, _out_path)


def process_file(in_path, out_path):
    """
    Read from in_path, convert YeT to TeX, and write to out_path

    :param in_path: string of existent file path, or sys.stdin
    :param out_path: string of valid file path, or sys.stdout
    """
    if in_path is sys.stdin:
        logger.info('reading from stdin')
        yet = load_yet(sys.stdin)
    else:
        logger.info(f'reading from {in_path}')
        with open(in_path) as f:
            yet = load_yet(f)

    tex = '\n'.join([str(v) for v in yet])

    if out_path is sys.stdout:
        logger.info('writing to stdout')
        print(tex)
    else:
        logger.info(f'writing to {out_path}')
        with open(out_path, 'w') as f:
            print(tex, file=f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input',
                        metavar='FILE',
                        type=str)
    parser.add_argument('--output',
                        metavar='FILE',
                        type=str,
                        default=None)
    parser.add_argument('--verbose',
                        action='store_true',
                        dest='verbose')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    logger.setLevel('INFO' if args.verbose else 'WARNING')
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter('{asctime} [{levelname}] {message}', style='{')
    )
    logger.addHandler(handler)

    if args.input == '-':
        in_path = sys.stdin
        out_path = sys.stdout if args.output in (None, '-') else args.output
    elif os.path.exists(args.input):
        in_path = args.input
        if os.path.isdir(in_path):
            out_path = sys.stdout if args.output == '-'\
                                  else in_path if args.output is None\
                                  else args.output
            return process_dir(in_path, out_path)
        out_path = sys.stdout if args.output == '-'\
                              else convert_extension(in_path) if args.output is None\
                              else args.output
    else:
        raise FileNotFoundError(f'Path {args.input} does not exist')

    process_file(in_path, out_path)
