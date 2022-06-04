import re


class Token:
    def __init__(self, lexeme_type, lexeme, line_num):
        self.lexeme_type = lexeme_type
        self.lexeme = lexeme
        self.line_num = line_num

    def get_type(self):
        return self.lexeme_type.lower()

    def get_lexeme(self):
        return self.lexeme

    def get_line_num(self):
        return str(self.line_num)


def check_lexemes(tmp_str, reg_dict):
    keys = reg_dict.keys()
    for word in keys:
        match_res = re.fullmatch(reg_dict[word], tmp_str)
        if match_res:
            return word
    return None


def lexer(file_name):
    f = open(file_name, "r")

    token_array = []
    reg_dict = {
        'DIGIT': r"^([0-9])|([1-9][0-9]*)$",
        'ASSIGN': r"^\=$",
        'OP': r"^[\-|\+|\*|\/][\=]?$",
        'COMP_OP': r"^[=]{2}|([>|<|][=]?)$",
        'WHILE': r"^while$",
        'FOR': r"^for$",
        'IF': r"^if$",
        'PRINT': r"^print$",
        'VAR': r"^[A-Za-z][0-9a-z_]*$",
        'STRING': r'^".*"?$',
        'SPACE': r"^\s$",
        'L_ROUND_BRACKET': r"^\($",
        'R_ROUND_BRACKET': r"^\)$",
        'L_SQUARE_BRACKET': r"^\[$",
        'R_SQUARE_BRACKET': r"^\]$",
        'L_BRACE': r"^{$",
        'R_BRACE': r"^}$",
        'SEMICOLON': r"^;$"
    }

    curr_line_num = 1
    for line in f:

        line = line.replace("\r", "")
        line = line.replace("\n", "")
        line += " "

        tmp_str = ""
        curr_type = ""
        prev_type = ""
        i = 0
        while i < len(line):
            tmp_str += line[i]
            curr_type = check_lexemes(tmp_str, reg_dict)
            if not curr_type and len(tmp_str) == 1:
                raise SyntaxError("in line " + str(curr_line_num))
            if curr_type == "SPACE":
                tmp_str = ""
                i += 1
                continue
            if not curr_type:
                prev_type = check_lexemes(tmp_str[:-1], reg_dict)
                if prev_type:
                    token_array.append(Token(prev_type, tmp_str[:-1], curr_line_num))
                    i -= 1
                    tmp_str = ""
                else:
                    raise SyntaxError("in line " + str(curr_line_num))
            i += 1
        if curr_type == 'STRING' and prev_type == 'STRING':
            raise SyntaxError("unfinished string in line " + str(curr_line_num))

        curr_line_num += 1
    return token_array
