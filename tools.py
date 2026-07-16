##Contains external tools or utility functions that the AI can use, such as calculators, web search, file operations, or database access.

import ast
import operator as op
import math

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}

FUNCTIONS = {
    'sqrt': math.sqrt,
    'log': math.log,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'exp': math.exp,
    'abs': abs,
}


def calculator(expression: str):
    try:
        tree = ast.parse(expression, mode='eval')
        result = _evaluate(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"
    

def _evaluate(node):

    if isinstance(node, ast.Constant):
        return node.value
    
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )
    
    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.operand)
        )
    
    elif isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Only named functions are allowed.")
        
        func_name = node.func.id

        if func_name not in FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not supported.")
        
        args = [_evaluate(arg) for arg in node.args]
        return FUNCTIONS[func_name](*args)
    raise ValueError(f"Unsupported expression")

if __name__ == "__main__":
    print(calculator("25*18"))
    print(calculator("(45+15)/3"))
