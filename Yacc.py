from sly import Parser
import sly
from Lex import CalcLexer  

class CalcParser(Parser):

    tokens = CalcLexer.tokens

    precedence = (

        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),

    )

    def __init__(self):
        self.names = { }

    ############################## Grammar rules and actions ##############################

    #STATEMENT : ASSIGNMENT

    #STATEMENT : EXPRESSION

    @_("ASSIGNMENT")
    def STATEMENT(self, production):
        if(production.ASSIGNMENT):
            print(production.ASSIGNMENT)
        return

    @_("EXPRESSION")
    def STATEMENT(self, production):
        print(production.EXPRESSION)
        return

    #######################################################################################
    
    #ASSIGNMENT : ID = EXPRESSION

    @_("ID ASSIGN EXPRESSION")
    def ASSIGNMENT(self, production):
        self.names[production.ID] = production.EXPRESSION

    #######################################################################################

    #EXPRESSION : EXPRESSION + ID
    @_("EXPRESSION PLUS ID")
    def EXPRESSION(self, production):
        try:
            return production.EXPRESSION + self.names[production.ID]
        except LookupError:
            print(f'Undefined name {production.ID!r}')

    #EXPRESSION : EXPRESSION + NUMBER
    @_("EXPRESSION PLUS NUMBER")
    def EXPRESSION(self, production):
        return production.EXPRESSION + production.NUMBER

    #EXPRESSION : NUMBER
    @_("NUMBER")
    def EXPRESSION(self, production):
        return production.NUMBER

    #EXPRESSION : ID
    @_("ID")
    def EXPRESSION(self, production):
        try:
            return self.names[production.ID]
        except LookupError:
            print(f'Undefined name {production.ID!r}')
    
    #######################################################################################

    