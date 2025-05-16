import ply.yacc as yacc
import compiler
from compiler import tokens

# reuse the lexer defined in compiler.py
lexer = compiler.lexer

def p_receta(p):
    'receta : TITULO INGREDIENTES lista_ingredientes INSTRUCCIONES lista_instrucciones'
    p[0] = {
        'titulo': p[1],
        'ingredientes': p[3],
        'instrucciones': p[5],
    }

def p_lista_ingredientes(p):
    '''lista_ingredientes : ingrediente
                         | lista_ingredientes ingrediente'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_ingrediente(p):
    'ingrediente : NOMBRE_ING "-" NUMERO MEDIDA'
    p[0] = {
        'nombre': p[1],
        'cantidad': p[3],
        'medida': p[4],
    }

def p_lista_instrucciones(p):
    '''lista_instrucciones : INSTRUCCION
                           | lista_instrucciones INSTRUCCION'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_error(p):
    if p:
        print(f"Error de sintaxis en token {p.type!r}, valor {p.value!r}")
    else:
        print("Error de sintaxis: fin de archivo inesperado")

def parse(data):
    # reset section counter before parsing
    compiler.section = 0
    return parser.parse(data, lexer=compiler.lexer)

parser = yacc.yacc()
