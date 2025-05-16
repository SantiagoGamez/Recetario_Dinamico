import sys
from parser import parse # Import our parser

def leer_receta(file_path):
    try:
        # note the correct encoding name is 'utf-8', not 'utf=8'
        with open(file_path, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

def main():
    # 1. check that exactly one argument (the file path) was given
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_al_archivo.txt>")
        sys.exit(1)

    # 2. read the recipe text
    file_path = sys.argv[1]
    data = leer_receta(file_path)

    # 3. parse it
    resultado = parse(data)

    # 4. show the result
    print(resultado)

if __name__ == '__main__':
    main()
