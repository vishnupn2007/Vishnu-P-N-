import tkinter as tk
import threading
import sounddevice as sd
import numpy as np
import time

MORSE_CODE = {
    # Letters
    "A": ".-",     "B": "-...",   "C": "-.-.",   "D": "-..","E": ".",      "F": "..-.",   "G": "--.",    "H": "....",
    "I": "..",     "J": ".---",   "K": "-.-",    "L": ".-..","M": "--",     "N": "-.",     "O": "---",    "P": ".--.",
    "Q": "--.-",   "R": ".-.",    "S": "...",    "T": "-","U": "..-",    "V": "...-",   "W": ".--",    "X": "-..-",
    "Y": "-.--",   "Z": "--..","0": "-----",  "1": ".----",  "2": "..---",  "3": "...--","4": "....-",  "5": ".....",  "6": "-....",  "7": "--...","8": "---..",  "9": "----.",
    ".": ".-.-.-",",": "--..--","?": "..--..","'": ".----.","!": "-.-.--","/": "-..-.","(": "-.--.",")": "-.--.-","&": ".-...",":": "---...",
    ";": "-.-.-.","=": "-...-","+": ".-.-.","-": "-....-","_": "..--.-","\"": ".-..-.","$": "...-..-","@": ".--.-.",
    " ": "/"
}
sample_rate=44100;fq=800
t_dot = np.linspace(0, 200.0/1000.0, int(sample_rate * 200.0/1000.0 ), endpoint=False)
t_dash = np.linspace(0, 600.0/1000.0, int(sample_rate * 600.0/1000.0), endpoint=False)
dot_sound = np.sin(2 * np.pi * fq * t_dot).astype(np.float32)
dash_sound = np.sin(2 * np.pi * fq * t_dash).astype(np.float32)
def play_sound(c):
    if c == ".":
        threading.Thread(target=lambda: sd.play(dot_sound, sample_rate,blocking=False)).start()    
    elif c == "-":
        threading.Thread(target=lambda: sd.play(dash_sound, sample_rate,blocking=False)).start()
    sd.wait()
def text_to_morse(text):
    result = []
    for ch in text.upper():
        if ch in MORSE_CODE:
            result.append(MORSE_CODE[ch])
        elif ch == " ":
            result.append(" ")
    return " ".join(result)

def display_morse(index=0):
    global displayed_text

    if index >= len(morse_string):
        return

    symbol = morse_string[index]
    displayed_text += symbol
    output_label.config(text=displayed_text)

    if symbol == ".":       
        play_sound(symbol)
        delay = 200
    elif symbol == "-":     
        play_sound(symbol)
        delay = 600
    elif symbol == " ":                   
        delay = 700
    else:
        delay=100

    root.after(delay, lambda: display_morse(index + 1))

def start_display():
    global morse_string, displayed_text
    text = entry.get()
    morse_string = text_to_morse(text)
    displayed_text = "" 
    display_morse(0)

root = tk.Tk()
root.configure(bg="black")
root.title("MORSE CODE GENERATOR")
tk.Label(root, text="INPUT MESSAGE :",bg="white",font=("Impact",20,"bold")).pack(pady=20)
entry = tk.Entry(root, width=50)
entry.pack(padx=10,pady=10)
tk.Button(root, text="Show Morse", command=start_display,font=("times roman",10,"bold")).pack(pady=10)
output_label = tk.Label(root, text="", font=("Courier", 24,"bold"))
output_label.pack(pady=10)
root.mainloop()
