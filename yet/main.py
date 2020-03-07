import argparse
import logging
import os
import sys

from yet.loader import load_yet

logger = logging.getLogger()


def step(in_path, out_path):
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
    elif os.path.exists(args.input):
        if os.path.isfile(args.input):
            in_path = args.input
        else:
            raise NotImplementedError('Directory batch-processing is not supported yet')
    else:
        raise FileNotFoundError(f'Path {args.input} does not exist')

    if args.output == '-':
        out_path = sys.stdout
    elif args.output is None:
        if args.input == '-':
            out_path = sys.stdout
        else:
            # change YAML extension to .tex
            if args.input.endswith('.yaml'):
                out_path = f'{args.input[:-5]}.tex'
            elif args.input.endswith('.yml'):
                out_path = f'{args.input[:-4]}.tex'
            # or append .tex if appropriate extension is not found
            else:
                out_path = f'{args.input}.tex'
    else:
        out_path = args.output

    step(in_path, out_path)
