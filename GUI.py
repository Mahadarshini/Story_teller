import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import requests
import json
import threading
import pyttsx3

# Flask API URL
API_URL = "http://127.0.0.1:5000/generate_story"

# Initialize Text-to-Speech Engine
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)  # Speed of speech

def type_story(text, index=0):
    if index < len(text):
        story_text.insert(tk.END, text[index])
        story_text.after(50, type_story, text, index + 1)  # Adjust speed with '50'

def display_story():
    story_text.delete("1.0", tk.END)  # Clear previous text
    story = "Clementine, a ginger cat with a perpetually unimpressed expression, ruled the sunbeam..."
    type_story(story)  # Call animation function

def get_story():
    prompt = prompt_entry.get()
    
    if not prompt.strip():
        messagebox.showwarning("Input Error", "Please enter a story prompt.")
        return

    # Show Loading Message
    story_text.delete("1.0", tk.END)
    story_text.insert(tk.END, "Generating story... Please wait.")
    
    # Fetch story in a separate thread to avoid UI freezing
    def fetch_story():
        try:
            response = requests.post(API_URL, json={"prompt": prompt})
            result = response.json()

            if "story" in result:
                story_text.delete("1.0", tk.END)
                story_text.insert(tk.END, result["story"])
            else:
                messagebox.showerror("Error", result.get("error", "Unknown error"))
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Connection Error", "Failed to connect to the server.\nIs Flask running?")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=fetch_story, daemon=True).start()

def save_story():
    story = story_text.get("1.0", tk.END).strip()
    if not story:
        messagebox.showwarning("No Story", "There's no story to save!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(story)
        messagebox.showinfo("Saved", "Story saved successfully!")

def read_story():
    story = story_text.get("1.0", tk.END).strip()
    if not story:
        messagebox.showwarning("No Story", "There's no story to read!")
        return
    
    # Run Text-to-Speech in a separate thread
    def speak():
        tts_engine = pyttsx3.init()
        tts_engine.setProperty("rate", 150)  # Adjust speed
        tts_engine.say(story)
        tts_engine.runAndWait()

    threading.Thread(target=speak, daemon=True).start()

# Create GUI Window
root = tk.Tk()
root.title("AI Story Generator")
root.geometry("650x450")
root.configure(bg="#222222")  # Dark Mode Background

# Styling
label_fg = "#ffffff"
button_bg = "#444444"
text_bg = "#333333"
text_fg = "#ffffff"

# Prompt Input
tk.Label(root, text="Enter a story topic:", fg=label_fg, bg="#222222", font=("Arial", 12)).pack(pady=5)
prompt_entry = tk.Entry(root, width=50, bg=text_bg, fg=text_fg, insertbackground="white", font=("Arial", 12))
prompt_entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#222222")
button_frame.pack(pady=5)

generate_button = tk.Button(button_frame, text="Generate Story", bg=button_bg, fg="white", command=get_story)
generate_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(button_frame, text="Save Story", bg=button_bg, fg="white", command=save_story)
save_button.grid(row=0, column=1, padx=5)

read_button = tk.Button(button_frame, text="Read Story", bg=button_bg, fg="white", command=read_story)
read_button.grid(row=0, column=2, padx=5)

# Story Output Box
story_text = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD, bg=text_bg, fg=text_fg, font=("Arial", 12))
story_text.pack(pady=10)

# Run Tkinter Main Loop
root.mainloop()


