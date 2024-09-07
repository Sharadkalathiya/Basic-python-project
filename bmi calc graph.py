import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# BMI Calculation and Categorization
def calculate_bmi(weight, height_feet):
    try:
        weight = float(weight)
        height_feet = float(height_feet)
        if weight <= 0 or height_feet <= 0:
            raise ValueError("Weight and height must be positive numbers.")
        height_meters = height_feet * 0.3048
        bmi = weight / (height_meters ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"
        return bmi, category
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
        return None, None

# Database Operations
def init_db():
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bmi_data
                 (id INTEGER PRIMARY KEY, name TEXT, weight REAL, height_feet REAL, bmi REAL, category TEXT)''')
    conn.commit()
    conn.close()

def save_data(name, weight, height_feet, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO bmi_data (name, weight, height_feet, bmi, category) VALUES (?, ?, ?, ?, ?)",
              (name, weight, height_feet, bmi, category))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bmi_data ORDER BY id ASC")
    data = c.fetchall()
    conn.close()
    return data

# GUI Application
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        
        # Initialize database
        init_db()
        
        # Create GUI Components
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)
        
        tk.Label(self.root, text="Weight (kg)").grid(row=1, column=0)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.grid(row=1, column=1)
        
        tk.Label(self.root, text="Height (feet)").grid(row=2, column=0)
        self.height_entry = tk.Entry(self.root)
        self.height_entry.grid(row=2, column=1)
        
        self.calculate_button = tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=3, column=0, columnspan=2)
        
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.grid(row=4, column=0, columnspan=2)
        
        self.show_graph_button = tk.Button(self.root, text="Show BMI Trend", command=self.show_bmi_trend)
        self.show_graph_button.grid(row=5, column=0, columnspan=2)
        
    def calculate_bmi(self):
        name = self.name_entry.get()
        weight = self.weight_entry.get()
        height_feet = self.height_entry.get()
        
        bmi, category = calculate_bmi(weight, height_feet)
        if bmi is not None:
            self.result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")
            save_data(name, weight, height_feet, bmi, category)
    
    def show_bmi_trend(self):
        data = get_all_data()
        names = [entry[1] for entry in data]
        bmis = [entry[4] for entry in data]

        if len(names) == 0:
            messagebox.showinfo("Info", "No data to show.")
            return
        
        fig, ax = plt.subplots()
        ax.plot(range(len(names)), bmis, marker='o', linestyle='-')
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha="right")
        ax.set_xlabel('Name')
        ax.set_ylabel('BMI')
        ax.set_title('BMI Trend')
        
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
