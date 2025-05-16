import ply.lex as lex

tokens = (
    'TITULO',
    'INGREDIENTES',
    'NUMERO',
    'MEDIDA',
    'NOMBRE_ING',
    'INSTRUCCIONES',
    'INSTRUCCION',
)

# tracks whether we're before title (0), in title (1), ingredients (2) or instructions (3)
section = 0

def t_TITULO(t):
    r'\#[A-Za-z ].*'
    global section
    if section == 0:
        section = 1
        # strip the leading '#'
        t.value = t.value.lstrip('#').strip()
        return t

def t_INGREDIENTES(t):
    r'INGREDIENTES'
    global section
    section = 2
    return t

def t_INSTRUCCIONES(t):
    r'INSTRUCCIONES'
    global section
    section = 3
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_MEDIDA(t):
    r'(g|mg|ml|l)'
    return t

def t_NOMBRE_ING(t):
    r'[A-Za-z]+(?:\s+[A-Za-z]+)*'
    return t

def t_INSTRUCCION(t):
    r'[A-Za-z].*'
    return t

# skip whitespace and newlines
t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
