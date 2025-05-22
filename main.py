import sys
import ply.lex as lex
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
import webbrowser
import atexit
import tempfile

class RecipeConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor de Recetas - TXT a HTML")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Center the window on startup
        self.center_window()
        
        # Variables
        self.selected_file = tk.StringVar()
        self.output_file = ""
        
        self.setup_ui()
        
        atexit.register(self.cleanup_file)
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Convertidor de Recetas", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Seleccionar Archivo", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Archivo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.selected_file, state="readonly")
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_button = ttk.Button(file_frame, text="Examinar...", command=self.browse_file)
        self.browse_button.grid(row=0, column=2)
        
        # Convert section
        convert_frame = ttk.LabelFrame(main_frame, text="Conversión", padding="10")
        convert_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.convert_button = ttk.Button(convert_frame, text="Convertir a HTML", 
                                       command=self.convert_file, state="disabled")
        self.convert_button.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(convert_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Estado", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.status_text = tk.Text(status_frame, height=6, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to status text
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Download section
        download_frame = ttk.LabelFrame(main_frame, text="Descargar", padding="10")
        download_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        button_frame = ttk.Frame(download_frame)
        button_frame.pack()
        
        self.download_button = ttk.Button(button_frame, text="Descargar HTML", 
                                        command=self.download_file, state="disabled")
        self.download_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_button = ttk.Button(button_frame, text="Abrir en Navegador", 
                                    command=self.open_in_browser, state="disabled")
        self.open_button.pack(side=tk.LEFT)
        
        self.log_message("Bienvenido al Convertidor de Recetas")
        self.log_message("Seleccione un archivo de texto para comenzar")
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de receta",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            self.selected_file.set(filename)
            self.convert_button.config(state="normal")
            self.log_message(f"Archivo seleccionado: {os.path.basename(filename)}")
    
    def log_message(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def convert_file(self):
        if not self.selected_file.get():
            messagebox.showerror("Error", "Por favor seleccione un archivo primero")
            return
        
        try:
            # Start progress bar
            self.progress.start()
            self.convert_button.config(state="disabled")
            self.download_button.config(state="disabled")
            self.open_button.config(state="disabled")
            
            self.log_message("Iniciando conversión...")
            
            # Read the recipe file
            file_path = self.selected_file.get()
            self.log_message(f"Leyendo archivo: {os.path.basename(file_path)}")
            
            data = self.leer_receta(file_path)
            
            # Generate output file name
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            temp_dir = tempfile.gettempdir()
            self.output_file = os.path.join(temp_dir, f"{base_name}.html")
            
            # Process with lexer
            self.log_message("Procesando contenido...")
            section = 0  # Reset section counter
            
            # Create lexer instance
            lexer = lex.lex(module=self)
            lexer.input(data)
            
            # Collect all tokens
            tokens_list = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens_list.append(tok)
            
            self.log_message(f"Tokens procesados: {len(tokens_list)}")
            
            # Convert to HTML
            self.log_message("Generando archivo HTML...")
            if self.tokens_to_html(tokens_list, self.output_file):
                self.log_message("✅ Conversión completada exitosamente!")
                self.log_message(f"Archivo generado: {self.output_file}")
                
                self.download_button.config(state="normal")
                self.open_button.config(state="normal")
                
                messagebox.showinfo("Éxito", f"Archivo HTML generado exitosamente:\n{self.output_file}")
            else:
                self.log_message("❌ Error al generar el archivo HTML")
                messagebox.showerror("Error", "Error al generar el archivo HTML")
        
        except Exception as e:
            self.log_message(f"❌ Error durante la conversión: {str(e)}")
            messagebox.showerror("Error", f"Error durante la conversión:\n{str(e)}")
        
        finally:
            self.progress.stop()
            self.convert_button.config(state="normal")
    
    def download_file(self):
        if not self.output_file or not os.path.exists(self.output_file):
            messagebox.showerror("Error", "No hay archivo HTML para descargar")
            return
        
        save_path = filedialog.asksaveasfilename(
            title="Guardar archivo HTML",
            defaultextension=".html",
            filetypes=[("Archivos HTML", "*.html"), ("Todos los archivos", "*.*")],
            initialfile=self.output_file
        )
        
        if save_path:
            try:
                shutil.copy2(self.output_file, save_path)
                self.log_message(f"Archivo guardado en: {save_path}")
                messagebox.showinfo("Éxito", f"Archivo guardado exitosamente en:\n{save_path}")
            except Exception as e:
                self.log_message(f"❌ Error al guardar: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar el archivo:\n{str(e)}")
    
    def open_in_browser(self):
        if not self.output_file or not os.path.exists(self.output_file):
            messagebox.showerror("Error", "No hay archivo HTML para abrir")
            return
        
        try:
            webbrowser.open(f"file://{os.path.abspath(self.output_file)}")
            self.log_message("Archivo abierto en el navegador")
        except Exception as e:
            self.log_message(f"❌ Error al abrir en navegador: {str(e)}")
            messagebox.showerror("Error", f"Error al abrir en navegador:\n{str(e)}")
    
    def leer_receta(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as archivo:
                return archivo.read()
        except FileNotFoundError:
            raise Exception(f"El archivo '{file_path}' no existe.")
        except Exception as e:
            raise Exception(f"Error al leer el archivo: {e}")
    
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
    
    def t_TITULO(self, t):
        r'\#[a-zA-Z].*'
        if self.section == 0:
            return t
    
    def t_INGREDIENTES(self, t):
        r'INGREDIENTES'
        self.section += 1
        return t
    
    def t_INSTRUCCIONES(self, t):
        r'INSTRUCCIONES'
        self.section += 1
        return t
    
    t_MEDICIONES = r'\d+[g|l|ml|mg]'
    
    def t_NUMERO(self, t):
        r'\d+ '
        t.value = int(t.value)
        return t
    
    def t_INGREDIENTE(self, t):
        r'[a-zA-Z]+(\s+[a-zA-Z]+)*\s*-\s*\d+\s*[a-zA-Z]*'
        return t
    
    def t_INSTRUCCION(self, t):
        r'[a-zA-Z].*'
        return t
    
    t_ignore = ' \t\n'
    
    def t_error(self, t):
        self.log_message(f"Caracter ilegal: '{t.value[0]}'")
        t.lexer.skip(1)
    
    def tokens_to_html(self, tokens_list, output_file):
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .recipe-container {{
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 4px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #34495e;
            margin-top: 35px;
            margin-bottom: 20px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .ingredientes-list {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 2px solid #e8f5e8;
        }}
        .ingredientes-list ul {{
            list-style-type: none;
            padding: 0;
            margin: 0;
        }}
        .ingredientes-list li {{
            margin: 12px 0;
            padding: 15px;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #27ae60;
            font-size: 1.1em;
            transition: transform 0.2s ease;
        }}
        .ingredientes-list li:hover {{
            transform: translateX(5px);
        }}
        /* Ingredient name highlighting */
        .ingredient-name {{
            color: #27ae60;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        /* Quantity highlighting */
        .quantity {{
            color: #e74c3c;
            font-weight: bold;
            background-color: rgba(231, 76, 60, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(231, 76, 60, 0.3);
        }}
        .instrucciones-list {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 25px;
            border-radius: 12px;
            border: 2px solid #f39c12;
        }}
        .instrucciones-list ol {{
            padding-left: 30px;
            margin: 0;
        }}
        .instrucciones-list li {{
            margin: 15px 0;
            line-height: 1.8;
            padding: 15px;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #f39c12;
            font-size: 1.05em;
        }}
        /* Action verbs highlighting */
        .action-verb {{
            color: #8e44ad;
            font-weight: bold;
            background-color: rgba(142, 68, 173, 0.1);
            padding: 2px 4px;
            border-radius: 3px;
            border-bottom: 2px solid rgba(142, 68, 173, 0.3);
        }}
        /* Time and temperature highlighting */
        .time-temp {{
            color: #e67e22;
            font-weight: bold;
            background-color: rgba(230, 126, 34, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(230, 126, 34, 0.3);
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
            font-size: 14px;
            font-style: italic;
            padding: 20px;
            border-top: 2px dashed #bdc3c7;
        }}
        /* Responsive design */
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            .recipe-container {{ padding: 20px; }}
            h1 {{ font-size: 2em; }}
            h2 {{ font-size: 1.5em; }}
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
            # Color highlighting
            highlighted_ingredient = self.highlight_ingredient(ingrediente)
            html_content += f"\n                <li>{highlighted_ingredient}</li>"
        
        html_content += """
            </ul>
        </div>
        
        <h2>👩‍🍳 Instrucciones</h2>
        <div class="instrucciones-list">
            <ol>"""
        
        for i, instruccion in enumerate(instrucciones, 1):
            # Color highlighting
            highlighted_instruction = self.highlight_instruction(instruccion)
            html_content += f"\n                <li>{highlighted_instruction}</li>"
        
        html_content += """
            </ol>
        </div>
        
        <div class="footer">
            <p>Receta generada automáticamente</p>
        </div>
    </div>
</body>
</html>"""
        
        # Make HTML file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            self.log_message(f"Error al escribir archivo HTML: {e}")
            return False
    
    def highlight_ingredient(self, ingredient_text):
        """Add color highlighting to ingredient names and quantities"""
        import re
        
        pattern = r'([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)\s*-\s*(\d+)\s*([a-zA-Z]*)'
        match = re.match(pattern, ingredient_text)
        
        if match:
            ingredient_name = match.group(1).strip()
            quantity = match.group(2)
            unit = match.group(3)
            
            highlighted = f'<span class="ingredient-name">{ingredient_name}</span> - <span class="quantity">{quantity} {unit}</span>'
            return highlighted
        
        return ingredient_text
    
    def highlight_instruction(self, instruction_text):
        """Add color highlighting to action verbs and measurements in instructions"""
        import re
        
        # Common cooking verbs
        action_verbs = [
            'mezclar', 'batir', 'cocinar', 'hornear', 'freír', 'hervir', 'saltear',
            'picar', 'cortar', 'rallar', 'pelar', 'lavar', 'añadir', 'agregar',
            'verter', 'servir', 'calentar', 'enfriar', 'refrigerar', 'tapar',
            'destapar', 'remover', 'revolver', 'amasar', 'estirar', 'doblar',
            'precalentar', 'dorar', 'sofreír', 'condimentar', 'sazonar'
        ]
        
        # Time and temperature patterns
        time_temp_patterns = [
            r'\d+\s*minutos?', r'\d+\s*horas?', r'\d+\s*segundos?',
            r'\d+\s*°[CF]', r'\d+\s*grados?'
        ]
        
        highlighted_text = instruction_text
        
        # Highlight action cooking verbs
        for verb in action_verbs:
            pattern = r'\b(' + verb + r')\b'
            highlighted_text = re.sub(pattern, r'<span class="action-verb">\1</span>', 
                                    highlighted_text, flags=re.IGNORECASE)
        
        # Highlight time and temperature
        for pattern in time_temp_patterns:
            highlighted_text = re.sub(pattern, r'<span class="time-temp">\g<0></span>', 
                                    highlighted_text, flags=re.IGNORECASE)
        
        return highlighted_text
    
    def cleanup_file(self):
        if self.output_file and os.path.exists(self.output_file):
            try:
                os.remove(self.output_file)
                print(f"Archivo temporal eliminado: {self.output_file}")
            except Exception:
                pass

def main():
    # Run the application
    try:
        import ply.lex as lex
    except ImportError:
        print("Error: PLY (Python Lex-Yacc) no está instalado.")
        print("Instale PLY ejecutando: pip install ply")
        sys.exit(1)
    
    root = tk.Tk()
    app = RecipeConverterGUI(root)
    
    try:
        root.iconbitmap('recipe_icon.ico') 
    except:
        pass
    
    root.mainloop()

if __name__ == '__main__':
    main()