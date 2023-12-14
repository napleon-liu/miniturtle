class ExprNode:
    def __init__(self, opcode, content):
        self.opcode = opcode
        self.content = content


class CaseOperator:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class CaseFunc:
    def __init__(self, child, math_func_ptr):
        self.child = child
        self.math_func_ptr = math_func_ptr


def print_expr_node(node, indent="", is_last=True):
    marker = "`- " if is_last else "|- "
    print(f"{indent}{marker}{node.opcode}")

    if isinstance(node.content, CaseOperator):
        print_expr_node(node.content.left, indent + ("   " if is_last else "|  "), False)
        print_expr_node(node.content.right, indent + ("   " if is_last else "|  "), True)
    elif isinstance(node.content, CaseFunc):
        print_expr_node(node.content.child, indent + ("   " if is_last else "|  "), True)
    elif isinstance(node.content, float):
        print(f"{indent}   |- Constant: {node.content}")
    elif isinstance(node.content, list):
        print(f"{indent}   |- Parameter: {node.content}")
    else:
        print(f"{indent}   |- Unknown content")


# 示例用法：
left_node = ExprNode("ADD", 2.0)
right_node = ExprNode("SUB", 3.0)
operator_node = CaseOperator(left_node, right_node)
expr_node = ExprNode("MUL", operator_node)

print_expr_node(expr_node)
