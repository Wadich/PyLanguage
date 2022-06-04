from ATS import StatementsNode, NumberNode, VariableNode, OperatorNode, BinOperationNode, AssignNode, If, WhileCycle, \
    ForCondition, ForCycle, PrintNode

index = 0

variableDict = {}


def parse(token_array):
    root = StatementsNode()
    while index < len(token_array) - 1:
        codeStringNode = parseExpression(token_array)
        root.add(codeStringNode)
    return root


def parseExpression(token_array):
    assignNode = parseAssign(token_array)

    if assignNode:
        return assignNode

    ifNode = parseIf(token_array)

    if ifNode:
        return ifNode

    whileNode = parseWhile(token_array)

    if whileNode:
        return whileNode

    forNode = parseFor(token_array)

    if forNode:
        return forNode

    printNode = parsePrint(token_array)

    if printNode:
        return printNode


def parseVarOrNum(token_array):
    token_type = token_array[index].get_type()
    lexeme = token_array[index].get_lexeme()
    if token_type != "var":
        if token_type != "digit":
            return None
        else:
            return NumberNode(int(lexeme))
    else:

        return VariableNode(lexeme)


def parseOperator(token_array):
    token_type = token_array[index].get_type()
    lexeme = token_array[index].get_lexeme()
    if token_type == "op" or token_type == "comp_op":
        return OperatorNode(lexeme)
    return None


def parseParentheses(token_array):
    if token_array[index].get_type() == "l_round_bracket":
        step(token_array)
        node = parseFormula(token_array)
        if token_array[index].get_type() != "r_round_bracket":
            raise SyntaxError(f"Unfinished line in line {token_array[index].get_line_num()}")
        return node
    else:
        return parseVarOrNum(token_array)


def parseFormula(token_array):
    leftNode = parseParentheses(token_array)

    if not leftNode:
        raise SyntaxError(f"Expected left operand, but got none; line {token_array[index].get_line_num()}")

    step(token_array)
    operator = parseOperator(token_array)

    if not operator and index < len(token_array) - 1:
        return leftNode

    if not operator:
        step(token_array, True)
        return leftNode

    step(token_array)

    while operator:
        rightNode = parseParentheses(token_array)
        step(token_array)
        leftNode = BinOperationNode(operator, leftNode, rightNode)
        operator = parseOperator(token_array)
        if operator:
            step(token_array)

    return leftNode


def parseCondition(token_array):
    leftNode = parseVarOrNum(token_array)

    if not leftNode:
        raise SyntaxError(f"Expected left operand, but got none; line {token_array[index].get_line_num()}")

    step(token_array)
    operator = parseOperator(token_array)

    if not operator:
        raise SyntaxError(f"Expected operator, but got none; line {token_array[index].get_line_num()}")

    step(token_array)

    rightNode = parseVarOrNum(token_array)

    if not rightNode:
        raise SyntaxError(f"Expected right operand, but got none; line {token_array[index].get_line_num()}")

    step(token_array)

    return BinOperationNode(operator, leftNode, rightNode)


def parseAssign(token_array):
    varNode = parseVarOrNum(token_array)

    if not varNode:
        return None

    if type(varNode) == NumberNode:
        raise TypeError(f"Expected variable, but got number in line {token_array[index].get_line_num()}.")

    if not varNode:
        return None

    step(token_array)

    if token_array[index].get_type() != "assign":
        raise TypeError(f"Expected assign operator, but got {token_array[index].get_type()} "
                        f"in line {token_array[index].get_line_num()}.")

    step(token_array)
    value = parseFormula(token_array)

    return AssignNode(varNode, value)


