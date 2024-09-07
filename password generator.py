import random
import string
from tkinter import *

# Initialize the main window
root = Tk()
root.title("Password Generator")  # Set the app title

# Create a frame to hold the widgets
frame = Frame(root)
frame.pack()

# Global variables for the password and character pool
randompass = ''
character = ''

# Variables to store the user's options and password length
data = IntVar()
check_digit = IntVar()
check_lower = IntVar()
check_upper = IntVar()
check_special = IntVar()

# Function to generate the password based on selected options
def generate():
    global character
    localcharacter = character  # Local copy of the character set
    length = data.get()  # Get the desired password length from user input
    
    global randompass
    randompass = ''  # Reset the password before generating a new one

    # Check if at least one character type is selected
    if len(localcharacter) > 0:
        if length > 1:  # Ensure the password length is greater than 1
            for i in range(length):
                newpass = random.choice(localcharacter)  # Randomly select characters
                randompass += newpass  # Add selected character to the password

            print(randompass)  # Print the generated password to the console
            password_label.config(text=randompass, fg='black')  # Display the password in the UI
        else:
            password_label.config(text="Length cannot be Zero", fg='red')  # Error message if length is 0 or 1
    else:
        password_label.config(text="Select at least one character type", fg='red')  # Error message if no character type is selected

# Function to add/remove digits from the character pool based on user selection
def cdigit():
    global character
    if check_digit.get() == 1:  # If the digit checkbox is selected
        character += string.digits  # Add digits to the character pool
        print(character)
    elif check_digit.get() == 0:  # If the digit checkbox is deselected
        character = character.replace(string.digits, '')  # Remove digits from the character pool
        print(character)

# Function to add/remove lowercase letters from the character pool based on user selection
def clower():
    global character
    if check_lower.get() == 1:  # If the lowercase checkbox is selected
        character += string.ascii_lowercase  # Add lowercase letters to the character pool
        print(character)
    elif check_lower.get() == 0:  # If the lowercase checkbox is deselected
        character = character.replace(string.ascii_lowercase, '')  # Remove lowercase letters from the character pool
        print(character)

# Function to add/remove uppercase letters from the character pool based on user selection
def cupper():
    global character
    if check_upper.get() == 1:  # If the uppercase checkbox is selected
        character += string.ascii_uppercase  # Add uppercase letters to the character pool
        print(character)
    elif check_upper.get() == 0:  # If the uppercase checkbox is deselected
        character = character.replace(string.ascii_uppercase, '')  # Remove uppercase letters from the character pool
        print(character)

# Function to add/remove special characters from the character pool based on user selection
def cspecial():
    global character
    if check_special.get() == 1:  # If the special characters checkbox is selected
        character += '$&!@*'  # Add special characters to the character pool
        print(character)
    elif check_special.get() == 0:  # If the special characters checkbox is deselected
        character = character.replace('$&!@*', '')  # Remove special characters from the character pool
        print(character)

# Create a label frame to organize the UI elements
info_frame = LabelFrame(frame)
info_frame.grid(row=0, column=0)

# Label and entry field for password length input
length_label = Label(info_frame, text="Enter Length of Password")
length_label.grid(row=0, column=0)

length_entry = Entry(info_frame, textvariable=data)  # Entry widget to input the desired password length
length_entry.grid(row=1, column=0)

# Checkboxes to select the types of characters to include in the password
checkbutton_digit = Checkbutton(info_frame, text="Digit", variable=check_digit, command=cdigit)
checkbutton_digit.grid(row=2, column=0)

checkbutton_lower = Checkbutton(info_frame, text="Lower case", variable=check_lower, command=clower)
checkbutton_lower.grid(row=2, column=1)

checkbutton_upper = Checkbutton(info_frame, text="Upper case", variable=check_upper, command=cupper)
checkbutton_upper.grid(row=3, column=0)

checkbutton_special = Checkbutton(info_frame, text="Special characters", variable=check_special, command=cspecial)
checkbutton_special.grid(row=3, column=1)

# Button to generate the password based on user input
btn = Button(info_frame, text="Generate", command=generate)
btn.grid(row=4, column=0, columnspan=2, pady=10)

# Label to display the generated password
password_label = Label(info_frame, text=randompass)
password_label.grid(row=5, column=0, columnspan=2)

# Apply padding to all widgets within the info frame for better UI spacing
for widget in info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
