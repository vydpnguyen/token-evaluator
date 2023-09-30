#Vy Nguyen & Sophie Tran

import sys
from scanner import scan
from parser import Parser
from ast import AST
import argparse
from evaluator import Evaluator

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, type=argparse.FileType('r'))
parser.add_argument('--output', nargs='?', type=argparse.FileType('w'))
args = parser.parse_args()

'''
try:
    lines = [x.rstrip() for x in open('input.txt', 'r').readlines()]
except:
    print('FAILED TO OPEN INPUT FILE!')
'''

def rec(ast, indent):
    if ast is None:
        return
    indentPrefix = indent * '\t'
    #print(f"{indentPrefix}{ast.token[1]} {ast.token[0]}")
    args.output.write(f"{indentPrefix}{ast.token[1]} {ast.token[0]}\n")
    rec(ast.leftChild, indent + 1)
    rec(ast.middleChild, indent + 1)
    rec(ast.rightChild, indent + 1)

def printASTToFile(ast):
    rec(ast, 0)

def main():
    try:
        tokens = scan(args.input)
        args.output.write('Tokens:')
        for token in tokens:
            #print(f'{token[1]} {token[0]}')
            args.output.write(f'\n{token[1]} {token[0]}')
    except Exception as ex:
        args.output.write(ex.args[0])
        sys.exit()

    parser = Parser(tokens)
    args.output.write('\n\nAST:\n')

    try:
        astree = parser.parseTokens()
        printASTToFile(astree)
    except Exception as ex:
        args.output.write(ex.args[0])
        sys.exit()

    eval = Evaluator(astree)
    args.output.write('\nOutput:')
    try:
        dict = eval.evaluate(astree)
        for keys, values in dict.items():
            args.output.write(f'\n{keys} = {values}')

    except Exception as ex:
        args.output.write(ex.args[0])
        sys.exit()

main()