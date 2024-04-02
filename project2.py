import tkinter as tk
import time
import os
from random import choice,shuffle
import csv
import numpy as np
start_time = None
data_dir = os.path.join(os.path.expanduser('~'))
paragraph = None 
def start_typing_on_keypress(event):
    global start_time
    if start_time is None:
        start_typing_test()
        
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    
def reset_time_and_colors():
    global start_time, time_left
    start_time = None
    time_left = 60
    reset_colors()
    timer_label.config(text="Time left: 60 seconds")

def reset_highlight():
    paragraph_entry.tag_remove("highlight", "1.0", "end")
def start_typing_test(event=None):
    global total_words_typed, correct_words_typed, errors, last_input
    total_words_typed = 0
    correct_words_typed = 0
    errors = []
    
    collect_correct_words()
    text_entry.config(state="normal")




   
    reset_highlight()
    reset_time_and_colors()  # Call the new function to reset time and colors
    last_input = ""
    
    text_entry.config(fg="white")


def update_timer():
    global time_left, start_time
    if start_time is not None:
        if time_left > 0:
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:  # Add this check
                wpm = int((total_words_typed / elapsed_time) * 60)
                time_left = max(60 - int(elapsed_time), 0)
                timer_label.config(text=f"Time left: {time_left} seconds | WPM: {wpm} ")
            else:
                wpm = 0
            root.after(1000, update_timer)
        else:
            end_typing_test()
    else:
        timer_label.config(text="Time left: 60 seconds")




def copy_misspelled_content():
    misspelled_content = misspelled_display.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(misspelled_content)
    root.update()


    
def save_misspelled_words():
    misspelled_content = misspelled_display.get("1.0", tk.END).strip()
    if misspelled_content:
        misspelled_words = [line.split() for line in misspelled_content.split('\n')]
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        file_path = os.path.join(desktop_path, 'misspelled_words.csv')
        append_mode = 'a' if os.path.exists(file_path) else 'w'
        with open(file_path, mode=append_mode, newline='') as file:
            writer = csv.writer(file)
            if append_mode == 'w':
                writer.writerow([ 'Misspelled Word','Correct Word','Error Type'])
            writer.writerows(misspelled_words)




def end_typing_test():
    global start_time
    elapsed_time = time.time() - start_time

    if elapsed_time > 0:
        wpm = int((total_words_typed / elapsed_time) * 60)
    else:
        wpm = 0

    accuracy = int((correct_words_typed / total_words_typed) * 100) if total_words_typed > 0 else 0
    result_label.config(text=f'Your typing speed: {wpm} WPM')
    feedback_label.config(text=f'Accuracy: {accuracy}%')
    text_entry.config(state="disabled")
    # Save misspelled words
    save_misspelled_words()

    # Reset colors
    


    

    
    # Make sure collect_correct_words is defined and called
    collect_correct_words()



def copy_misspelled_content():
    misspelled_content = misspelled_display.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(misspelled_content)
    root.update()



def load_paragraphs_from_text():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    text_file_path = os.path.join(script_directory, 'data.txt')

    print(f"Attempting to open file: {text_file_path}")

   

    if os.path.exists(text_file_path):
        with open(text_file_path, 'r') as file:
            words = file.read().split()
            
            shuffle(words)
            
        # Shuffle the words while ensuring words with the same first letter are not adjacent
        grouped_words = {}
        for word in words:
            first_letter = word[0].lower()
            if first_letter not in grouped_words:
                grouped_words[first_letter] = [word]
            else:
                grouped_words[first_letter].append(word)
        
        shuffled_paragraph = []
        while grouped_words:
            for first_letter, words_list in list(grouped_words.items()):
                shuffled_paragraph.append(words_list.pop())
                if not words_list:
                    del grouped_words[first_letter]

        return ' '.join(shuffled_paragraph)
    else:
        print("File not found.")

    return "No words available."





    # Reset colors
def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = np.zeros((m + 1, n + 1))
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
    return dp[m][n]

def determine_error_type(correct_word, misspelled_word):
    distance = levenshtein_distance(correct_word, misspelled_word)
    if distance == 0:
        return "Correct-Spelling"
    elif distance == 1:
        return "Missing-Letters"
    elif distance == len(correct_word) - len(misspelled_word):
        return "Missing-Letters"
    elif distance == len(misspelled_word) - len(correct_word):
        return "Extra-Letters"
    elif distance == len(misspelled_word) + len(correct_word):
        return "Extra-Letters" 
    else:
        return "Mixed-Up"   
    
