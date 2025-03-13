import ast

# Mapping of Python operators to Octave operators
OPERATOR_MAP = {
    "Add": "+",
    "Sub": "-",
    "Mult": "*",
    "Div": "/",
    "Pow": "^",
    "Eq": "==",
    "NotEq": "!=",
    "Lt": "<",
    "LtE": "<=",
    "Gt": ">",
    "GtE": ">=",
    "And": "&&",
    "Or": "||",
}

# Mapping of Python functions to Octave functions
FUNCTION_MAP = {
    "print": "disp",
    "range": "1:",  # Octave uses 1-based indexing
    "len": "length",
}

# Translate Python operators to Octave
def translate_operator(op):
    return OPERATOR_MAP.get(op.__class__.__name__, str(op))

# Translate Python expressions to Octave
def translate_expr(node):
    if isinstance(node, ast.Num):  # Numbers
        return str(node.n)
    elif isinstance(node, ast.Name):  # Variables
        return node.id
    elif isinstance(node, ast.BinOp):  # Binary operations
        left = translate_expr(node.left)
        right = translate_expr(node.right)
        op = translate_operator(node.op)
        return f"({left} {op} {right})"
    elif isinstance(node, ast.Call):  # Function calls
        func_name = node.func.id
        args = ", ".join(translate_expr(arg) for arg in node.args)
        return f"{FUNCTION_MAP.get(func_name, func_name)}({args})"
    elif isinstance(node, ast.Compare):  # Comparisons
        left = translate_expr(node.left)
        ops = " ".join(translate_operator(op) for op in node.ops)
        comparators = " ".join(translate_expr(comp) for comp in node.comparators)
        return f"{left} {ops} {comparators}"
    elif isinstance(node, ast.Assign):  # Assignments
        target = translate_expr(node.targets[0])
        value = translate_expr(node.value)
        return f"{target} = {value};"
    elif isinstance(node, ast.For):  # For loops
        target = translate_expr(node.target)
        iterable = translate_expr(node.iter)
        body = "\n".join(translate_expr(stmt) for stmt in node.body)
        return f"for {target} = {iterable}\n{body}\nend"
    elif isinstance(node, ast.If):  # If statements
        test = translate_expr(node.test)
        body = "\n".join(translate_expr(stmt) for stmt in node.body)
        orelse = "\n".join(translate_expr(stmt) for stmt in node.orelse)
        return f"if {test}\n{body}\nelse\n{orelse}\nend"
    else:
        return f"# UNSUPPORTED: {ast.dump(node)}"

# Translate a Python script to Octave
def translate_python_to_octave(python_code):
    tree = ast.parse(python_code)
    octave_code = []
    for node in tree.body:
        octave_code.append(translate_expr(node))
    return "\n".join(octave_code)

# Main function
def main():
    # Input Python file
    python_file = input("Enter the path to the Python file: ")
    with open(python_file, "r") as f:
        python_code = f.read()

    # Translate Python code to Octave
    octave_code = translate_python_to_octave(python_code)

    # Output Octave file
    octave_file = python_file.replace(".py", ".m")
    with open(octave_file, "w") as f:
        f.write(octave_code)

    print(f"Translated Octave code saved to {octave_file}")

if __name__ == "__main__":
    main()