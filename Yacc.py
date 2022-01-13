
from sly import Parser
from Lex import CalcLexer  

class CalcParser(Parser):

    debugfile = 'parser.out'

    tokens = CalcLexer.tokens

    precedence = (
       ('left', OR),
       ('left', AND),
       ('left', BITWISE_AND),
       ('left', BITWISE_OR),
       ('left', LESS_THAN, LESS_THAN_EQ, GREATER_THAN, GREATER_THAN_EQ, IS_NOT_EQUAL, IS_EQUAL),
       ('left', PLUS, MINUS),
       ('left', DIVIDE, TIMES, MOD),
       ('right', UMINUS),
       ("right", EXPONENT),     
    )

    def __init__(self):
        self.allIDs = []
        self.variables = { }
        self.functions = { }

        self.local_func_names = None
        self.allIDs_local_var_inc = 0

    ############################## Grammar rules and actions ##############################

    #STATEMENT : ASSIGNMENT

    #STATEMENT : EXPRESSION

    #STATEMENT : LOOP

    #STATEMENT : CONDITIONAL

    #STATEMENT : FUNCTIONAL

    @_('STATEMENT STATEMENT_LIST')
    def STATEMENT_LIST(self, production):
        return ('NODE_STATEMENT_LIST', production.STATEMENT, production.STATEMENT_LIST)

    @_('STATEMENT')
    def STATEMENT_LIST(self, production):
        return ('NODE_STATEMENT_LIST', production.STATEMENT)

    @_('ASSIGNMENT')
    def STATEMENT(self, production):
        if not production.ASSIGNMENT[1] in self.allIDs:
            self.allIDs.append(production.ASSIGNMENT[1])
        return ('NODE_STATEMENT', production.ASSIGNMENT)

    @_('EXPRESSION SEMI_COL')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.EXPRESSION)

    @_('LOOP', 'LOOP SEMI_COL')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.LOOP) 

    @_('CONDITIONAL', 'CONDITIONAL SEMI_COL')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.CONDITIONAL) 

    @_('FUNCTIONAL')
    def STATEMENT(self, production):
        return ('NODE_STATEMENT', production.FUNCTIONAL) 

    ####################################################################################### 
     
    #ASSIGNMENT : ID = EXPRESSION ;
    @_('ID ASSIGN EXPRESSION SEMI_COL')
    def ASSIGNMENT(self, production):
        return ('NODE_ASSIGNMENT', production.ID, production.EXPRESSION)
    
   #ASSIGNMENT : ID = EXPRESSION, ASSIGNMENT 
    @_("ID ASSIGN EXPRESSION COMMA ASSIGNMENT")
    def ASSIGNMENT(self, production):
        return ('NODE_ASSIGNMENT_EXP', production.ID, production.EXPRESSION, production.ASSIGNMENT)

    ########################################################################################## 

    @_('LOOP_BREAK SEMI_COL')
    def STATEMENT_LIST(self, production):
        return ('NODE_BREAK', production.LOOP_BREAK)

    #LOOP : WHILE ( BOOL_EXPRESSION ) { STATEMENT_LIST }
    @_('WHILE LPAREN BOOL_EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY')
    def LOOP(self, production):
        return ('NODE_WHILE', production.BOOL_EXPRESSION, production.STATEMENT_LIST)

    ##########################################################################################

    #CONDITIONAL : IF ( BOOL_EXPRESSION ) { STATEMENT_LIST }
    @_('IF LPAREN BOOL_EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL", production.BOOL_EXPRESSION, production.STATEMENT_LIST)

    #CONDITIONAL : IF ( BOOL_EXPRESSION ) { STATEMENT_LIST } ELSE { STATEMENT_LIST } 
    @_('IF LPAREN BOOL_EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY ELSE LCURLY STATEMENT_LIST RCURLY')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL_ELSE", production.BOOL_EXPRESSION, production.STATEMENT_LIST0, production.STATEMENT_LIST1)

    #CONDITIONAL : IF ( BOOL_EXPRESSION ) { STATEMENT_LIST } ELSE CONDITIONAL 
    @_('IF LPAREN BOOL_EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY ELSE CONDITIONAL')
    def CONDITIONAL(self, production):   
        return ("NODE_CONDITIONAL_ELSE_CONDITIONAL", production.BOOL_EXPRESSION, production.STATEMENT_LIST, production.CONDITIONAL)

    ##########################################################################################  

    #FUNCTION : FUNCTION_DEFINITION
    @_('FUNCTION_DEFINITION')
    def FUNCTIONAL(self, production):
        return ('NODE_FUNCTIONAL', production.FUNCTION_DEFINITION)

    #FUNCTION_DEFINITION : FUNCTION ID (PARAM_LIST) { STATEMENT_LIST } | FUNCTION ID (PARAM_LIST) { STATEMENT_LIST } ;
    @_('FUNCTION ID LPAREN PARAM_LIST RPAREN LCURLY STATEMENT_LIST RCURLY', 
       'FUNCTION ID LPAREN PARAM_LIST RPAREN LCURLY STATEMENT_LIST RCURLY SEMI_COL')  
    def FUNCTION_DEFINITION(self, production):

        param_dic = { } 

        node = production.STATEMENT_LIST

        if(production.PARAM_LIST):
            for k in production.PARAM_LIST:
                param_dic[k] = None

        while(True):

            if(node[1][1][0] == 'NODE_ASSIGNMENT'):
                self.allIDs_local_var_inc += 1

            if(len(node) > 2):
                node = node[2]
            else:
                break

        for i in range(self.allIDs_local_var_inc):
            self.allIDs.pop()

        if production.ID not in self.functions:
            self.functions[production.ID] = (production.ID, production.PARAM_LIST, production.STATEMENT_LIST, param_dic)

        return ('NODE_FUNCTION_DEFINITION', production.ID, production.PARAM_LIST, production.STATEMENT_LIST)

    #PARAM_LIST : EMPTY
    @_('EMPTY')
    def PARAM_LIST(self, production):
        self.allIDs_lenght = len(self.allIDs)
        return None

    #PARAM_LIST : ID
    @_('ID')
    def PARAM_LIST(self, production):
        if not production.ID in self.allIDs:
            self.allIDs.append(production.ID)
            self.allIDs_local_var_inc += 1
        return (production.ID,)
    
    #PARAM_LIST : ID, PARAM_LIST
    @_('ID COMMA PARAM_LIST')
    def PARAM_LIST(self, production):
        if not production.ID in self.allIDs:
            self.allIDs.append(production.ID)
            self.allIDs_local_var_inc += 1
        return (production.ID, *production.PARAM_LIST)

    #############################################  
    
    #FUNCTION : FUNCTION_CALL
    @_('FUNCTION_CALL')
    def FUNCTIONAL(self, production):
        return ('NODE_FUNCTIONAL', production.FUNCTION_CALL)

    #FUNCTION_CALL : ID (VALUE_LIST) ;
    @_('ID LPAREN VALUE_LIST RPAREN SEMI_COL')  
    def FUNCTION_CALL(self, production):
        
        if production.ID not in self.functions:
            print("Undefined Reference to " + production.ID + " at line " + str(production.lineno))

        foo = self.functions[production.ID]

        if(foo[1] and production.VALUE_LIST):
            if(len(production.VALUE_LIST) != len(foo[1])):
                print("Invalid paramater list to function " + production.ID + " at line " + str(production.lineno))  
        elif foo[1] and not production.VALUE_LIST:
            print("Invalid paramater list to function " + production.ID + " at line " + str(production.lineno))
        elif not foo[1] and production.VALUE_LIST:
            print("Invalid paramater list to function " + production.ID + " at line " + str(production.lineno))

        return ('NODE_FUNCTION_CALL', production.ID, production.VALUE_LIST)

    #VALUE_LIST : EMPTY
    @_('EMPTY')
    def VALUE_LIST(self, production):
        return None

    #VALUE_LIST : EXPRESSION
    @_('EXPRESSION')
    def VALUE_LIST(self, production):
        return (production.EXPRESSION,)

    #VALUE_LIST : EXPRESSION, VALUE_LIST
    @_('EXPRESSION COMMA VALUE_LIST')
    def VALUE_LIST(self, production):
        return (production.EXPRESSION, *production.VALUE_LIST)

    ########################################################################################## 

    #EXPRESSION : NUMBER
    @_('NUMBER')
    def EXPRESSION(self, production):
        return ('NODE_NUMBER', production.NUMBER)

    #EXPRESSION : ID 
    @_("ID")
    def EXPRESSION(self, production):
        if production.ID not in self.allIDs:
            print("Undefined Reference to " + production.ID + " at line " + str(production.lineno))
        return('NODE_ID', production.ID)

    #EXPRESSION : ( EXPRESSION )
    @_('LPAREN EXPRESSION RPAREN')
    def EXPRESSION(self, production):
        return ('NODE_LP_EXPRESSION_RP', production.EXPRESSION)

    #EXPRESSION : -EXPRESSION 
    @_('MINUS EXPRESSION %prec UMINUS')
    def EXPRESSION(self, production):
        return ('NODE_UMINUS', production.EXPRESSION)

    #EXPRESSION : EXPRESSION + EXPRESSION
    @_("EXPRESSION PLUS EXPRESSION")
    def EXPRESSION(self, production):
        return ('NODE_PLUS', production.EXPRESSION0, production.EXPRESSION1)

    #EXPRESSION : EXPRESSION - EXPRESSION
    @_("EXPRESSION MINUS EXPRESSION")
    def EXPRESSION(self, production):
        return ('NODE_MINUS', production.EXPRESSION0, production.EXPRESSION1)

    #EXPRESSION : EXPRESSION * EXPRESSION   
    @_("EXPRESSION TIMES EXPRESSION")
    def EXPRESSION(self, production):
        return ('NODE_TIMES', production.EXPRESSION0, production.EXPRESSION1)

    #EXPRESSION : EXPRESSION / EXPRESSION   
    @_("EXPRESSION DIVIDE EXPRESSION")
    def EXPRESSION(self, production):
        return ('NODE_DIVIDE', production.EXPRESSION0, production.EXPRESSION1)
    
    #EXPRESSION : EXPRESSION % EXPRESSION
    @_('EXPRESSION MOD EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_MOD', production.EXPRESSION0, production.EXPRESSION1)

    #EXPRESSION : EXPRESSION ** EXPRESSION
    @_('EXPRESSION EXPONENT EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_EXPONENT', production.EXPRESSION0, production.EXPRESSION1)  
    
    ##########################################################################################  

    #BOOL_EXPRESSION : ( BOOL_EXPRESSION )
    @_('LPAREN BOOL_EXPRESSION RPAREN')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_LP_BOOL_EXPRESSION_RP', production.BOOL_EXPRESSION)

    #BOOL_EXPRESSION : EXPRESSION == EXPRESSION
    @_('EXPRESSION IS_EQUAL EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_IS_EQUAL', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION != EXPRESSION
    @_('EXPRESSION IS_NOT_EQUAL EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_IS_NOT_EQUAL', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION >= EXPRESSION
    @_('EXPRESSION GREATER_THAN_EQ EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_GREATER_THAN_EQ', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION > EXPRESSION
    @_('EXPRESSION GREATER_THAN EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_GREATER_THAN', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION <= EXPRESSION
    @_('EXPRESSION LESS_THAN_EQ EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_LESS_THAN_EQ', production.EXPRESSION0, production.EXPRESSION1)

    #BOOL_EXPRESSION : EXPRESSION < EXPRESSION
    @_('EXPRESSION LESS_THAN EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_LESS_THAN', production.EXPRESSION0, production.EXPRESSION1)

    #######################################################################################

    #EXPRESSION : EXPRESSION & EXPRESSION
    @_('EXPRESSION BITWISE_AND EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_BITWISE_AND', production.EXPRESSION0, production.EXPRESSION1)
    
    #EXPRESSION : EXPRESSION | EXPRESSION
    @_('EXPRESSION BITWISE_OR EXPRESSION')
    def EXPRESSION(self, production):
        return ('NODE_BITWISE_OR', production.EXPRESSION0, production.EXPRESSION1)

    #######################################################################################

    #BOOL_EXPRESSION : BOOL_EXPRESSION and BOOL_EXPRESSION
    @_('BOOL_EXPRESSION AND BOOL_EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_AND', production.BOOL_EXPRESSION0, production.BOOL_EXPRESSION1)
    
    #BOOL_EXPRESSION : BOOL_EXPRESSION or BOOL_EXPRESSION
    @_('BOOL_EXPRESSION OR BOOL_EXPRESSION')
    def BOOL_EXPRESSION(self, production):
        return ('NODE_OR', production.BOOL_EXPRESSION0, production.BOOL_EXPRESSION1)

    #######################################################################################

    @_('')
    def EMPTY(self, production):
        pass

    #######################################################################################

    def eval_ast(self, ast):

        if(ast == None):
            return

        #############################################

        elif(ast[0] == 'NODE_STATEMENT_LIST'):
            if(len(ast) > 2):
                return self.eval_ast(ast[1]), self.eval_ast(ast[2])
            else:
                return self.eval_ast(ast[1])

        elif(ast[0] == 'NODE_STATEMENT'):
            return self.eval_ast(ast[1])

        #############################################

        elif(ast[0] == 'NODE_ASSIGNMENT'):

            evaled_exp = self.eval_ast(ast[2]) 

            if(self.local_func_names == None):
                if(ast[1] in self.variables):
                    self.variables[ast[1]] = evaled_exp
                    print("Global Variable "+ast[1] + " = " + str(evaled_exp))
                else:
                    self.variables[ast[1]] = evaled_exp
                    print("New Global Variable "+ast[1] + " = " + str(evaled_exp))

                return self.variables[ast[1]]

            else:
                #If There is a local variable
                if ast[1] in self.local_func_names:
                    self.local_func_names[ast[1]] = evaled_exp
                    print("Local Variable "+ast[1] + " = " + str(evaled_exp))
                    return self.local_func_names[ast[1]]
                #There was no local variable, check globals
                elif ast[1] in self.variables:
                    self.variables[ast[1]] = evaled_exp
                    print("Global Variable " + ast[1] + " = " + str(evaled_exp))
                    return self.variables[ast[1]]
                #There was no id so create one in local variables
                else:
                    self.local_func_names[ast[1]] = evaled_exp
                    print("New Local Variable "+ast[1] + " = " + str(evaled_exp))
                    return self.local_func_names[ast[1]]

        elif(ast[0] == 'NODE_ASSIGNMENT_EXP'): 

            evaled_exp = self.eval_ast(ast[2]) 

            if(self.local_func_names == None):
                if(ast[1] in self.variables):
                    self.variables[ast[1]] = evaled_exp
                    print("Global Variable "+ast[1] + " = " + str(evaled_exp))
                else:
                    self.variables[ast[1]] = evaled_exp
                    print("New Global Variable "+ast[1] + " = " + str(evaled_exp))
                return self.variables[ast[1]], self.eval_ast(ast[3]) 
        
            else:
                #If There is a local variable
                if ast[1] in self.local_func_names:
                    self.local_func_names[ast[1]] = evaled_exp
                    print("Local Variable "+ast[1] + " = " + str(evaled_exp))
                    return self.local_func_names[ast[1]], self.eval_ast(ast[3]) 
                #There was no local variable, check globals
                elif ast[1] in self.variables:
                    self.variables[ast[1]] = evaled_exp
                    print("Global Variable " + ast[1] + " = " + str(evaled_exp))
                    return self.variables[ast[1]], self.eval_ast(ast[3]) 
                #There was no id so create one in local variables
                else:
                    self.local_func_names[ast[1]] = evaled_exp
                    print("New Local Variable "+ast[1] + " = " + str(evaled_exp))
                    return self.local_func_names[ast[1]], self.eval_ast(ast[3]) 
        
        #############################################

        elif(ast[0] == 'NODE_CONDITIONAL'):
            evaled_exp = self.eval_ast(ast[1])
            if(evaled_exp == True):
                print()
                print('---IF BLOCK OK---')
                evaled_exp = self.eval_ast(ast[2])
                print('---IF BLOCK END---')
                print()
                return evaled_exp
            else:
                return None

        elif(ast[0] == 'NODE_CONDITIONAL_ELSE'):

            evaled_exp = self.eval_ast(ast[1])

            if(evaled_exp == True):
                print()
                print('---IF BLOCK OK---')
                evaled_exp = self.eval_ast(ast[2])
                print('---IF BLOCK END---')
                print()
            else:
                print()
                print('---ELSE BLOCK OK---')
                evaled_exp = self.eval_ast(ast[3])
                print('---ELSE BLOCK END---')
                print()

            return evaled_exp

        elif(ast[0] == 'NODE_CONDITIONAL_ELSE_CONDITIONAL'):

            evaled_exp = self.eval_ast(ast[1])

            if(evaled_exp == True):
                print()
                print('---IF BLOCK OK---')
                evaled_exp = self.eval_ast(ast[2])
                print('---IF BLOCK END---')
                print()
            else:
                evaled_exp = self.eval_ast(ast[3])

            return evaled_exp

            return self.eval_ast(ast[2]) if (self.eval_ast(ast[1]) == True) else self.eval_ast(ast[3])
        
        #############################################

        elif(ast[0] == 'NODE_BREAK'):
            return "BREAK"

        elif(ast[0] == 'NODE_WHILE'):
            
            loop_result = None

            evaled_exp = self.eval_ast(ast[1])

            if(evaled_exp == True):
                print('\n---Start While Loop---')
                while( evaled_exp == True ):
                    print('------ Iteration ------')
                    loop_result = self.eval_ast(ast[2])
                    
                    if(type(loop_result) == tuple):
                        if "BREAK" in loop_result:
                            print('--- Break While Loop ---')
                            break
                    elif "BREAK" == loop_result:
                        print('--- Break While Loop ---')
                        break
                    print('-----------------------')
                    evaled_exp  = self.eval_ast(ast[1])
                print('---Finish While Loop---\n')

            return loop_result
        
        #############################################

        elif(ast[0] == 'NODE_FUNCTIONAL'):
            return self.eval_ast(ast[1]) 

        elif(ast[0] == 'NODE_FUNCTION_DEFINITION'):
            return 

        elif(ast[0] == 'NODE_FUNCTION_CALL'):

            foo = self.functions[ast[1]]

            if ast[2]:

                values = [ self.eval_ast(val) for val in ast[2] ]
                
                i = 0
                for k in foo[3]:
                    foo[3][k] = values[i]          
                    i += 1

            self.local_func_names = foo[3]
            print('\n---Function ' + ast[1] + ' Called---')
            f_result = self.eval_ast(foo[2])
            self.local_func_names = None
            print('---Function ' + ast[1] + ' Ended---\n')
            return f_result

        #############################################

        elif(ast[0] == 'NODE_ID'):
            if(self.local_func_names == None):
                if ast[1] in self.variables:
                    return self.variables[ast[1]]
            else:
                if ast[1] in self.local_func_names:
                    return self.local_func_names[ast[1]]
                elif ast[1] in self.variables:
                    return self.variables[ast[1]]
                
        elif(ast[0] == 'NODE_NUMBER'):
            return ast[1]
   
        elif(ast[0] == 'NODE_LP_EXPRESSION_RP'):
            return self.eval_ast(ast[1])

        elif(ast[0] == 'NODE_UMINUS'):
            return -self.eval_ast(ast[1])

        elif(ast[0] == 'NODE_PLUS'):
            return self.eval_ast(ast[1]) + self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_MINUS'):
            return self.eval_ast(ast[1]) - self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_TIMES'):
            return self.eval_ast(ast[1]) * self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_DIVIDE'):
            return self.eval_ast(ast[1]) / self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_MOD'):
            return self.eval_ast(ast[1]) % self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_EXPONENT'):
            return self.eval_ast(ast[1]) ** self.eval_ast(ast[2])

        #############################################

        elif(ast[0] == 'NODE_LP_BOOL_EXPRESSION_RP'):
            return self.eval_ast(ast[1])

        elif(ast[0] == 'NODE_IS_EQUAL'):
            return self.eval_ast(ast[1]) == self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_IS_NOT_EQUAL'):
            return self.eval_ast(ast[1]) != self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_GREATER_THAN_EQ'):
            return self.eval_ast(ast[1]) >= self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_GREATER_THAN'):
            return self.eval_ast(ast[1]) > self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_LESS_THAN_EQ'):
            return self.eval_ast(ast[1]) <= self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_LESS_THAN'):
            return self.eval_ast(ast[1]) < self.eval_ast(ast[2])

        #############################################

        elif(ast[0] == 'NODE_BITWISE_AND'):
            return self.eval_ast(ast[1]) & self.eval_ast(ast[2])

        elif(ast[0] == 'NODE_BITWISE_OR'):
            return self.eval_ast(ast[1]) | self.eval_ast(ast[2])
        
        #############################################

        elif(ast[0] == 'NODE_AND'):
            return True if (self.eval_ast(ast[1]) == True and self.eval_ast(ast[2]) == True) else False

        elif(ast[0] == 'NODE_OR'):
            return True if (self.eval_ast(ast[1]) == True or self.eval_ast(ast[2]) == True) else False

    #######################################################################################

    def parse(self, tokens):
        result = super(CalcParser, self).parse(tokens)

        print()
        print("EVALUATION RESULT")

        x = None

        if type(result) == tuple:
            x = self.eval_ast(result)
        else:
            x = result

        '''
        stack = []

        stack.append(x)

        ress = []

        while (len(stack)):
            s = stack[-1]
            stack.pop()

            if(type(s) != tuple):
                ress.append(s)
            else:
                for n in s:
                    stack.append(n)

        ress.reverse()

        for i in ress:
            print()
            print(i)
        '''

        return x

    #######################################################################################

    #MISSING SEMI COLUMN
    #ASSIGNMENT : ID = EXPRESSION 
    @_('ID ASSIGN EXPRESSION error')
    def ASSIGNMENT(self, production):
        print('Expected ; or , at line', production.lineno)

    #INVALID EXPRESSION
    #ASSIGNMENT : ID = error ; 
    @_('ID ASSIGN error SEMI_COL')
    def ASSIGNMENT(self, production):
        print('Invalid expression at line', production.lineno)

    #######################################################################################
    
    #INVALID CONDITIONAL
    #LOOP : WHILE error { STATEMENT_LIST }
    @_('WHILE error LCURLY STATEMENT_LIST RCURLY')
    def LOOP(self, production):
        print('Invalid condition at line', production.lineno)

    #INVALID STATEMENT LIST
    #LOOP : WHILE ( BOOL_EXPRESSION ) error
    @_('WHILE LPAREN BOOL_EXPRESSION RPAREN error')
    def LOOP(self, production):
        print('Invalid statement block at line', production.lineno)

    #######################################################################################

    #MISSING SEMI COLUMN
    #FUNCTION_CALL : ID (VALUE_LIST) 
    @_('ID LPAREN VALUE_LIST RPAREN error')  
    def FUNCTION_CALL(self, production):
        print('Expected ; at line', production.lineno)

    #INVALID PARAMETER LIST
    #FUNCTION_CALL : ID error ;
    @_('ID error SEMI_COL')  
    def FUNCTION_CALL(self, production):
        print('Invalid paramters list at line', production.lineno)

    #######################################################################################

    #INVALID PARAMETER LIST
    #FUNCTION_DEFINITION : FUNCTION ID error { STATEMENT_LIST } | FUNCTION ID error { STATEMENT_LIST } ;
    @_('FUNCTION ID error LCURLY STATEMENT_LIST RCURLY', 
       'FUNCTION ID error LCURLY STATEMENT_LIST RCURLY SEMI_COL')  
    def FUNCTION_DEFINITION(self, production):
        print('Invalid paramters list at line', production.lineno)

    #INVALID STATEMENT LIST
    #FUNCTION_DEFINITION : FUNCTION ID (PARAM_LIST) error | FUNCTION ID (PARAM_LIST) error ;
    @_('FUNCTION ID LPAREN PARAM_LIST RPAREN error', 
       'FUNCTION ID LPAREN PARAM_LIST RPAREN error SEMI_COL')  
    def FUNCTION_DEFINITION(self, production):
        print('Invalid statement block at line', production.lineno)

    #INVALID FUNCTION IDENTIFIER
    #FUNCTION_DEFINITION : FUNCTION error (PARAM_LIST) { STATEMENT_LIST } | FUNCTION error (PARAM_LIST) { STATEMENT_LIST } ;
    @_('FUNCTION error LPAREN PARAM_LIST RPAREN LCURLY STATEMENT_LIST RCURLY', 
       'FUNCTION error LPAREN PARAM_LIST RPAREN LCURLY STATEMENT_LIST RCURLY SEMI_COL')  
    def FUNCTION_DEFINITION(self, production):
        print('Invalid function identifier at line', production.lineno)

    #######################################################################################

    #INVALID CONDITIONAL
    #CONDITIONAL : IF error { STATEMENT_LIST }
    @_('IF error LCURLY STATEMENT_LIST RCURLY',
       'IF error LCURLY STATEMENT_LIST RCURLY ELSE LCURLY STATEMENT_LIST RCURLY',
       'IF error LCURLY STATEMENT_LIST RCURLY ELSE CONDITIONAL')
    def CONDITIONAL(self, production):   
        print('Invalid condition at line', production.lineno)

    #INVALID STATEMENT LIST
    #CONDITIONAL : IF ( BOOL_EXPRESSION ) error
    @_('IF LPAREN BOOL_EXPRESSION RPAREN error',
       'IF LPAREN BOOL_EXPRESSION RPAREN error ELSE LCURLY STATEMENT_LIST RCURLY',
       'IF LPAREN BOOL_EXPRESSION RPAREN LCURLY STATEMENT_LIST RCURLY ELSE error')
    def CONDITIONAL(self, production):   
        print('Invalid statement block at line', production.lineno)

    #######################################################################################