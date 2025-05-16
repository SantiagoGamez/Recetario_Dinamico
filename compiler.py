import ply.lex as lex

tokens = ('TITULO',
          'INGREDIENTES',
          'MEDICIONES',
          'NUMERO',
          'INGREDIENTE',
          'INSTRUCCIONES',
          'INSTRUCCION')

section = 0
def t_TITULO(t):
    r'\#[a-zA-Z].*'
    print('hi')
    global section
    if section == 0:
        return t

def t_INGREDIENTES(t):
    r'INGREDIENTES'
    global section
    section += 1
    return t

def t_INSTRUCCIONES(t):
    r'INSTRUCCIONES'
    global section
    section += 1
    return t

t_MEDICIONES = r'\d+[g|l|ml|mg]'

def t_NUMERO(t):
    r'\d+ '
    t.value = int(t.value)
    return t

def t_INGREDIENTE(t):
    r'[a-zA-Z]+(\s+[a-zA-Z]+)*\s*-\s*\d+\s*[a-zA-Z]*'
    return t

def t_INSTRUCCION(t):
    r'[a-zA-Z].*'
    return t


t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

data = '''
#Huevo con Jamon
INGREDIENTES
Huevo - 1 huevo
Jamon - 200 mg
INSTRUCCIONES
Cortar jamon
Cocinar huevo y jamon
'''

lexer.input(data)


while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