def parseIf(token_array):
    if token_array[index].get_type() != "if":
        return None

    step(token_array)

    if token_array[index].get_type() != "l_round_bracket":
        raise SyntaxError(f"Expected '(', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)

    conditionNode = parseFormula(token_array)

    if token_array[index].get_type() != "r_round_bracket":
        raise SyntaxError(f"Expected ')', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)

    if token_array[index].get_type() != "l_brace":
        raise SyntaxError("Expected '{'" + f", but got {token_array[index].get_type()} "
                                           f"in line {token_array[index].get_line_num()}")

    step(token_array)

    bodyNode = parseExpression(token_array)

    if not bodyNode:
        raise SyntaxError(f"Empty 'if' construction body in line {token_array[index].get_line_num()}")

    step(token_array)

    if token_array[index].get_type() != "r_brace":
        raise SyntaxError("Expected '}'" + f", but got {token_array[index].get_type()} "
                                           f"in line {token_array[index].get_line_num()}")

    step(token_array)

    return If(conditionNode, bodyNode)


def parseWhile(token_array):
    if token_array[index].get_type() != "while":
        return None

    step(token_array)

    if token_array[index].get_type() != "l_round_bracket":
        raise SyntaxError(f"Expected '(', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)

    conditionNode = parseFormula(token_array)

    if token_array[index].get_type() != "r_round_bracket":
        raise SyntaxError(f"Expected ')', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)

    if token_array[index].get_type() != "l_brace":
        raise SyntaxError("Expected '{'" + f", but got {token_array[index].get_type()} "
                                           f"in line {token_array[index].get_line_num()}")

    step(token_array)

    bodyNode = parseExpression(token_array)

    if not bodyNode:
        raise SyntaxError(f"Empty 'while' construction body in line {token_array[index].get_line_num()}")

    if token_array[index].get_type() != "r_brace":
        raise SyntaxError("Expected '}'" + f", but got {token_array[index].get_type()} "
                                           f"in line {token_array[index].get_line_num()}")

    step(token_array)

    return WhileCycle(conditionNode, bodyNode)


def parseForCondition(token_array):
    initNode = parseAssign(token_array)

    if token_array[index].get_type() != "semicolon":
        raise SyntaxError(f"Expected ';', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)
    conditionNode = parseCondition(token_array)

    if token_array[index].get_type() != "semicolon":
        raise SyntaxError(f"Expected ';', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)
    counterUpdateNode = parseAssign(token_array)
    step(token_array, True)

    return ForCondition(initNode, conditionNode, counterUpdateNode)


def parseFor(token_array):
    if token_array[index].get_type() != "for":
        return None

    step(token_array)

    if token_array[index].get_type() != "l_round_bracket":
        raise SyntaxError(f"Expected '(', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)

    forConditionNode = parseForCondition(token_array)

    if token_array[index].get_type() != "r_round_bracket":
        raise SyntaxError(f"Expected ')', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)

    if token_array[index].get_type() != "l_brace":
        raise SyntaxError("Expected '{'" + f", but got {token_array[index].get_type()} "
                                           f"in line {token_array[index].get_line_num()}")

    step(token_array)

    bodyNode = parseExpression(token_array)

    if not bodyNode:
        raise SyntaxError(f"Empty 'for' construction body in line {token_array[index].get_line_num()}")

    step(token_array)

    if token_array[index].get_type() != "r_brace":
        raise SyntaxError("Expected '}'" + f", but got {token_array[index].get_type()} "
                                           f"in line {token_array[index].get_line_num()}")

    step(token_array)

    return ForCycle(forConditionNode, bodyNode)


def parsePrint(token_array):
    if token_array[index].get_type() != "print":
        return None

    step(token_array)

    if token_array[index].get_type() != "l_round_bracket":
        raise SyntaxError(f"Expected '(', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)

    valueNode = parseVarOrNum(token_array)

    step(token_array)

    if token_array[index].get_type() != "r_round_bracket":
        raise SyntaxError(f"Expected ')', but got {token_array[index].get_type()} "
                          f"in line {token_array[index].get_line_num()}")

    step(token_array)

    return PrintNode(valueNode)


def step(token_array, reversed=False):
    global index
    if index + 1 > len(token_array):
        raise IndexError()
    if index + 1 < len(token_array) and not reversed:
        index += 1
    elif index + 1 < len(token_array) and reversed:
        index -= 1


def run(node):
    if type(node) == NumberNode:
        return int(node.getValue())

    if type(node) == BinOperationNode:
        if node.getOperator() == "+":
            leftNode = run(node.getLeftNode())
            if type(leftNode) == str:
                leftNodeValue = variableDict.get(leftNode)
            else:
                leftNodeValue = leftNode
            rightNode = run(node.getRightNode())
            if type(rightNode) == str:
                rightNodeValue = variableDict.get(rightNode)
            else:
                rightNodeValue = rightNode

            return leftNodeValue + rightNodeValue

        if node.getOperator() == "-":
            leftNode = run(node.getLeftNode())
            if type(leftNode) == str:
                leftNodeValue = variableDict.get(leftNode)
            else:
                leftNodeValue = leftNode
            rightNode = run(node.getRightNode())
            if type(rightNode) == str:
                rightNodeValue = variableDict.get(rightNode)
            else:
                rightNodeValue = rightNode

            return leftNodeValue - rightNodeValue

        if node.getOperator() == "*":
            leftNode = run(node.getLeftNode())
            if type(leftNode) == str:
                leftNodeValue = variableDict.get(leftNode)
            else:
                leftNodeValue = leftNode
            rightNode = run(node.getRightNode())
            if type(rightNode) == str:
                rightNodeValue = variableDict.get(rightNode)
            else:
                rightNodeValue = rightNode

            return leftNodeValue * rightNodeValue

        if node.getOperator() == "/":
            leftNode = run(node.getLeftNode())
            if type(leftNode) == str:
                leftNodeValue = variableDict.get(leftNode)
            else:
                leftNodeValue = leftNode
            rightNode = run(node.getRightNode())
            if type(rightNode) == str:
                rightNodeValue = variableDict.get(rightNode)
            else:
                rightNodeValue = rightNode

            return leftNodeValue / rightNodeValue

        if node.getOperator() == ">" or node.getOperator() == ">=" \
                or node.getOperator() == "<" or node.getOperator() == "<=" \
                or node.getOperator() == "==":
            return run(node.getLeftNode()), node.getOperator(), run(node.getRightNode())

    if type(node) == AssignNode:
        result = run(node.getValue())
        variable = node.getVariable()
        variableDict.update({variable: result})
        return result

    if type(node) == VariableNode:
        if node.getValue() in variableDict.keys():
            return node.getValue()
        raise ValueError(f"Variable '{node.getVariable()}' is not declared in this scope")

    if type(node) == StatementsNode:
        for line in node.getLines():
            run(line)

        return

    if type(node) == PrintNode:
        if type(node.getValue()) == VariableNode:
            variable = run(node.getValue())
            value = variableDict.get(variable)
            print(value)
            return

        if type(node.getValue()) == NumberNode:
            value = run(node.getValue())
            print(value)
            return

    if type(node) == If:
        varCondition, operator, rightNode = run(node.getCondition())

        value = variableDict.get(varCondition)

        if type(rightNode) != int:
            if rightNode not in variableDict.keys():
                raise ValueError(f"Variable '{rightNode}' is not declared in this scope")
            rightNode = variableDict.get(rightNode)

        if operator == ">":
            if value > rightNode:
                run(node.getBody())
            return

        if operator == ">=":
            if value >= rightNode:
                run(node.getBody())
            return

        if operator == "==":
            if value == rightNode:
                run(node.getBody())
            return

        if operator == "<":
            if value < rightNode:
                run(node.getBody())
            return

        if operator == "<=":
            if value <= rightNode:
                run(node.getBody())
            return

    if type(node) == WhileCycle:
        varCondition, operator, rightNode = run(node.getCondition())

        value = variableDict.get(varCondition)

        if type(rightNode) != int:
            if rightNode not in variableDict.keys():
                raise ValueError(f"Variable '{rightNode}' is not declared in this scope")
            rightNode = variableDict.get(rightNode)

        if operator == ">" or operator == ">=":
            while value >= rightNode:
                if operator == ">" and value == rightNode:
                    break
                run(node.getBody())
                value = variableDict.get(varCondition)
            return

        if operator == "<" or operator == "<=":
            while value <= rightNode:
                if operator == "<" and value == rightNode:
                    break
                run(node.getBody())
                value = variableDict.get(varCondition)
            return

        if operator == "==":
            while value == rightNode:
                run(node.getBody())
                value = variableDict.get(varCondition)
            return
    raise TypeError("Error")
