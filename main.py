# from scanner.scanner import Scanner
from parser.parser import Parser


def main():
    parser = Parser("testcase.txt")
    parser.program()


if __name__ == '__main__':
    main()
