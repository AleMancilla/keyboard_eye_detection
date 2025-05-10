import tkinter as tk
import multiprocessing
import threading
import time

class VirtualKeyboard:
    def __init__(self, root, command_queue):
        self.root = root
        self.command_queue = command_queue

        self.entry = tk.Entry(root, width=50, font=("Arial", 16))
        self.entry.grid(row=0, column=0, columnspan=10, padx=10, pady=10)

        self.keys = [
            ['1','2','3','4','5','6','7','8','9','0'],
            ['Q','W','E','R','T','Y','U','I','O','P'],
            ['A','S','D','F','G','H','J','K','L'],
            ['Z','X','C','V','B','N','M'],
            ['Espacio', '←', 'Limpiar']
        ]
        self.buttons = []
        self.selected = (0, 0)
        self.create_keyboard()
        self.highlight_selected()

        self.listen_thread = threading.Thread(target=self.listen_to_queue, daemon=True)
        self.listen_thread.start()

    def create_keyboard(self):
        for row_idx, row in enumerate(self.keys, 1):
            button_row = []
            for col_idx, key in enumerate(row):
                btn = tk.Button(self.root, text=key, width=7, height=2,
                                font=("Arial", 12), bg='lightgrey',
                                relief='flat', bd=1)
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)
                btn.configure(command=lambda k=key: self.handle_key(k))
                button_row.append(btn)
            self.buttons.append(button_row)

    def insert_text(self, char):
        self.entry.insert(tk.END, char)

    def backspace(self):
        current_text = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current_text[:-1])

    def space(self):
        self.insert_text(' ')

    def clear(self):
        self.entry.delete(0, tk.END)

    def handle_key(self, key):
        if key == 'Espacio':
            self.space()
        elif key == '←':
            self.backspace()
        elif key == 'Limpiar':
            self.clear()
        else:
            self.insert_text(key)

    def highlight_selected(self):
        for r, row in enumerate(self.buttons):
            for c, btn in enumerate(row):
                btn.configure(relief='flat', bd=0, highlightthickness=0)
        r, c = self.selected
        self.buttons[r][c].configure(
            relief='solid', bd=4, highlightthickness=2, highlightbackground='green'
        )

    def move_selection(self, direction):
        r, c = self.selected
        if direction == 'up' and r > 0:
            r -= 1
            c = min(c, len(self.buttons[r]) - 1)
        elif direction == 'down' and r < len(self.buttons) - 1:
            r += 1
            c = min(c, len(self.buttons[r]) - 1)
        elif direction == 'left' and c > 0:
            c -= 1
        elif direction == 'right' and c < len(self.buttons[r]) - 1:
            c += 1
        elif direction == 'enter':
            self.press_selected()
        self.selected = (r, c)
        self.highlight_selected()

    def press_selected(self):
        r, c = self.selected
        key = self.keys[r][c]
        self.handle_key(key)

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
