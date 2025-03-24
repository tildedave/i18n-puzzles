import argparse
import problem6
import problem7
import problem8
import problem9
import problem10
import problem11
import problem12
import problem13
import problem14
import problem15
import problem16
import problem17
import problem18


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("problem")
    parser.add_argument("input_file")

    args = parser.parse_args()
    lines = open(args.input_file, "r").read().split("\n")
    if args.problem == "problem6":
        problem6.answer(lines)
    elif args.problem == "problem7":
        problem7.answer(lines)
    elif args.problem == "problem8":
        problem8.answer(lines)
    elif args.problem == "problem9":
        problem9.answer(lines)
    elif args.problem == "problem10":
        problem10.answer(lines)
    elif args.problem == "problem11":
        problem11.answer(lines)
    elif args.problem == "problem12":
        problem12.answer(lines)
    elif args.problem == "problem13":
        problem13.answer(lines)
    elif args.problem == "problem14":
        problem14.answer(lines)
    elif args.problem == "problem15":
        problem15.answer(lines)
    elif args.problem == "problem16":
        problem16.answer(lines)
    elif args.problem == "problem17":
        problem17.answer(lines)
    elif args.problem == "problem18":
        problem18.answer(lines)
    else:
        raise ValueError("Invalid Problem")
