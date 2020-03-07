import argparse
import logging
import sys

from yet.loader import load_yet

logger = logging.getLogger()


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
        # read from stdin
        logger.info('reading from stdin')
        yet = load_yet(sys.stdin)
    else:
        # read from given file
        logger.info(f'reading from {args.input}')
        with open(args.input) as f:
            yet = load_yet(f)

    tex = '\n'.join([str(v) for v in yet])

    if args.output == '-' or args.input == '-':
        # print to stdout
        logger.info('writing to stdout')
        print(tex)
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

        logger.info(f'writing to {output_path}')
        with open(output_path, 'w') as f:
            print(tex, file=f)
