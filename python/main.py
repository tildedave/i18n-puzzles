import argparse
from problem6 import answer as problem6_answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('problem')
    parser.add_argument('input_file')

    args = parser.parse_args()
    lines = open(args.input_file, 'r').read().split('\n')
    if args.problem == 'problem6':
        problem6_answer(lines)
