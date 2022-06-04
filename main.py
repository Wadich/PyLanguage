from lexer import lexer
from myParser import parser
from parseAST import parse, run

token_array = lexer("cmd.txt")
i = 0
for token in token_array:
    print(i, token.get_type(), token.get_lexeme())
    i += 1

root = parse(token_array)
run(root)
