import tkinter as tk
import sounddevice as sd
import numpy as np
import time
from PIL import Image, ImageTk
MORSE_CODE = {
    "A": ".-",     "B": "-...",   "C": "-.-.",   "D": "-..","E": ".",      "F": "..-.",   "G": "--.",    "H": "....",
    "I": "..",     "J": ".---",   "K": "-.-",    "L": ".-..","M": "--",     "N": "-.",     "O": "---",    "P": ".--.",
    "Q": "--.-",   "R": ".-.",    "S": "...",    "T": "-","U": "..-",    "V": "...-",   "W": ".--",    "X": "-..-",
    "Y": "-.--",   "Z": "--..",
    "0": "-----",  "1": ".----",  "2": "..---",  "3": "...--","4": "....-",  "5": ".....",  "6": "-....",  "7": "--...","8": "---..",  
    "9": "----.",
    ".": ".-.-.-",",": "--..--","?": "..--..","'": ".----.","!": "-.-.--","/": "-..-.","(": "-.--.",")": "-.--.-","&": ".-...",":": "---...",
    ";": "-.-.-.","=": "-...-","+": ".-.-.","-": "-....-","_": "..--.-","\"": ".-..-.","$": "...-..-","@": ".--.-.",
    " ": "/"
}

# To create and store the audio of sin curve.
sample_rate=44100;fq=800
t_dot = np.linspace(0, 200.0/1000.0, int(sample_rate * 200.0/1000.0 ), endpoint=False)
t_dash = np.linspace(0, 600.0/1000.0, int(sample_rate * 600.0/1000.0), endpoint=False)
dot_sound = np.sin(2 * np.pi * fq * t_dot).astype(np.float32)
dash_sound = np.sin(2 * np.pi * fq * t_dash).astype(np.float32)
blank_sound=np.sin(2 * np.pi * fq * 0).astype(np.float32)
# To play the corresponding audio when called and enhancing time by usinging concept
def play_sound(c):
    if c == ".":
        sd.play(dot_sound, sample_rate,blocking=False)
        output_label.config(text=displayed_text)    
    elif c == "-":
        sd.play(dash_sound, sample_rate,blocking=False)
        output_label.config(text=displayed_text)  
    elif c == " ":
        sd.play(blank_sound, sample_rate,blocking=False)
        output_label.config(text=displayed_text)  
    
#To convert the given text into morse code 
def text_to_morse(text):
    result = []
    for ch in text.upper():
        if ch in MORSE_CODE:
            result.append(MORSE_CODE[ch])
        elif ch == " ":
            result.append(" ")
    return " ".join(result)+" "

# Display the code in the tkinter window
def display_morse(index=0):
    global displayed_text

    if index >= len(morse_string):
        return

    symbol = morse_string[index]
    displayed_text += symbol
    if symbol == ".":       
        play_sound(symbol)
        delay = 200
    elif symbol == "-":     
        play_sound(symbol)
        delay = 500
    elif symbol == " ":   
        play_sound(symbol)                
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
    
# To create tkinter window
root = tk.Tk()
root.geometry("")
root.configure(bg="black")
img=Image.open("FINALIMG.jpg")
bg=ImageTk.PhotoImage(img)
bgl=tk.Label(root,image=bg)
bgl.place(x=0,y=0,relwidth=1,relheight=1)

root.title("MORSE CODE GENERATOR")
tk.Label(root, text="MORSE CODE GENERATOR",bg="black",fg="white", font=("Impact",40)).pack(pady=100)
tk.Label(root, text="INPUT MESSAGE :",bg="black",fg="white",font=("Impact",30)).pack(pady=20)
entry = tk.Entry(root,width=30,fg="white",bg="black",font=("Arial",20))
entry.pack(padx=10,pady=30)
tk.Button(root, text="Show Morse",bg="black",fg="white", command=start_display,font=("times roman",15,"bold")).pack(pady=10)
output_label = tk.Label(root, text="", bg="black",fg="white",font=("Courier", 24,"bold"))
output_label.pack(pady=10)
root.mainloop()
