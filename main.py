from scanner.scanner import Scanner


def main():
    scanner = Scanner("testcase.txt")
    print("{:<20}{:<15}{:<20}{:<10}".format("Token Type", "Token Lexeme", "Token Value", "Token Func Ptr"))
    while scanner.read_token():
        token = scanner.get_token()
        print(token)


if __name__ == '__main__':
    main()

