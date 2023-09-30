#Vy Nguyen & Sophie Tran
#Project Phase 3.2 Evaluator

from ast import AST

class Evaluator:
    def __init__(self, ast):
        self.ast = ast
        #Empty dictionary
        self.memory = {}

    def evaluate(self, ast):
        self.evaluateStatement(ast)
        return self.memory

    def evaluateStatement(self, ast):
        if ast.token[0] == ';':
            self.evaluateStatement(ast.leftChild)
            self.evaluateStatement(ast.rightChild)
        elif ast.token[0] == ':=':
            self.evaluateAssignment(ast)
        elif ast.token[0] == 'skip':
            return
        elif ast.token[1] == 'IF-STATEMENT':
            self.evaluateIfStatement(ast)
        elif ast.token[1] == 'WHILE-LOOP':
            self.evaluateWhileStatement(ast)
        else:
            raise Exception('Error evaluating token')

    def evaluateAssignment(self, ast):
        #self.VARIABLE_NAME_TO_VALUE_MAPPING[VARIABLE_NAME]
        value = self.evaluateExpression(ast.rightChild)
        #RESULT_OF_EXPRESSION
        key = ast.leftChild.token[0]
        self.memory[key] = value

    def evaluateIfStatement(self, ast):
        expr = self.evaluateExpression(ast.leftChild)
        if expr != 0:
            self.evaluateStatement(ast.middleChild)
        else:
            self.evaluateStatement(ast.rightChild)

    def evaluateWhileStatement(self, ast):
        while self.evaluateExpression(ast.leftChild) != 0:
            self.evaluateStatement(ast.rightChild)

    def evaluateExpression(self, ast):
        #Tree only has a NUMBER
        if ast.token[1] == 'NUMBER':
            return int(ast.token[0])
        #Tree starts with an IDENTIFIER
        if ast.token[1] == 'IDENTIFIER':
            if ast.token[0] not in self.memory:
                raise Exception('Error evaluating tree')
            return self.memory[ast.token[0]]
        #Tree starts with a SYMBOL
        if ast.token[1] == 'SYMBOL':
            left = self.evaluateExpression(ast.leftChild)
            right = self.evaluateExpression(ast.rightChild)
            if ast.token[0] == '+':
                return left + right
            elif ast.token[0] == '-':
                return max(left - right, 0)
            elif ast.token[0] == '*':
                return left * right
            elif ast.token[0] == '/':
                if right == 0:
                    raise Exception('Cannot divide by 0')
                return left // right
            else:
                raise Exception('Invalid symbol')
        else:
            raise Exception('Error evaluating tree')






