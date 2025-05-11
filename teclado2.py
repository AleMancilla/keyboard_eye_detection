import tkinter as tk
import threading
import time
from openai import OpenAI

class VirtualKeyboard:
    def __init__(self, root, command_queue):
        self.root = root
        self.command_queue = command_queue

        # Configuración de la API de OpenAI
        self.client = OpenAI(
            api_key="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"
        )

        # Campo de entrada
        self.entry = tk.Entry(root, width=50, font=("Arial", 16))
        self.entry.grid(row=0, column=0, columnspan=11, padx=10, pady=10)

        # Vincular el evento de teclado al campo de entrada
        self.entry.bind("<KeyRelease>", self.update_suggestions)

        # Inicialización de frases y teclas
        self.keys = [
            ['Tengo que ir al baño','1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['No, gracias','Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['Hola, necesito ayuda.','A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Estoy bien, solo necesito más tiempo.','Z', 'X', 'C', 'V', 'B', 'N', 'M'],
            ['¿Podrías repetir, por favor?','Espacio', '←', 'Limpiar']
        ]
        self.buttons = []  # Lista de todas las filas de botones
        self.selected = (0, 0)  # Botón seleccionado inicialmente

        # Crear las filas
        self.create_info_row()  # Fila de 3 columnas debajo del campo de entrada
        self.create_keyboard()  # Teclas del teclado

        # Resaltar el botón inicial
        self.highlight_selected()

        # Obtener sugerencias iniciales
        self.update_initial_suggestions()

        # Hilo para escuchar comandos
        self.listen_thread = threading.Thread(target=self.listen_to_queue, daemon=True)
        self.listen_thread.start()

    def create_info_row(self):
        # Crear una fila de tres columnas debajo del campo de entrada
        self.info_buttons = []
        for i in range(3):
            btn = tk.Button(self.root, text=f"Sugerencia {i + 1}", width=15, height=2,
                            font=("Arial", 12), bg="lightgrey", relief="flat", bd=1)
            btn.grid(row=1, column=i * 4, columnspan=3, padx=10, pady=10)  # Espaciado entre botones
            btn.configure(command=lambda idx=i: self.insert_suggestion(idx))
            self.info_buttons.append(btn)

        # Agregar las sugerencias a la lista de botones para navegación
        self.buttons.append(self.info_buttons)

    def update_initial_suggestions(self):
        # Solicitar sugerencias iniciales a la API de OpenAI
        prompt = "Dame 3 palabras separadas por comas para comenzar una conversación."
        try:
            # Llamada a la API de OpenAI usando el cliente
            response = self.client.responses.create(
                model="gpt-4o",
                instructions="Eres un asistente útil.",
                input=prompt
            )
            # Extraer las palabras separadas por comas
            suggestions = response.output_text.strip().split(",")
            suggestions = [s.strip() for s in suggestions]  # Eliminar espacios adicionales

            # Actualizar los botones con las sugerencias
            for i, suggestion in enumerate(suggestions):
                if i < len(self.info_buttons):
                    self.info_buttons[i].config(text=suggestion)
        except Exception as e:
            print(f"Error al obtener sugerencias iniciales: {e}")

    def update_suggestions(self, event=None):
        print("ENTRO PARA ACTUALIZARRRRRRRR")
        current_text = self.entry.get().strip()

        if not current_text:
            prompt = (
                "Vas a actuar como un generador de autocompletado. "
                "Solo responde con 3 palabras aleatorias separadas por comas para comenzar una conversación."
            )
        else:
            prompt = f"""
    Vas a actuar como un generador de autocompletado de acuerdo a las letras que te mande.
    Solo responde con una lista de 3 palabras sugeridas, separadas por comas. No escribas ninguna explicación.

    Ejemplo:
    - Entrada: ho
    - Sugerencias: hola, hoy, hoigan

    Entrada: {current_text}
    """

        try:
            # ✅ Usa el endpoint correcto
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )

            # ✅ Extraer respuesta del primer mensaje
            content = response.choices[0].message.content.strip()
            suggestions = [s.strip() for s in content.split(",")]

            # ✅ Actualizar los botones
            for i in range(3):
                text = suggestions[i] if i < len(suggestions) else ""
                self.info_buttons[i].config(text=text)

        except Exception as e:
            print(f"❌ Error al obtener sugerencias: {e}")



    def insert_suggestion(self, idx):
        # Insertar la sugerencia seleccionada en el campo de entrada
        if idx < len(self.info_buttons):
            suggestion = self.info_buttons[idx].cget("text")
            self.entry.insert(tk.END, suggestion)

    def create_keyboard(self):
        for row_idx, row in enumerate(self.keys, 2):
            button_row = []
            for col_idx, key in enumerate(row):
                # Ajustar ancho si es la primera columna (col_idx == 0)
                button_width = 15 
                if col_idx == 0 and len(key) > 10:
                    button_width = 25
                    button_height = 3
                    wrap_len = 180  # En píxeles, para ajustar el texto
                else:
                    button_width = 7
                    button_height = 2
                    wrap_len = 0  # sin wrap

                btn = tk.Button(self.root, text=key, width=button_width, height=button_height,
                                font=("Arial", 12), bg='lightgrey',
                                relief='flat', bd=1, wraplength=wrap_len, justify='center')
                
                btn.grid(row=row_idx, column=col_idx + 1, padx=2, pady=2)
                btn.configure(command=lambda k=key: self.handle_key(k))
                button_row.append(btn)
            self.buttons.append(button_row)


    def handle_key(self, key):
        if key == 'Espacio':
            self.insert_text(' ')
        elif key == '←':
            self.backspace()
        elif key == 'Limpiar':
            self.clear()
        else:
            self.insert_text(key)

    def insert_text(self, char):
        self.entry.insert(tk.END, char)

    def backspace(self):
        current_text = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current_text[:-1])

    def clear(self):
        self.entry.delete(0, tk.END)

    def highlight_selected(self):
        # Limpiar resaltados de todos los botones
        for r, row in enumerate(self.buttons):
            for c, btn in enumerate(row):
                btn.configure(relief='flat', bd=0, highlightthickness=0)

        # Resaltar el botón seleccionado
        r, c = self.selected
        self.buttons[r][c].configure(
            relief='solid', bd=4, highlightthickness=2, highlightbackground='green'
        )

    def move_selection(self, direction):
        r, c = self.selected

        if direction == 'up':
            if r > 0:
                r -= 1
            else:
                r = len(self.buttons) - 1  # Ir a la última fila
            c = min(c, len(self.buttons[r]) - 1)

        elif direction == 'down':
            if r < len(self.buttons) - 1:
                r += 1
            else:
                r = 0  # Ir a la primera fila
            c = min(c, len(self.buttons[r]) - 1)

        elif direction == 'left':
            if c > 0:
                c -= 1
            else:
                c = len(self.buttons[r]) - 1  # Ir a la última columna de la fila actual

        elif direction == 'right':
            if c < len(self.buttons[r]) - 1:
                c += 1
            else:
                c = 0  # Ir a la primera columna de la fila actual

        elif direction == 'enter':
            self.press_selected()

        self.selected = (r, c)
        self.highlight_selected()


    def press_selected(self):
        r, c = self.selected
        self.buttons[r][c].invoke()  # Simular la pulsación del botón

    def listen_to_queue(self):
        while True:
            if not self.command_queue.empty():
                signal = self.command_queue.get()
                if signal == '1':
                    self.root.after(0, lambda: self.move_selection('up'))
                elif signal == '0':
                    self.root.after(0, lambda: self.move_selection('down'))
                elif signal == '5':
                    self.root.after(0, lambda: self.move_selection('left'))
                elif signal == '4':
                    self.root.after(0, lambda: self.move_selection('right'))
                elif signal == '3':
                    self.root.after(0, lambda: self.move_selection('enter'))
            time.sleep(0.05)

def start_virtual_keyboard(queue):
    root = tk.Tk()
    app = VirtualKeyboard(root, queue)
    root.mainloop()