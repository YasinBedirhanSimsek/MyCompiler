from sly import Parser
import sly
from Lex import CalcLexer  

class CalcParser(Parser):

    tokens = CalcLexer.tokens

    precedence = (
       ('left', EQUALS),
       ('left', PLUS, MINUS),
       ('left', TIMES, DIVIDE),
       ('right', UMINUS),
    )

    def __init__(self):
        self.names = { }

    ############################## Grammar rules and actions ##############################

    #STATEMENT : ASSIGNMENT

    #STATEMENT : EXPRESSION

    #STATEMENT : LOOP

    #STATEMENT : CONDITIONAL

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


    ##########################################################################################
    
    # ------------------> EXPRESSION : EXPRESSION ** EXPRESSION   <------------------
    @_('EXPRESSION EXPONENT EXPRESSION')
    def EXPRESSION(self, production):
        return production.EXPRESSION0 ** production.EXPRESSION1

    #EXPRESSION : EXPRESSION + EXPRESSION
    @_("EXPRESSION PLUS EXPRESSION")
    def EXPRESSION(self, production):
        return production.EXPRESSION0 + production.EXPRESSION1

    #EXPRESSION : EXPRESSION - EXPRESSION
    @_("EXPRESSION MINUS EXPRESSION")
    def EXPRESSION(self, production):
        return production.EXPRESSION0 - production.EXPRESSION1

    #EXPRESSION : EXPRESSION * EXPRESSION   
    @_("EXPRESSION TIMES EXPRESSION")
    def EXPRESSION(self, production):
        return (production.EXPRESSION0 * production.EXPRESSION1)

    #EXPRESSION : EXPRESSION / EXPRESSION   
    @_("EXPRESSION DIVIDE EXPRESSION")
    def EXPRESSION(self, production):
        return (production.EXPRESSION0 / production.EXPRESSION1)
    
    # ------------------> EXPRESSION : EXPRESSION % EXPRESSION   <------------------
    @_('EXPRESSION MOD EXPRESSION')
    def EXPRESSION(self, production):
        return production.EXPRESSION0 % production.EXPRESSION1
    
    # ------------------> EXPRESSION : EXPRESSION == EXPRESSION    <-----------------
    @_('EXPRESSION EQUALS EXPRESSION')
    def EXPRESSION(self, production):
        return production.EXPRESSION0 == production.EXPRESSION1

    #EXPRESSION : -EXPRESSION 
    @_('MINUS EXPRESSION %prec UMINUS')
    def EXPRESSION(self, production):
        return -production.EXPRESSION

    #EXPRESSION : NUMBER
    @_("NUMBER")
    def EXPRESSION(self, production):
        return production.NUMBER

    #EXPRESSION : ( EXPRESSION )
    @_('LPAREN EXPRESSION RPAREN')
    def EXPRESSION(self, production):
        return production.EXPRESSION

    #EXPRESSION : ID
    @_("ID")
    def EXPRESSION(self, production):
        try:
            return self.names[production.ID]
        except LookupError:
            print(f'Undefined name {production.ID!r}')

    #######################################################################################

    