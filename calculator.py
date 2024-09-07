import tkinter as tk
from tkinter import ttk

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self.configure(bg="black")

        self.current_value = tk.StringVar()
        self.create_display()
        self.create_buttons()

    def create_display(self):
        entry = ttk.Entry(self, textvariable=self.current_value, font=("Arial", 18), justify="right")
        entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('(', 5, 1), (')', 5, 2), ('Exit', 5, 3),
            ('Backspace', 6, 0, 2), ('AC', 6, 2, 2)
        ]

        for text, row, col, *colspan in buttons:
            button_widget = tk.Button(self, text=text, command=lambda t=text: self.on_button_click(t), 
                                       font=("Arial", 14), bg="white", fg="black")
            button_widget.grid(row=row, column=col, columnspan=(colspan[0] if colspan else 1), 
                              padx=5, pady=5, sticky="nsew")

    def on_button_click(self, button_text):
        if button_text == "C":
            self.current_value.set("")
        elif button_text == "=":
            try:
                self.current_value.set(str(eval(self.current_value.get())))
            except Exception:
                self.current_value.set("Error")
        elif button_text == "Exit":
            self.quit()
        elif button_text == "Backspace":
            self.current_value.set(self.current_value.get()[:-1])
        elif button_text == "AC":
            self.current_value.set("")
        else:
            self.current_value.set(self.current_value.get() + button_text)

if __name__ == "__main__":
    app = CalculatorApp()
    for i in range(7):
        app.grid_rowconfigure(i, weight=1)
    for i in range(4):
        app.grid_columnconfigure(i, weight=1)
    app.mainloop()
