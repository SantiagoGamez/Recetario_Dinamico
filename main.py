from parser import parser
import sys

def leer_receta(file_path):
    try:
        with open(file_path, 'r', encoding='utf=8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

def main():
    ...

if __name__ == '__main__':
    main()