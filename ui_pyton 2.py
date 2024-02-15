from hmac import compare_digest
import customtkinter
import tkinter as tk
import fileinput
import os
import subprocess
import pyttsx3
import threading
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import CENTER
import sys




customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("500x500")




# Function to update a line in a file
def update_file(file_path, old_line, new_line):
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            if line == old_line:
                print(new_line, end="")
            else:
                print(line, end="")

# Function to speak the contents of a file
engine = pyttsx3.init()

tts_thread = None
tts_lock = threading.Lock()  # Add a lock for synchronization

# Shared variable to signal the TTS thread to stop
stop_tts_flag = threading.Event()

def speak_file(file_path):
    global tts_thread, tts_lock
    with tts_lock:  # Acquire the lock to ensure safe stopping
        if tts_thread and tts_thread.is_alive():
            stop_tts_flag.set()  # Signal the thread to stop

            # Wait for the thread to complete
            tts_thread.join()

        stop_tts_flag.clear()  # Reset the stop signal
        if not stop_tts_flag.is_set():
            def tts_thread_function():
                with open(file_path, "r") as f:
                    text = f.read()
                engine.say(text)
                engine.runAndWait()

            tts_thread = threading.Thread(target=tts_thread_function)
            tts_thread.start()


def stop_tts():
    global tts_thread, tts_lock
    with tts_lock:  # Acquire the lock to ensure safe stopping
        stop_tts_flag.set()  # Signal the thread to stop

        # Wait for the thread to complete
        if tts_thread and tts_thread.is_alive():
            tts_thread.join()

# Function to select an image and perform OCR
def select_image():
    filename = customtkinter.filedialog.askopenfilename(title="Select Image File...")

    if filename:
        with open('D:\Downloads\Python_OCR\input\path.txt', 'w') as output_file:
            output_file.write(filename)

        subprocess_popen = subprocess.Popen(["python", "D:\Downloads\Python_OCR\python ocr.py"])
        subprocess_popen.wait()

        with open("D:\Downloads\Python_OCR\output.txt", "r") as output_file:
            output_text = output_file.read()

        text_widget = customtkinter.CTkTextbox(master=root)
        text_widget.insert(tk.END, output_text)
        text_widget.pack(side=tk.LEFT, expand=True, fill='both')
        

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="OCR", font=("Franklin Gothic Demi", 50))
label.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Open Image", command=select_image)
button.pack(pady=12, padx=10)

# Function to trigger the TTS Python file
def trigger_tts():
    global tts_thread

    tts_thread = threading.Thread(target=speak_file, args=("D:\\Downloads\\Python_OCR\\output.txt",))
    tts_thread.start()

# Function to stop the TTS thread
def stop_tts():
    global tts_thread

    if tts_thread and tts_thread.is_alive():
        try:
            tts_thread.terminate()
        except Exception:
            pass

# Function to speak the contents of a file
def speak_file(file_path):
    engine = pyttsx3.init()

    with open(file_path, "r") as f:
        text = f.read()

    engine.say(text)
    engine.runAndWait()




# Create a frame for TTS and Compare buttons
tts_compare_frame = customtkinter.CTkFrame(master=frame)
tts_compare_frame.pack(pady=12)



# Create a "Text to Speech" button
tts_button = customtkinter.CTkButton(master=tts_compare_frame, text="Text to Speech", command=trigger_tts)
tts_button.pack(side="left", padx=5)

# Add space between buttons
space_label = customtkinter.CTkLabel(master=tts_compare_frame, text=" ")
space_label.pack(side="left")


def select_image():
    filename = customtkinter.filedialog.askopenfilename(title="Select Image File...")

    if filename:
        with open('D:\\Downloads\\Python_OCR\\input\\path2.txt', 'w') as output_file:
            output_file.write(filename)

        subprocess_popen = subprocess.Popen(["python", "D:\\Downloads\\Python_OCR\\python ocr2.py"])
        subprocess_popen.wait()

        with open("D:\\Downloads\\Python_OCR\\output2.txt", "r") as output_file:
            output_text = output_file.read()
        
        text_widget = customtkinter.CTkTextbox(master=root)
        text_widget.insert(tk.END, output_text)
        text_widget.pack(side=tk.RIGHT, expand=True, fill='both')
        
        with open("D:\\Downloads\\Python_OCR\\input\\percentage.txt", "r") as percentage_file:
            percentage_file = percentage_file.read()
        
        text_widget = customtkinter.CTkTextbox(master=root)
        text_widget.insert(tk.END, percentage_file)
        text_widget.pack(side=tk.BOTTOM, fill='both')
            
    
button = customtkinter.CTkButton(master=frame, text="Compare", command=select_image)
button.pack(pady=12, padx=10)

def restart_ui():
    python = sys.executable
    subprocess.Popen([python, "ui_pyton 2.py"])
    root.destroy()

# Create a "Reset" button
reset_button = customtkinter.CTkButton(master=root, text="Reset", command=restart_ui)
reset_button.pack(pady=12, padx=10)



root.mainloop()
