import ply.lex as lex
import ply.yacc as yacc
from compiler import tokens, lexer

lexer = lex.lex()
def p_receta(p):
    p[0] = {
        'titulo': p[1],
        'ingredientes': p[3],
        'instrucciones': p[5]
    }

def p_lista_ingredientes(p):
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_ingrediente(p):
    if len(p) == 3:
        p[0] = {'cantidad': p[1], 'nombre': p[2], 'medida': None}
    else:
        p[0] = {'cantidad': p[1], 'nombre': p[3], 'medida': p[2]}

def p_lista_instrucciones(p):
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_error(p):
    print(f"Error de sintaxis en '{p.value}'")

parser = yacc.yacc()