class StatementsNode:
    def __init__(self):
        self.lines = []

    def add(self, line):
        self.lines.append(line)

    def print(self):
        for line in self.lines:
            line.print()

    def getLines(self):
        return self.lines


class VariableNode:
    def __init__(self, variable):
        self.variable = variable

    def getValue(self):
        return self.variable

    def print(self):
        print(self.variable)


class OperatorNode:
    def __init__(self, operator):
        self.operator = operator

    def getValue(self):
        return self.operator

    def print(self):
        print(self.operator)


class PrintNode:
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def print(self):
        self.value.print()


class NumberNode:
    def __init__(self, number):
        self.number = number

    def getValue(self):
        return self.number

    def print(self):
        print(self.number)


class AssignNode:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def getVariable(self):
        return self.variable.getValue()

    def getValue(self):
        return self.value

    def print(self):
        self.variable.print()
        self.value.print()


class BinOperationNode:
    def __init__(self, operator, leftNode, rightNode):
        self.operator = operator
        self.leftNode = leftNode
        self.rightNode = rightNode

    def getOperator(self):
        return self.operator.getValue()

    def getLeftNode(self):
        return self.leftNode

    def getRightNode(self):
        return self.rightNode

    def print(self):
        self.leftNode.print()
        self.operator.print()
        self.rightNode.print()


class If:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def getCondition(self):
        return self.condition

    def getBody(self):
        return self.body

    def print(self):
        self.condition.print()
        self.body.print()


class WhileCycle:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def getCondition(self):
        return self.condition

    def getBody(self):
        return self.body

    def print(self):
        self.condition.print()
        self.body.print()


class ForCycle:
    def __init__(self, forCondition, body):
        self.forCondition = forCondition
        self.body = body

    def print(self):
        self.forCondition.print()
        self.body.print()


class ForCondition:
    def __init__(self, initialization, condition, counterUpdate):
        self.initialization = initialization
        self.condition = condition
        self.counterUpdate = counterUpdate

    def print(self):
        self.initialization.print()
        self.condition.print()
        self.counterUpdate.print()
