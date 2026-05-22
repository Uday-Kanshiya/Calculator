import ast
import math
import operator

class SafeEvaluator(ast.NodeVisitor):
    """
    A safe mathematical expression evaluator using Python's AST (Abstract Syntax Tree).
    This avoids the safety issues of raw eval() while providing robust calculations.
    """
    def __init__(self, angle_mode="Radians", variables=None):
        self.angle_mode = angle_mode
        self.variables = variables or {}
        
        # Supported operators mapping
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: lambda x: x,
        }
        
        # Supported constants
        self.constants = {
            'pi': math.pi,
            'PI': math.pi,
            'e': math.e,
            'E': math.e,
        }

    def get_functions(self):
        """
        Returns functions available in the calculator, taking into account 
        the current angle mode (Degrees vs Radians).
        """
        is_deg = (self.angle_mode.lower() == "degrees")
        
        def sin_val(x):
            return math.sin(math.radians(x) if is_deg else x)
            
        def cos_val(x):
            return math.cos(math.radians(x) if is_deg else x)
            
        def tan_val(x):
            # Handle tan(90), tan(270) undefined cases in degrees
            if is_deg:
                x_mod = x % 180
                if abs(x_mod - 90) < 1e-9:
                    raise ValueError("tan(x) is undefined")
            return math.tan(math.radians(x) if is_deg else x)

        def asin_val(x):
            if x < -1 or x > 1:
                raise ValueError("asin domain is [-1, 1]")
            val = math.asin(x)
            return math.degrees(val) if is_deg else val

        def acos_val(x):
            if x < -1 or x > 1:
                raise ValueError("acos domain is [-1, 1]")
            val = math.acos(x)
            return math.degrees(val) if is_deg else val

        def atan_val(x):
            val = math.atan(x)
            return math.degrees(val) if is_deg else val

        def fact_val(x):
            if x < 0 or not float(x).is_integer():
                raise ValueError("Factorial is only defined for non-negative integers")
            if x > 1000:
                raise OverflowError("Factorial value too large to compute")
            return math.factorial(int(x))

        def sqrt_val(x):
            if x < 0:
                raise ValueError("Square root of negative number is undefined (real domain)")
            return math.sqrt(x)

        def cbrt_val(x):
            return math.copysign(abs(x) ** (1/3), x)

        return {
            'sin': sin_val,
            'cos': cos_val,
            'tan': tan_val,
            'asin': asin_val,
            'acos': acos_val,
            'atan': atan_val,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'sqrt': sqrt_val,
            'cbrt': cbrt_val,
            'fact': fact_val,
            'abs': abs,
            'exp': math.exp,
        }

    def evaluate(self, expr_str: str):
        """
        Sanitizes and evaluates the expression string safely.
        """
        # 1. Clean visual operators to python operators
        expr_str = expr_str.replace('^', '**')
        expr_str = expr_str.replace('π', 'pi')
        expr_str = expr_str.replace('×', '*')
        expr_str = expr_str.replace('÷', '/')
        
        # 2. STRICT CHECK: Block any logarithmic inputs
        # Look for log/ln as word tokens to prevent substrings like "clog" or "blog" from blocking, 
        # but let's be extremely safe: block any case-insensitive occurrences of log, ln, log10, log2.
        # We also check for them specifically.
        expr_lower = expr_str.lower()
        forbidden_keywords = ['log', 'ln', 'log10', 'log2']
        
        # We can tokenize or simply check if any of these exist in the string.
        # To avoid blocking words like "cbrt" because of "ln" (wait, "cbrt" does not have "ln"),
        # but let's make sure we check for exact log patterns.
        # A simple check: check for 'log', 'ln' (as words or followed by '(').
        # To be completely safe and strict, let's check:
        import re
        for forbidden in forbidden_keywords:
            # Match word boundary or prefix, e.g., "log(", "log (", "ln(", etc.
            pattern = rf"\b{forbidden}\b|{forbidden}\s*\("
            if re.search(pattern, expr_lower):
                raise ValueError("Logarithmic functions ('log', 'ln') are strictly disabled in this calculator.")

        if not expr_str.strip():
            return ""

        try:
            node = ast.parse(expr_str, mode='eval')
            return self.visit(node.body)
        except SyntaxError as e:
            raise ValueError("Invalid syntax") from e
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        except OverflowError:
            raise ValueError("Result too large (overflow)")

    def visit_Num(self, node):
        return node.n

    def visit_Constant(self, node):
        return node.value

    def visit_BinOp(self, node):
        op_type = type(node.op)
        if op_type not in self.operators:
            raise TypeError(f"Unsupported operator: {op_type.__name__}")
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        try:
            return self.operators[op_type](left, right)
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        except OverflowError:
            raise ValueError("Result overflow")

    def visit_UnaryOp(self, node):
        op_type = type(node.op)
        if op_type not in self.operators:
            raise TypeError(f"Unsupported operator: {op_type.__name__}")
        operand = self.visit(node.operand)
        return self.operators[op_type](operand)

    def visit_Name(self, node):
        name = node.id
        if name in self.variables:
            return self.variables[name]
        if name in self.constants:
            return self.constants[name]
        raise NameError(f"Undefined symbol: '{name}'")

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise TypeError("Unsupported function syntax")
        
        func_name = node.func.id
        funcs = self.get_functions()
        
        if func_name not in funcs:
            if func_name in ['log', 'ln', 'log10', 'log2']:
                raise ValueError("Logarithmic functions are strictly disabled.")
            raise NameError(f"Unsupported function: '{func_name}'")
        
        if len(node.args) != 1:
            raise TypeError(f"Function '{func_name}' expects exactly 1 argument")
        
        arg_val = self.visit(node.args[0])
        try:
            return funcs[func_name](arg_val)
        except ValueError as ve:
            raise ValueError(f"Math domain error in {func_name}: {str(ve)}")
        except OverflowError:
            raise ValueError(f"Overflow error in {func_name}")

    def generic_visit(self, node):
        raise TypeError(f"Unsupported operation: {type(node).__name__}")
