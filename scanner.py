# Vy Nguyen & Sophie Tran
# Project Phase 1.2 Scanner

import re

def scan(lines):
    identifier = re.compile('([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*')
    number = re.compile('[0-9]+')
    symbol = re.compile('(\+|\-|\*|/|\(|\)|:=|;)')
    keyword = re.compile('if|then|else|endif|while|do|endwhile|skip')

    token_list = []

    for line in lines:
        tokens = line.split()
        br = False
        for token in tokens:
            if br:
                break
            while token:
                if re.fullmatch(keyword, token):
                    cat = 'KEYWORD'
                    token_list.append((token, cat))
                    token = ''
                elif re.fullmatch(identifier, token):
                    cat = 'IDENTIFIER'
                    token_list.append((token, cat))
                    token = ''
                elif re.fullmatch(number, token):
                    cat = 'NUMBER'
                    token_list.append((token, cat))
                    token = ''
                elif re.fullmatch(symbol, token):
                    cat = 'SYMBOL'
                    token_list.append((token, cat))
                    token = ''
                else:
                    id_part = re.match(identifier, token)
                    num_part = re.match(number, token)
                    sym_part = re.match(':=', token)
                    if not sym_part:
                        sym_part = re.match(symbol, token)
                    if num_part:
                        mini, maxi = num_part.span()
                        partial_token = token[mini:maxi]
                        token_list.append((partial_token, 'NUMBER'))
                        token = token[maxi:len(token)]

                    elif id_part:
                        mini, maxi = id_part.span()
                        partial_token = token[mini:maxi]
                        if re.fullmatch(keyword, partial_token):
                            token_list.append((partial_token, 'KEYWORD'))
                        else:
                            token_list.append((partial_token, 'IDENTIFIER'))
                        token = token[maxi:len(token)]

                    elif sym_part:
                        mini, maxi = sym_part.span()
                        partial_token = token[mini:maxi]
                        token_list.append((partial_token, 'SYMBOL'))
                        token = token[maxi:len(token)]
                    else:
                        if token != '':
                            #print(f'ERROR READING "{token}"')
                            raise Exception(f'ERROR READING "{token}"')
                        br = True
                        break

    return token_list