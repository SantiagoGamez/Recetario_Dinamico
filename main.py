import sys
import ply.lex as lex
import os

def leer_receta(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

# Lexer tokens and functions
tokens = ('TITULO',
          'INGREDIENTES',
          'MEDICIONES',
          'NUMERO',
          'INGREDIENTE',
          'INSTRUCCIONES',
          'INSTRUCCION')

# Global variable for tracking sections
section = 0

def t_TITULO(t):
    r'\#[a-zA-Z].*'
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

def tokens_to_html(tokens_list, output_file):
    # Parse tokens into structured data
    titulo = ""
    ingredientes = []
    instrucciones = []
    
    current_section = None
    
    for token in tokens_list:
        if token.type == 'TITULO':
            titulo = token.value[1:].strip()  # Remove the # symbol
        elif token.type == 'INGREDIENTES':
            current_section = 'ingredientes'
        elif token.type == 'INSTRUCCIONES':
            current_section = 'instrucciones'
        elif token.type == 'INGREDIENTE':
            ingredientes.append(token.value)
        elif token.type == 'INSTRUCCION':
            if current_section == 'instrucciones':
                instrucciones.append(token.value)
    
    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .recipe-container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        .ingredientes-list {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}
        .ingredientes-list ul {{
            list-style-type: none;
            padding: 0;
        }}
        .ingredientes-list li {{
            margin: 8px 0;
            padding: 5px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .instrucciones-list {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
        }}
        .instrucciones-list ol {{
            padding-left: 25px;
        }}
        .instrucciones-list li {{
            margin: 12px 0;
            line-height: 1.6;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #7f8c8d;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="recipe-container">
        <h1>{titulo}</h1>
        
        <h2>📋 Ingredientes</h2>
        <div class="ingredientes-list">
            <ul>"""
    
    for ingrediente in ingredientes:
        html_content += f"\n                <li>{ingrediente}</li>"
    
    html_content += """
            </ul>
        </div>
        
        <h2>👩‍🍳 Instrucciones</h2>
        <div class="instrucciones-list">
            <ol>"""
    
    for i, instruccion in enumerate(instrucciones, 1):
        html_content += f"\n                <li>{instruccion}</li>"
    
    html_content += """
            </ol>
        </div>
        
        <div class="footer">
            <p>Receta generada automáticamente</p>
        </div>
    </div>
</body>
</html>"""
    
    # Write HTML file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"Error al escribir archivo HTML: {e}")
        return False

def main():
    # Check if a file argument was provided
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.txt>")
        print("Ejemplo: python main.py example.txt")
        sys.exit(1)
    
    # Get the file path from command line arguments
    file_path = sys.argv[1]
    
    # Generate output file name (replace .txt with .html)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = f"{base_name}.html"
    
    # Read the recipe from the file
    data = leer_receta(file_path)
    
    # Reset section counter before processing
    global section
    section = 0
    
    # Create lexer instance
    lexer = lex.lex()
    
    # Process the data with lexer
    lexer.input(data)
    
    # Collect all tokens
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
    
    # Convert tokens to HTML
    print(f"Procesando archivo: {file_path}")
    if tokens_to_html(tokens_list, output_file):
        print(f"✅ Archivo HTML generado exitosamente: {output_file}")
        print(f"📄 Puedes abrir el archivo '{output_file}' en tu navegador web")
    else:
        print("❌ Error al generar el archivo HTML")
        sys.exit(1)

if __name__ == '__main__':
    main()