import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import os

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")  # Set the title of the App
        self.geometry("500x500")  # Set the App size
        self.configure(bg="white")  # Set the background color to white

        self.tasks = []  
        self.create_widgets()  

    def create_widgets(self):
        """Create and place all the widgets in the GUI"""
        
        # Title Label
        title_label = tk.Label(self, text="To-Do List", font=("Arial", 18), bg="white")
        title_label.pack(pady=10)  

        # Task Entry
        self.task_entry = tk.Entry(self, font=("Arial", 14), width=24)
        self.task_entry.pack(pady=10)  

        # Date and Time Entry
        self.date_entry = DateEntry(self, width=16, background='darkblue',
                                    foreground='white', borderwidth=2, year=datetime.now().year)
        self.date_entry.pack(pady=5)

        self.time_entry = tk.Entry(self, font=("Arial", 14), width=10)
        self.time_entry.insert(0, "HH:MM")
        self.time_entry.pack(pady=5)

        # Add Task Button
        add_button = tk.Button(self, text="Add Task", width=10, command=self.add_task)
        add_button.pack(pady=5) 

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self, font=("Arial", 14), width=50, height=10, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)
        
        # Update, Delete, and Edit Buttons
        update_button = tk.Button(self, text="Edit Task", width=10, command=self.update_task)
        update_button.pack(side=tk.LEFT, padx=20, pady=10)

        delete_button = tk.Button(self, text="Delete Task", width=10, command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=20, pady=10)

        # Save and Load Buttons
        save_button = tk.Button(self, text="Save List", width=10, command=self.save_list)
        save_button.pack(side=tk.RIGHT, padx=20, pady=10)

        load_button = tk.Button(self, text="Load List", width=10, command=self.load_list)
        load_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def add_task(self):
        """Add a new task to the task list with optional date and time"""
        
        task = self.task_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        if task: 
           
            task_with_time = f"{task} - {date} {time}" if time != "HH:MM" else task
            self.tasks.append(task_with_time)
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, "HH:MM")
        else:
            
            messagebox.showwarning("Warning", "You must enter a task.")

    def update_task(self):
        """Update the selected task in the list"""
        
        selected_task_index = self.task_listbox.curselection() 
        if selected_task_index:
            task = self.task_entry.get()
            date = self.date_entry.get()
            time = self.time_entry.get()

            if task: 
                
                task_with_time = f"{task} - {date} {time}" if time != "HH:MM" else task
                self.tasks[selected_task_index[0]] = task_with_time  
                self.update_listbox()
                self.task_entry.delete(0, tk.END)
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, "HH:MM")
            else:
                messagebox.showwarning("Warning", "You must enter a task.")
        else:
            messagebox.showwarning("Warning", "You must select a task to update.")

    def delete_task(self):
        """Delete the selected task from the list"""
        
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def save_list(self):
        """Save the current list of tasks to a file"""
        
        # Open a file dialog to save the task list
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for task in self.tasks:
                    file.write(task + "\n")
                    
            # Show confirmation that the list is saved
            messagebox.showinfo("Info", "Task list saved successfully.")

    def load_list(self):
        """Load a list of tasks from a file"""
        
        # Open a file dialog to load a task list
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:  
            with open(file_path, "r") as file:  
                self.tasks = file.read().splitlines()  
            self.update_listbox()  

    def update_listbox(self):
        """Refresh the listbox to display the current list of tasks"""
        
        self.task_listbox.delete(0, tk.END) 
        for task in self.tasks:  
            self.task_listbox.insert(tk.END, task)

if __name__ == "__main__":
    app = TodoApp() 
    app.mainloop()  # For Run the app
