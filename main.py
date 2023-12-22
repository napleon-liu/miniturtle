# from scanner.scanner import Scanner
from parser.parser import Parser
from semantics import Semantics


def main():
    parser = Parser("testcase.txt")
    semantics = Semantics(parser)
    semantics.parse()
    semantics.run()


if __name__ == '__main__':
    main()
