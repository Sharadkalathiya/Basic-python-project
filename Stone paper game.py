import tkinter as tk
from tkinter import messagebox
import random

# Initialize main window
root = tk.Tk()
root.title("Rock, Paper, Scissors Game")

# Initialize score variables
user_score = 0
computer_score = 0
two_player_mode = False

# Function to determine winner
def determine_winner(user_choice, player_number):
    global user_score, computer_score
    
    if two_player_mode:
        # Two-player mode
        if player_number == 1:
            player_one_choice.set(user_choice)
            result_text.set("Player 2, make your choice!")
        else:
            player_two_choice.set(user_choice)
            # Determine the result
            result = check_winner(player_one_choice.get(), player_two_choice.get())
            
            # Update result text and scores
            result_text.set(f"Player 1 chose {player_one_choice.get()}. Player 2 chose {user_choice}. {result}")
            update_scores(result, "Player 1", "Player 2")
            ask_play_again()
    else:
        # Computer mode
        computer_choice = random.choice(['Rock', 'Paper', 'Scissors'])
        
        # Determine the result
        result = check_winner(user_choice, computer_choice)
        
        # Update result text and scores
        result_text.set(f"You chose {user_choice}. The computer chose {computer_choice}. {result}")
        update_scores(result, "You", "Computer")
        ask_play_again()

# Function to check winner
def check_winner(choice1, choice2):
    if choice1 == choice2:
        return "It's a Tie!"
    elif (choice1 == 'Rock' and choice2 == 'Scissors') or \
         (choice1 == 'Paper' and choice2 == 'Rock') or \
         (choice1 == 'Scissors' and choice2 == 'Paper'):
        return "You Win!" if not two_player_mode else "Player 1 Wins!"
    else:
        return "You Lose!" if not two_player_mode else "Player 2 Wins!"

# Function to update scores
def update_scores(result, winner_label, loser_label):
    global user_score, computer_score
    
    if "Win" in result:
        user_score += 1
    elif "Lose" in result:
        computer_score += 1
    
    score_text.set(f"{winner_label}'s Score: {user_score} | {loser_label}'s Score: {computer_score}")

# Function to ask if user wants to play again
def ask_play_again():
    play_again = messagebox.askyesno("Play Again", "Do you want to play another round?")
    if not play_again:
        root.quit()

# Function to choose game mode
def choose_mode():
    global two_player_mode
    mode = mode_var.get()
    if mode == "Computer":
        two_player_mode = False
    else:
        two_player_mode = True
    reset_game()

# Function to reset the game
def reset_game():
    global user_score, computer_score
    user_score = 0
    computer_score = 0
    player_one_choice.set("")
    player_two_choice.set("")
    result_text.set("Make your choice!")
    score_text.set(f"Your Score: {user_score} | Computer Score: {computer_score}")

# Function to exit the game
def exit_game():
    messagebox.showinfo("Exit Game", "Thanks for playing!")
    root.quit()

# Setting up the GUI layout
result_text = tk.StringVar()
result_text.set("Choose mode to start the game!")
score_text = tk.StringVar()
score_text.set(f"Your Score: {user_score} | Computer Score: {computer_score}")
player_one_choice = tk.StringVar()
player_two_choice = tk.StringVar()

# Mode selection
mode_var = tk.StringVar(value="Computer")
mode_label = tk.Label(root, text="Choose Mode:", font=('Arial', 12))
mode_label.pack(pady=5)
mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)
computer_mode_button = tk.Radiobutton(mode_frame, text="Play Against Computer", variable=mode_var, value="Computer", command=choose_mode)
computer_mode_button.grid(row=0, column=0, padx=10)
two_player_mode_button = tk.Radiobutton(mode_frame, text="Two Player Mode", variable=mode_var, value="Two Player", command=choose_mode)
two_player_mode_button.grid(row=0, column=1, padx=10)

# Result label
result_label = tk.Label(root, textvariable=result_text, font=('Arial', 14))
result_label.pack(pady=20)

# Score label
score_label = tk.Label(root, textvariable=score_text, font=('Arial', 12))
score_label.pack(pady=10)

# Buttons for user choices with emojis
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

rock_button = tk.Button(button_frame, text="🪨 Rock", width=10, command=lambda: determine_winner('Rock', 1 if not two_player_mode or player_one_choice.get() == "" else 2))
rock_button.grid(row=0, column=0, padx=10)

paper_button = tk.Button(button_frame, text="📄 Paper", width=10, command=lambda: determine_winner('Paper', 1 if not two_player_mode or player_one_choice.get() == "" else 2))
paper_button.grid(row=0, column=1, padx=10)

scissors_button = tk.Button(button_frame, text="✂️ Scissors", width=10, command=lambda: determine_winner('Scissors', 1 if not two_player_mode or player_one_choice.get() == "" else 2))
scissors_button.grid(row=0, column=2, padx=10)

# Exit button
exit_button = tk.Button(root, text="Exit Game", command=exit_game)
exit_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