def check_typing(event):
    global paragraph, total_words_typed, correct_words_typed, errors, last_input, start_time

    if start_time is None and event.keysym != "BackSpace":
        start_time = time.time()
        update_timer()

    if event.keysym == "BackSpace":
        return
    user_input = text_entry.get("1.0", tk.END).split()

    paragraph_entry.tag_remove("correct", "1.0", "end")
    paragraph_entry.tag_remove("incorrect", "1.0", "end")
    paragraph_entry.tag_remove("highlight", "1.0", "end")

    misspelled_display.config(state="normal")
    misspelled_display.delete('1.0', tk.END)  # Clear previous content

    if user_input:
        current_input = user_input[-1].strip()

        if last_input == " " and text_entry.index(tk.INSERT) < f"1.{len(current_input)}":
            text_entry.mark_set(tk.INSERT, f"1.{len(current_input)+1}")
            text_entry.delete("1.0", tk.END)  # Clear the text entry

        correct_words_typed = 0
        for i in range(min(len(user_input), len(paragraph.split()))):
            correct_word = paragraph.split()[i]
            user_word = user_input[i]

            if current_input and correct_word.startswith(current_input) and correct_word not in user_word:
                start = paragraph_entry.search(current_input, "1.0", "end")
                if start:
                    end = f"{start}+{len(current_input)}c"
                    paragraph_entry.tag_add("highlight",  f"1.{len(' '.join(paragraph.split()[:i]))}", f"1.{len(' '.join(paragraph.split()[:i+1]))}")
                    paragraph_entry.tag_config("highlight", foreground="purple")

            if user_word == correct_word:
                paragraph_entry.tag_add("correct", f"1.{len(' '.join(paragraph.split()[:i]))}", f"1.{len(' '.join(paragraph.split()[:i+1]))}")
                paragraph_entry.tag_config("correct", foreground="green")
                correct_words_typed += 1
            else:
                paragraph_entry.tag_add("incorrect", f"1.{len(' '.join(paragraph.split()[:i]))}", f"1.{len(' '.join(paragraph.split()[:i+1]))}")

                error_type = determine_error_type(correct_word, user_word)
                errors.append((user_word, correct_word, error_type))
                misspelled_display.insert(tk.END, f"{user_word}       {correct_word}          {error_type}\n")
                paragraph_entry.tag_config("incorrect", foreground="red")
        last_input = current_input
        total_words_typed = len(user_input)
        correct_label.config(text=f'Correct Words: {correct_words_typed}')
        accuracy = int((correct_words_typed / total_words_typed) * 100) if total_words_typed > 0 else 0
        feedback_label.config(text=f'Accuracy: {accuracy}%')

        elapsed_time = time.time() - start_time
        wpm = int((total_words_typed / elapsed_time) * 60)
        timer_label.config(text=f"Time left: {time_left} seconds | WPM: {wpm}")

    misspelled_display.config(state="disabled")







   



 
def load_paragraphs_from_file(file_path):
    print(f"Attempting to open file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            words = file.read().split()

        # Shuffle the words
        shuffle(words)

        return ' '.join(words)
    except FileNotFoundError:
        return "File not found."




def disable_backspace(event):
    if event.keysym == 'BackSpace' and start_time is not None:
        return 'break'

    text_entry.bind('<KeyPress>', disable_backspace)



def start_typing_on_keypress(event):
    if start_time is None:
        start_typing_test()


def reset_colors():
    paragraph_entry.tag_remove("correct", "1.0", "end")
    paragraph_entry.tag_remove("incorrect", "1.0", "end")
    paragraph_entry.tag_remove("highlight", "1.0", "end")
    paragraph_entry.tag_remove("Typing", "1.0", "end")

    text_entry.delete('1.0', tk.END)
    misspelled_display.delete('1.0', tk.END)
    text_entry.focus()
    
   
    
    result_label.config(text="")
    feedback_label.config(text="")


    paragraph_entry.yview_moveto(0.0)

def collect_correct_words():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, 'misspelled_words.csv')

    correct_words = []

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:           
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                correct_word = row[2]
                correct_words.append(correct_word)

    return correct_words

correct_words = collect_correct_words()
correct_words_sentence = ' '.join(correct_words)

with open('collect_words.txt', 'w') as file:
    file.write(correct_words_sentence)






root = tk.Tk()
root.title("Typing Speed Test 6")
root.geometry("1000x1000")
root.configure(bg="#2B2B2B")


mode_frame = tk.Frame(root)
mode_frame.pack(pady=10)

normal_mode_button = tk.Button(mode_frame, text="Normal Mode", command=lambda: switch_mode("Normal"))
normal_mode_button.pack(side="left", padx=10)



misspelled_words_mode_button = tk.Button(mode_frame, text="Misspelled Words Mode",
                                         command=lambda: switch_mode("Misspelled Words"))
misspelled_words_mode_button.pack(side="left", padx=10)


def switch_mode(mode):
    global paragraph
    print(f"Switching mode to {mode}")
    paragraph_entry.config(state="normal")  # Allow modification of the paragraph entry
    paragraph_entry.delete("1.0", tk.END)  # Clear the paragraph entry

    if mode == "Normal":
        paragraph = load_paragraphs_from_text()
    elif mode == "Misspelled Words":
        paragraph = load_paragraphs_from_file('collect_words.txt')
        if paragraph == "File not found." or paragraph == "No words available.":
            print("Error: 'correct_words.txt' not found.")
            paragraph = "No misspelled words available."

    paragraph_entry.insert(tk.END, paragraph)  # Insert the new paragraph
    paragraph_entry.config(state="disabled")  # Disable modification of the paragraph entry

    # Print success or failure message
    try:
        print("Success: 'correct_words.txt' loaded successfully.")
    except Exception as e:
        print(f"Error: Failed to load 'correct_words.txt'. {e}")

    # Update the paragraph_entry label (replace with the correct widget name and method)
    # Assuming you have a label widget, use "config" to update its text
    # paragraph_entry.config(text=f"Paragraph: {paragraph}")

    # print(f"Paragraph: {paragraph}")


