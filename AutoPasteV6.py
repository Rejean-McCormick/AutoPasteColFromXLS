import pyautogui
import pyperclip
import time
import tkinter as tk
from tkinter import messagebox

def paste_text(x, y, text, send_x, send_y, wait_time):
    """
    Pastes the text at the specified x, y coordinates and clicks the send button located at send_x, send_y.
    """
    pyautogui.click(x, y)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.click(send_x, send_y)
    time.sleep(wait_time)

def run_program():
    """
    Executes the program based on the user-provided parameters.
    """
    global input_x, input_y, send_x, send_y

    try:
        wait_time = int(wait_var.get())
        iterations = int(iterations_var.get())
        start_number = int(start_number_var.get()) if increment_enabled.get() else None
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for iterations, wait time, and starting number.")
        return

    # Collect sentences and validate activation checkboxes
    sentences = []
    if sentence1_enabled.get():
        sentences.append(sentence1_var.get())
    if sentence2_enabled.get():
        sentences.append(sentence2_var.get())
    if sentence3_enabled.get():
        sentences.append(sentence3_var.get())
    if sentence4_enabled.get():
        sentences.append(sentence4_var.get())

    if not sentences:
        messagebox.showerror("Error", "Please activate and provide at least one sentence.")
        return

    # Generate final text with optional incrementation
    final_text = ""
    current_number = start_number if increment_enabled.get() else None

    for i in range(iterations):
        for sentence in sentences:
            if increment_enabled.get() and current_number is not None:
                final_text += sentence + str(current_number) + "\n"
            else:
                final_text += sentence + "\n"
        if increment_enabled.get() and current_number is not None:
            current_number += 1
        final_text += "\n"  # Add spacing between loops

    # Perform the automated pasting
    paste_text(input_x, input_y, final_text.strip(), send_x, send_y, wait_time)
    messagebox.showinfo("Success", "The text has been pasted successfully!")

def set_paste_position():
    """
    Captures the position for pasting text.
    """
    messagebox.showinfo("Instructions", "Position your cursor over the paste location. You have 3 seconds.")
    time.sleep(3)
    x, y = pyautogui.position()
    paste_pos_var.set(f"X: {x}, Y: {y}")
    global input_x, input_y
    input_x, input_y = x, y

def set_send_position():
    """
    Captures the position for clicking the send button.
    """
    messagebox.showinfo("Instructions", "Position your cursor over the send button. You have 3 seconds.")
    time.sleep(3)
    x, y = pyautogui.position()
    send_pos_var.set(f"X: {x}, Y: {y}")
    global send_x, send_y
    send_x, send_y = x, y

def toggle_sentence(checkbox_var, text_entry):
    """
    Enables or disables the text box for a sentence based on the checkbox state.
    """
    if checkbox_var.get():
        text_entry.config(state="normal")
    else:
        text_entry.delete(0, tk.END)
        text_entry.config(state="disabled")

# Initialize Tkinter
root = tk.Tk()
root.title("Text Pasting Automation")

# Variables
iterations_var = tk.StringVar(value="1")
wait_var = tk.StringVar(value="1")
paste_pos_var = tk.StringVar(value="Not Set")
send_pos_var = tk.StringVar(value="Not Set")
sentence1_var = tk.StringVar()
sentence1_enabled = tk.BooleanVar(value=False)
sentence2_var = tk.StringVar()
sentence2_enabled = tk.BooleanVar(value=False)
sentence3_var = tk.StringVar()
sentence3_enabled = tk.BooleanVar(value=False)
sentence4_var = tk.StringVar()
sentence4_enabled = tk.BooleanVar(value=False)
increment_enabled = tk.BooleanVar(value=False)
start_number_var = tk.StringVar(value="1")

# Iterations
tk.Label(root, text="Number of Iterations:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=iterations_var, width=10).grid(row=0, column=1, sticky="w", padx=10, pady=5)

# Wait Time
tk.Label(root, text="Wait Time (sec):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=wait_var, width=10).grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Increment Option
tk.Checkbutton(root, text="Enable Incrementation", variable=increment_enabled).grid(row=2, column=0, sticky="w", padx=10, pady=5)
tk.Label(root, text="Start Number:").grid(row=2, column=1, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=start_number_var, width=10, state="normal").grid(row=2, column=2, sticky="w", padx=10, pady=5)

# Paste Position
tk.Label(root, text="Paste Position:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
tk.Label(root, textvariable=paste_pos_var).grid(row=3, column=1, sticky="w", padx=10, pady=5)
tk.Button(root, text="Set Position", command=set_paste_position).grid(row=3, column=2, padx=10, pady=5)

# Send Position
tk.Label(root, text="Send Position:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
tk.Label(root, textvariable=send_pos_var).grid(row=4, column=1, sticky="w", padx=10, pady=5)
tk.Button(root, text="Set Position", command=set_send_position).grid(row=4, column=2, padx=10, pady=5)

# Sentence 1
tk.Checkbutton(root, text="Include Sentence 1", variable=sentence1_enabled, command=lambda: toggle_sentence(sentence1_enabled, sentence1_entry)).grid(row=5, column=0, sticky="w", padx=10, pady=5)
sentence1_entry = tk.Entry(root, textvariable=sentence1_var, width=40, state="disabled")
sentence1_entry.grid(row=5, column=1, padx=10, pady=5)

# Sentence 2
tk.Checkbutton(root, text="Include Sentence 2", variable=sentence2_enabled, command=lambda: toggle_sentence(sentence2_enabled, sentence2_entry)).grid(row=6, column=0, sticky="w", padx=10, pady=5)
sentence2_entry = tk.Entry(root, textvariable=sentence2_var, width=40, state="disabled")
sentence2_entry.grid(row=6, column=1, padx=10, pady=5)

# Sentence 3
tk.Checkbutton(root, text="Include Sentence 3", variable=sentence3_enabled, command=lambda: toggle_sentence(sentence3_enabled, sentence3_entry)).grid(row=7, column=0, sticky="w", padx=10, pady=5)
sentence3_entry = tk.Entry(root, textvariable=sentence3_var, width=40, state="disabled")
sentence3_entry.grid(row=7, column=1, padx=10, pady=5)

# Sentence 4
tk.Checkbutton(root, text="Include Sentence 4", variable=sentence4_enabled, command=lambda: toggle_sentence(sentence4_enabled, sentence4_entry)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
sentence4_entry = tk.Entry(root, textvariable=sentence4_var, width=40, state="disabled")
sentence4_entry.grid(row=8, column=1, padx=10, pady=5)

# Run Button
tk.Button(root, text="Run", command=run_program, bg="green", fg="white").grid(row=9, column=0, columnspan=3, pady=20)

# Start Tkinter Loop
root.mainloop()
