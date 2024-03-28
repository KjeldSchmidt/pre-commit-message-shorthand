import argparse

print("Top level print.")


def print_arguments(arguments: list[str]):
    for argument in arguments:
        print(argument)


def main():
    print("Print in main")
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    print_arguments(args.filenames)
    exit(1)


if __name__ == "__main__":
    print("Print in __main__ gate")
    main()