def left_click(event):
    global start_time

    if start_time is None:
        # Timer is not counting, perform reset actions
        reset_time_and_colors()
        start_typing_test()
    else:
        # Timer is active, make it a simple left-click
        pass

paragraph_entry = tk.Text(root, wrap="word", state="normal", height=6, width=60, font=("Helvetica", 20), bg="#2B2B2B", fg="white")
def disable_left_click(event):
    # Disable left mouse button click
    return 'break'

# Iterate over all widgets in the root window and bind the disable_left_click function
for widget in root.winfo_children():
    if isinstance(widget, tk.Button):
        widget.bind("<Button-1>", disable_left_click)

paragraph_entry.tag_configure("correct", foreground="green")
paragraph_entry.tag_configure("incorrect", foreground="red")
#paragraph_entry.tag_configure("Typing", background="gray")
#paragraph_entry.tag_configure("highlight", background="gray")

paragraph_entry.bind("<KeyRelease>", check_typing)
paragraph_entry.config(state="disabled")
paragraph_entry.pack(padx=10, pady=(2, 8))
def update_paragraph_scroll(*args):
    fraction = text_entry.yview()[0]
    paragraph_entry.yview_scroll(int(fraction * 2), "unit")  # Adjusted multiplier


text_entry = tk.Text(root, wrap="word", state="normal", height=2, width=60, font=("Helvetica", 24), bg="#2B2B2B", fg="white", insertbackground="red")
text_entry['yscrollcommand'] = update_paragraph_scroll
text_entry.pack(padx=10, pady=10)
text_entry.bind("<Button-1>", lambda event: reset_time_and_colors())
text_entry.bind("<Key>", start_typing_on_keypress)
text_entry.bind("<KeyRelease>", check_typing)
text_entry.tag_configure("cursor", background="red")
text_entry['yscrollcommand'] = update_paragraph_scroll
text_entry.bind("<Button-1>", left_click)
start_button = tk.Button(root, text="Reset", command=lambda: start_typing_test() )


start_button.pack(pady=10)
start_button.bind("<Button-1>", left_click)
timer_label = tk.Label(root, text="Time left: 60 seconds", font=("Helvetica", 20), bg="#2B2B2B", fg="white")
timer_label.pack(pady=10)
feedback_label = tk.Label(root, text="", font=("Helvetica", 16), bg="#2B2B2B", fg="white")
feedback_label.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 16), bg="#2B2B2B", fg="white")
result_label.pack(pady=10)

correct_label = tk.Label(root, text="", font=("Helvetica", 16) , bg="#2B2B2B", fg="white")
correct_label.pack(pady=10)

misspelled_display_label = tk.Label(root, text="Misspelled:", font=("Helvetica", 24), bg="#2B2B2B", fg="white")
misspelled_display_label.pack(pady=(10, 0))

misspelled_display_frame = tk.Frame(root)
misspelled_display_frame.pack(padx=10, pady=10, fill=tk.BOTH)

# Add labels for "Preceding Word", "Misspelled", "Correct", and "Error"
labels_text = ["Preceding Word", "Misspelled", "Correct", "Error"]
labels_frame = tk.Frame(misspelled_display_frame, bg="#2B2B2B")
for label_text in labels_text:
    label = tk.Label(labels_frame, text=label_text, font=("Helvetica", 16), bg="#2B2B2B", fg="white", padx=5)
    label.pack(side="left", expand=True)

labels_frame.pack(side="top", fill=tk.X)
def disable_enter(event):
    return 'break'

text_entry.bind("<Return>", disable_enter)
paragraph_entry.bind("<Return>", disable_enter)
misspelled_display = tk.Text(misspelled_display_frame, wrap="word", state="normal", height=3, width=60, font=("Helvetica", 16), bg="#2B2B2B", fg="white")
misspelled_display.pack(side="left", fill=tk.BOTH, expand=True)

vertical_scrollbar = tk.Scrollbar(misspelled_display_frame, orient="vertical", command=misspelled_display.yview)
vertical_scrollbar.pack(side="right", fill="y")

misspelled_display.config(yscrollcommand=vertical_scrollbar.set)

# Configure a trace on the yscrollcommand to automatically scroll down
def autoscroll(*args):
    misspelled_display.yview_moveto(1.0)
    
misspelled_display['yscrollcommand'] = autoscroll

# Enable automatic scrolling for the misspelled display
misspelled_display.see("end")



copy_button = tk.Button(root, text="Copy Misspelled", command=copy_misspelled_content)
copy_button.pack(pady=10)

cursor_visible = True



for widget in root.winfo_children():
    if isinstance(widget, tk.Button):
        widget.bind("<Button-1>", start_typing_on_keypress)

root.mainloop()
