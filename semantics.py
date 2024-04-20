from CCparse import parser
from CClex import reserved_word
import requests
from lark import Transformer, v_args, Token, Tree


class SemanticError(Exception):
    def __init__(self, message, token=None):
        self.message = message
        self.line = token.line if token else None
        self.column = token.column if token else None
        super().__init__(self.message)

    def __str__(self):
        return f"Semantic Error at line {self.line}, column {self.column}: {self.message}"

class SemanticAnalyzer(Transformer):
    def __init__(self):
        super().__init__()
        self.contracts = {}
        self.functions = {}
        self.current_scope = None
        self.scope_stack = []
        self.reserved_keywords = set(reserved_word.keys())
        self.symbol_table = {}
        self.errors = []

    @v_args(inline=True)
    def check_contract(self, name, token):
        if name in self.contracts:
            self._add_error(f"Contract '{name}' is already defined, redeclaration!", token)
        else:
            self.contracts[name] = self.current_scope
            self.scope_stack.append(name)
        return name

    @v_args(inline=True)
    def check_function(self, name, token):
        if name in self.functions:
            self._add_error(f"Function '{name}' redeclaration", token)
        else:
            self.functions[name] = self.current_scope
            self.scope_stack.append(name)
        return name

    def check_variable(self, name: str, token: Token):
        if not self.current_scope:
            self._add_error(f"Undefined variable '{name}'", token)
            return False
        elif name not in self.current_scope:
            self._add_error(f"Variable is inaccessible '{name}' in current scope '{self.current_scope}'", token)
            return False
        return True

    def function_exist(self, name: str, token: Token):
        if name not in self.functions:
            self._add_error(f"Undefined function '{name}'", token)
            return False
        return True

    def check_reserved_keyword(self, name: str, token: Token):
        if name in self.reserved_keywords:
            self._add_error(f"'{name}' is a reserved keyword and cannot be used as an identifier", token)
            return False
        return True

    def add_symbol(self, name, _type, token: Token):
        self.symbol_table[name] = {"type:", _type, "token", token}

    def check_assignment(self, l_expr, r_expr):
        l_expr_type = self.symbol_table[l_expr]["type"]
        r_expr_type = self.symbol_table[r_expr]["type"]
        if l_expr_type == r_expr_type:
            return True
        else:
            self._add_error(f"Cannot assign {l_expr_type} expression to {r_expr_type} variable {l_expr}")
            return False

    def _add_error(self, message, token=None):
        self.errors.append(SemanticError(message, token))

    def get_errors(self):
        return self.errors


class ASTSimplifier(Transformer):
    def if_statement(self, args):
        condition, then_block = args[0], args[1]
        else_block = args[2] if len(args) > 2 else None
        children = [self.flatten_expression(condition), Tree('then', [then_block])]
        if else_block:
            children.append(Tree('else', [else_block]))
        return Tree('if_statement', children)

    @staticmethod
    def display(args):
        return Tree('display', args)

    @staticmethod
    def block(args):
        if len(args) == 1:
            return args[0]
        return Tree('block', args)

    @staticmethod
    def type_specifier(args):
        return Tree('type_specifier', args)

    def term(self, args):
        if len(args) == 1:
            return self.flatten_expression(args[0])
        else:
            flattened_args = [self.flatten_expression(arg) for arg in args]
            return Tree('expression', flattened_args)

    def flatten_expression(self, tree):
        if tree.data in ['term', 'factor'] and len(tree.children) == 1:
            return self.flatten_expression(tree.children[0])
        else:
            return Tree(tree.data, [self.flatten_expression(child) if isinstance(child, Tree) else child for child in
                                    tree.children])


def analyze(ast):
    analyzer = SemanticAnalyzer()
    analyzer.transform(ast)
    return analyzer
