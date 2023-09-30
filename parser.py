#Vy Nguyen & Sophie Tran
#Project Phase 2.2 Parser

from ast import AST

class Parser:
    def __init__(self, tokens):
        self.tokenId = 0
        self.tokens = tokens
        self.currentToken = tokens[0] if len(tokens) > 0 else None

    def parseTokens(self):
        return self.parseStatement()

    def parseStatement(self) -> AST:
        tree = self.parseBaseStatement()
        while self.currentToken and self.currentToken[0] == ';':
            token = self.currentToken
            self.consumeToken()
            tree = AST(token, tree, None, self.parseBaseStatement())
        return tree

    def parseBaseStatement(self):
        if self.currentToken and self.currentToken[0] == 'skip':
            token = self.currentToken
            self.consumeToken()
            return AST(token, None, None, None)
        elif self.currentToken and self.currentToken[0] == 'if':
            return self.parseIfStatement()
        elif self.currentToken and self.currentToken[0] == 'while':
            return self.parseWhileStatement()
        elif self.currentToken and self.currentToken[1] == 'IDENTIFIER':
            return self.parseAssignment()
        else:

            raise Exception('ERROR')

    def parseAssignment(self):
        if self.currentToken and self.currentToken[1] == 'IDENTIFIER':
            id = self.currentToken
            self.consumeToken()
            if self.currentToken and self.currentToken[1] == 'SYMBOL':
                symbol = self.currentToken
                self.consumeToken()
            else:
                raise Exception('ERROR')
            return AST(symbol, AST(id, None, None, None), None, self.parseExpression())
        else:
            raise Exception('ERROR')

    def parseIfStatement(self):
        if self.currentToken and self.currentToken[0] == 'if':
            self.consumeToken()
            expr = self.parseExpression()
            if self.currentToken and self.currentToken[0] == 'then':
                self.consumeToken()
                statement1 = self.parseStatement()
                if self.currentToken and self.currentToken[0] == 'else':
                    self.consumeToken()
                    statement2 = self.parseStatement()
                    if self.currentToken and self.currentToken[0] == 'endif':
                        self.consumeToken()
                    else:
                        raise Exception('ERROR')
                    return AST(('','IF-STATEMENT'), expr, statement1, statement2)
                else:
                    raise Exception('ERROR')
            else:
                raise Exception('ERROR')
        else:
            raise Exception('ERROR')

    def parseWhileStatement(self):
        if self.currentToken and self.currentToken[0] == 'while':
            self.consumeToken()
            expr = self.parseExpression()
            if self.currentToken and self.currentToken[0] == 'do':
                self.consumeToken()
                statement = self.parseStatement()
                if self.currentToken and self.currentToken[0] == 'endwhile':
                    self.consumeToken()
                else:
                    raise Exception('ERROR')
                return AST(('','WHILE-LOOP'), expr, None, statement)
            else:
                raise Exception('ERROR')
        else:
            raise Exception('ERROR')

    def parseExpression(self):
        tree = self.parseTerm()
        while self.currentToken and self.currentToken[0] == '+':
            token = self.currentToken
            self.consumeToken()
            tree = AST(token, tree, None, self.parseTerm())
        return tree

    def parseTerm(self):
        tree = self.parseFactor()
        while self.currentToken and self.currentToken[0] == '-':
            token = self.currentToken
            self.consumeToken()
            tree = AST(token, tree, None, self.parseFactor())
        return tree

    def parseFactor(self):
        tree = self.parsePiece()
        while self.currentToken and self.currentToken[0] == '/':
            token = self.currentToken
            self.consumeToken()
            tree = AST(token, tree, None, self.parsePiece())
        return tree

    def parsePiece(self):
        tree = self.parseElement()
        while self.currentToken and self.currentToken[0] == '*':
            token = self.currentToken
            self.consumeToken()
            tree = AST(token, tree, None, self.parseElement())
        return tree

    def parseElement(self):
        if self.currentToken and self.currentToken[0] == '(':
            self.consumeToken()
            tree = self.parseExpression()
            if not self.currentToken or self.currentToken[0] != ')':
                raise Exception('Missing parenthesis')
            self.consumeToken()
            return tree
        elif self.currentToken and self.currentToken[1] == 'NUMBER':
            token = self.currentToken
            self.consumeToken()
            return AST(token, None, None, None)
        elif self.currentToken and self.currentToken[1] == 'IDENTIFIER':
            token = self.currentToken
            self.consumeToken()
            return AST(token, None, None, None)
        else:
            raise Exception('ERROR')

    def consumeToken(self):
        self.tokenId += 1
        self.currentToken = None if self.tokenId >= len(self.tokens) else self.tokens[self.tokenId]

    def rec(self, ast, indent):
        if ast is None:
            return
        indentPrefix = indent * '\t'
        print(f"{indentPrefix}{ast.token[1]} {ast.token[0]}")
        self.rec(ast.leftChild, indent + 1)
        self.rec(ast.middleChild, indent + 1)
        self.rec(ast.rightChild, indent + 1)

    def printAST(self, ast):
        self.rec(ast, 0)