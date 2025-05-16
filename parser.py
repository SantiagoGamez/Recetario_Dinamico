import ply.yacc as yacc
from compiler import tokens, lexer

def p_receta(p):
    '''receta : titulo ingredientes instrucciones'''
    p[0] = {
        'titulo': p[1],
        'ingredientes': p[2],
        'instrucciones': p[3]
    }

def p_titulo(p):
    '''titulo : TITULO'''
    p[0] = p[1][1:].strip()

def p_ingredientes(p):
    '''ingredientes : INGREDIENTES lista_ingredientes'''
    p[0] = p[2]

def p_lista_ingredientes(p):
    '''lista_ingredientes : ingrediente
                        | lista_ingredientes ingrediente'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_ingrediente(p):
    '''ingrediente : INGREDIENTE'''
    parts = p[1].split(' - ')
    if len(parts) != 2:
        print(f"Formato de ingrediente inválido: {p[1]}")
        p[0] = None
        return
    
    nombre = parts[0].strip()
    cantidad_medida = parts[1].split()
    
    if not cantidad_medida:
        print(f"Ingrediente sin cantidad: {p[1]}")
        p[0] = None
        return
    
    p[0] = {
        'nombre': nombre,
        'cantidad': cantidad_medida[0],
        'medida': ' '.join(cantidad_medida[1:]) if len(cantidad_medida) > 1 else None
    }

def p_instrucciones(p):
    '''instrucciones : INSTRUCCIONES lista_instrucciones'''
    p[0] = p[2]

def p_lista_instrucciones(p):
    '''lista_instrucciones : INSTRUCCION
                        | lista_instrucciones INSTRUCCION'''
    if len(p) == 2:
        p[0] = [p[1].strip()]
    else:
        p[0] = p[1] + [p[2].strip()]

def p_error(p):
    print(f"Error de sintaxis en '{p.value}'")

def parse(data):
    global section
    from compiler import section
    section = 0
    return parser.parse(data, lexer=lexer)

parser = yacc.yacc()

data = '''
#Huevo con Jamon
INGREDIENTES
Huevo - 1 huevo
Jamon - 200 mg
INSTRUCCIONES
Cortar jamon
Cocinar huevo y jamon
'''

result = parser.parse(data, lexer=lexer)
print(result)