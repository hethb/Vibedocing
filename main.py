import ast

class CodeExplainer(ast.NodeVisitor):
    def __init__(self):
        self.explanations = []

    def visit_FunctionDef(self, node):
        args = [arg.arg for arg in node.args.args]
        self.explanations.append(f"Defines a function '{node.name}' with parameters {args}.")
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = [ast.unparse(t) for t in node.targets]
        value = ast.unparse(node.value)
        self.explanations.append(f"Assigns {value} to {', '.join(targets)}.")
        self.generic_visit(node)

    def visit_Call(self, node):
        func_name = ast.unparse(node.func)
        args = [ast.unparse(a) for a in node.args]
        self.explanations.append(f"Calls the function '{func_name}' with arguments {args}.")
        self.generic_visit(node)

    def visit_Return(self, node):
        value = ast.unparse(node.value)
        self.explanations.append(f"Returns {value} from the function.")
        self.generic_visit(node)

    def visit_If(self, node):
        test = ast.unparse(node.test)
        self.explanations.append(f"If statement checking condition: {test}.")
        self.generic_visit(node)

    def visit_For(self, node):
        target = ast.unparse(node.target)
        iter_ = ast.unparse(node.iter)
        self.explanations.append(f"For loop iterating over {iter_} with variable '{target}'.")
        self.generic_visit(node)

def explain_code(code: str):
    tree = ast.parse(code)
    explainer = CodeExplainer()
    explainer.visit(tree)
    return "\n".join(explainer.explanations)

if __name__ == "__main__":
    print("Paste Python code below (end with Ctrl+D or Ctrl+Z):\n")
    import sys
    user_code = sys.stdin.read()
    explanation = explain_code(user_code)
    print("\n--- Explanation ---\n")
    print(explanation)
