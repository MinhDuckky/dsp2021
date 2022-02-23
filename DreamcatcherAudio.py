import wave
from tkinter import *
from tkinter import filedialog

filepath = "" 

def browseFiles():
    global filepath
    filepath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = [("Audio Files",
                                                        ".wav")])
    # Change label contents
    filename = filepath.split("/")[-1]
    label_file_explorer.configure(text="File Opened: " + filename)
    return filepath

def encode(filepath, text):
    audio = wave.open("{}".format(filepath) ,mode="rb")
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    string = text.get("1.0",'end-1c')
    string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)

    filetypes = [('Audio Files', '.wav')]
    file = filedialog.asksaveasfile(initialdir = "/", 
                                    title = "Save As", 
                                    filetypes = filetypes, 
                                    defaultextension = '.wav')
    newAudio =  wave.open(file.name, 'wb')
    newAudio.setparams(audio.getparams())
    newAudio.writeframes(frame_modified)
    newAudio.close()
    audio.close()

def decode(frame):
    filepath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = [("Audio Files",
                                                        ".wav")])
    audio = wave.open("{}".format(filepath), mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    decoded = string.split("###")[0]

    for widget in frame.winfo_children():           # Reset frame
        widget.destroy()
    canvas = Canvas(frame, bg = "black")
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

    canvas.create_window((0, 0), window = scrollable_frame, anchor ="nw", width = 570)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    frame_message = Message(scrollable_frame, 
                            text = decoded,
                            anchor = W,
                            justify = LEFT,
                            width = 550,
                            bg = "black", 
                            fg = "white", 
                            font = ("Courier New", 11))
    frame_message.pack(fill = BOTH)

    audio.close()

def down(x):
    for i in range(x):
        temp = Label(window)
        temp.pack()
                                                                            
# Create the root window
window = Tk()
  
# Set window title
window.title('Dreamcatcher Audio')

width = 600
height = 600
screen_width = window.winfo_screenwidth()             # Get your screen width
screen_height = window.winfo_screenheight()           # Get your screen height

x = (screen_width / 2) - (width / 2)
y = (screen_height /2) - (height / 2)
window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')      # Pop up window at the center of the screen

window.resizable(0, 0)
  
# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "Choose an audio file",
                            width = 40,
                            height = 4)

label = Label(window,
            text = "Enter your message :",
            width = 40,
            height = 2,
            anchor = S)
  
      
button_explore = Button(window,
                        text = "Browse Files",
                        width = 17,
                        command = browseFiles)
button_encode = Button(window,
                        text = "Encode Audio File",
                        anchor = N,
                        command = lambda: encode(filepath, text))
button_decode = Button(window,
                        text = "Decode Audio File",
                        command = lambda: decode(frame))

text = Text(window, wrap = WORD)
ScrollBar = Scrollbar(text)
ScrollBar.config(command=text.yview)
text.config(yscrollcommand=ScrollBar.set)
ScrollBar.pack(side=RIGHT, fill= Y)


label_file_explorer.pack()

button_explore.pack()
label.pack()
text.pack(fill = X, ipady = 60)
button_encode.pack()        #                                                                          #
line = Label(window, text = "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
line.pack()
button_decode.pack()
frame = LabelFrame(window, text = "HIDDEN MESSAGE")        # Create new frame
frame.pack(fill = X)

canvas = Canvas(frame, bg = "black")
scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

canvas.create_window((0, 0), window = scrollable_frame, anchor ="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


  
# Let the window wait for any events
window.mainloop()