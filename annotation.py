from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
from tkFileDialog import askdirectory
import os
import unicodedata, time, math

if __name__ == "__main__":
    global coordinatesClicked
    root = Tk()
    imageNumber = 0
    coordinatesLogged = 0
    xCoords = []
    yCoords = []

    #SETTINGS
    zoom = 4

    #canvas setup
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #directory selection
    Directory = askdirectory(parent=root, initialdir="C:/",title='Choose the directory')
    imagesToProcess = []
    imageNames = []

    #image gathering
    for filename in os.listdir(Directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            canvas.delete("all")
            name = unicodedata.normalize('NFKD', filename).encode('ascii','ignore')
            filepath = os.path.join(Directory + os.sep, name).replace("\\", "/")
            image = Image.open(filepath)
            image = image.resize((1280*zoom, 738*zoom), Image.ANTIALIAS)
            root.img = img = ImageTk.PhotoImage(image)
            print filepath + "!"
            imageNames.append(filename[:-4])
            imagesToProcess.append(img)

    #onclick action
    def logcoords(event):
        #outputting x and y coords to console
        # print (event.x,event.y)
        global imageNumber, coordinatesLogged, xCoords, yCoords
        xCoords.append(int(math.floor(canvas.canvasx(event.x)/zoom)))
        yCoords.append(int(math.floor(canvas.canvasy(event.y)/zoom)))
        coordinatesLogged += 1
        if coordinatesLogged == 4:
            lineToWrite = imageNames[imageNumber] + ": (" + str(min(yCoords)) + ", " + str(min(xCoords)) + ", " + str(max(yCoords)) + ", " + str(max(xCoords)) + ")"
            xCoords = []
            yCoords = []
            coordinatesLogged = 0
            imageNumber += 1
            with open("label.txt", "a") as myfile:
                myfile.write(lineToWrite)
                myfile.write("\n")

            if imageNumber != len(imageNames):
                canvas.itemconfig(imageDisplayed, image = imagesToProcess[imageNumber])
            else:
                root.destroy()


    #undo functionality (not implemented)

    # def unlogcoords():
    #     print "deleted last coordinate"
    #     global imageNumber, coordinatesLogged
    #     coordinatesLogged -= 1
    #     if coordinatesLogged == 0:
    #         coordinatesLogged = 3
    #         imageNumber -= 1
    #         canvas.itemconfig(imageDisplayed, image = imagesToProcess[imageNumber])

    #display first image
    imageDisplayed = canvas.create_image(0,0,image=imagesToProcess[imageNumber],anchor="nw")
    #set scroll bars
    canvas.config(scrollregion=canvas.bbox(ALL))

    canvas.bind("<Button 1>", logcoords)
    # canvas.bind("<Key>", unlogcoords)
    root.mainloop()