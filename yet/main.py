import argparse
import sys

from yet.loader import load_yet


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
        yet = load_yet(sys.stdin)
    else:
        # read from given file
        with open(args.input) as f:
            yet = load_yet(f)

    tex = '\n'.join([str(v) for v in yet])

    if args.output == '-' or args.input == '-':
        # print to stdout
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

        with open(output_path, 'w') as f:
            print(tex, file=f)
