from tkinter import *
from PIL import Image

root = Tk()

root.geometry("800x550")
root.config(background="#108cff")

gifImage = "five_seconds.gif"

openImage = Image.open(gifImage)
frames = openImage.n_frames
imageObject = [PhotoImage(file=gifImage,format=f"gif -index {i}") for i in range(frames)]

count = 0
showAnimation = None

def animation(count):
    global showAnimation
    newImage = imageObject[count]
    gif_Label.configure(image=newImage)
    count += 1
    if count == frames:
        count = 0   
    showAnimation = root.after(5000,lambda:animation(count))

root.mainloop()