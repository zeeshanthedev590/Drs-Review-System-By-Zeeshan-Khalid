import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
from functools import partial
import threading
import time
import imutils


stream = cv2.VideoCapture("clip.mp4")
flag = True


def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    # Play the video in reverse mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 26, fill="black",
                           font="Times 26 bold", text="Decision Pending")
    flag = not flag


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")


def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")


def pending(decision):
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    # 2. Wait for 1 second
    time.sleep(1.5)

    # 3. Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    # 4. Wait for 1.5 second
    time.sleep(2.5)
    # 5. Display out/notout image
    if decision == 'out':
        decisionImg = "out.png"
    else:
        decisionImg = "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


SET_WIDTH = 650
SET_HEIGHT = 368
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
window = tkinter.Tk()
window.title("Drs Review System Kit By Zeeshan Khalid")
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()
btn = tkinter.Button(window, text="<< Previous (fast)",
                     width=50, bg="light green", fg='black', command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)",
                     width=50, bg="light blue", fg='black', command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>",
                     width=50, bg="purple", fg='white', command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>",
                     width=50, bg="Deeppink", fg='white', command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50,
                     bg="red", fg='white', command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out",
                     width=50, bg="green", fg='white', command=not_out)
btn.pack()

window.mainloop()
print("Code Completed")
