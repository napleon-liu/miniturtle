from scanner.token import *


class ExprNode:
    def __init__(self, opcode, *args):
        self.Opcode = opcode
        self.Content = self.ContentStruct()

        if opcode == TokenType.CONST_ID:
            self.Content.CaseConst = float(args[0])
        elif opcode == TokenType.T:
            self.Content.CaseParaPtr = args[0]
        elif opcode == TokenType.FUNC:
            self.Content.CaseFunc.MathFuncPtr = args[0]
            self.Content.CaseFunc.Child = args[1]
        else:
            self.Content.CaseOperator.Left = args[0]
            self.Content.CaseOperator.Right = args[1]

    class ContentStruct:
        def __init__(self):
            self.CaseOperator = self.CaseOperatorStruct()
            self.CaseFunc = self.CaseFuncStruct()
            self.CaseConst = 0.0
            self.CaseParaPtr = None

        class CaseOperatorStruct:
            def __init__(self):
                self.Left = None
                self.Right = None

        class CaseFuncStruct:
            def __init__(self):
                self.Child = None
                self.MathFuncPtr = None


def print_expr_tree(node, indent=''):
    print(indent + 'Opcode:', node.Opcode)
    if node.Opcode == TokenType.PLUS or node.Opcode == TokenType.MINUS or node.Opcode == TokenType.MUL or node.Opcode == TokenType.DIV or node.Opcode == TokenType.POWER:
        print(indent + 'Left:')
        print_expr_tree(node.Content.CaseOperator.Left, indent + '|  ')
        print(indent + 'Right:')
        print_expr_tree(node.Content.CaseOperator.Right, indent + '|  ')
    elif node.Opcode == TokenType.FUNC:
        print(indent + 'Child:')
        print_expr_tree(node.Content.CaseFunc.Child, indent + '|  ')
        print(indent + 'MathFuncPtr:', node.Content.CaseFunc.MathFuncPtr)
    elif node.Opcode == TokenType.CONST_ID:
        print(indent + 'CaseConst:', node.Content.CaseConst)
    elif node.Opcode == TokenType.T:
        print(indent + 'CaseParaPtr:', node.Content.CaseParaPtr)
