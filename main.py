from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import Entry, Button, OptionMenu
import random
import cv2
import numpy as np
import os


class Tiles():
    def __init__(self):
        self.tiles = []

    def add(self, tile):
        self.tiles.append(tile)

    def shuffle(self):
        random.shuffle(self.tiles)
        i = 0
        for row in range(4):
            for col in range(4):
                self.tiles[i].pos = (row, col)
                i += 1

    def show(self):
        for tile in self.tiles:
            tile.show()


class Tile(Label):
    def __init__(self, parent, image, pos):
        Label.__init__(self, parent, image=image)

        self.image = image
        self.pos = pos

    def show(self):
        self.grid(row=self.pos[0], column=self.pos[1])


class Board(Frame):
    BOARD_SIZE = 400

    def __init__(self, parent, image, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.image = self.openImage(image)
        self.tileSize = self.image.size[0] / 4
        self.tiles = self.createTiles()
        self.tiles.shuffle()
        self.tiles.show()

    def openImage(self, image):
        image = Image.open(image)
        # if min(image.size) > self.BOARD_SIZE:
        image = image.resize((self.BOARD_SIZE, self.BOARD_SIZE), Image.ANTIALIAS)
        # if image.size[0] != image.size[1]:
        #     image = image.crop((0, 9, image.size[0], image.size[0]))
        return image

    def createTiles(self):
        tiles = Tiles()
        for row in range(4):
            for col in range(4):
                x0 = col * self.tileSize
                y0 = row * self.tileSize
                x1 = x0 + self.tileSize
                y1 = y0 + self.tileSize
                tileImage = ImageTk.PhotoImage(self.image.crop((x0, y0, x1, y1)))
                tile = Tile(self, tileImage, (row, col))
                tiles.add(tile)
        return tiles


class Main():
    def __init__(self, parent):
        self.parent = parent

        self.image = StringVar()

        self.createWidgets()

    def createWidgets(self):
        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame, text='Puzzle Oyunu', font=('', 50)).pack(padx=10, pady=10)
        frame = Frame(self.mainFrame)
        Label(frame, text='Image').grid(sticky=W)
        Entry(frame, textvariable=self.image, width=50).grid(row=0, column=1, pady=10, padx=10)
        Button(frame, text='Aç', command=self.browse).grid(row=0, column=2, pady=10, padx=10)
        frame.pack(padx=10, pady=10)
        Button(self.mainFrame, text='Başla', command=self.start).pack(padx=10, pady=10)
        self.mainFrame.pack()
        self.board = Frame(self.parent)
        self.winFrame = Frame(self.parent)

    def browse(self):
        self.image.set(filedialog.askopenfilename(title='Please select one (any) frame from your set of images.',
                                                  filetypes=[('Image Files', ['.jpeg', '.jpg', '.png', '.gif',
                                                                              '.tiff', '.tif', '.bmp'])]))

    def start(self):
        image = self.image.get()
        if os.path.exists(image):
            self.board = Board(self.parent, image)
            self.mainFrame.pack_forget()
            self.board.pack()


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def test_similar(img1, img2):
    h, w, d = img1.shape
    total = h * w * d
    diff = cv2.absdiff(img1, img2)
    num = (diff < 1).sum()
    return num * 100.0 / total


def get_image_piece(img, i, j):
    # if not (0 < i < 5 | 0 < j < 5): error!
    try:
        image_box = img
        h = image_box.shape[0]
        box_length = int(h / 4)
        return image_box[0 + box_length * i:100 + box_length * i, 0 + box_length * j:100 + box_length * j, :]
    except:
        print("slice error!")


def get_loaction(arr, xy):
    for i in range(0, 4):
        for j in range(0, 4):
            if arr[i][j] == xy:
                return i, j


# def main():
# mantıksal hatalar
# tsetimg = cv2.imread('karisik1.jpg')
# indexes = np.arange(16)
# random.shuffle(indexes)
# j = 0
# suffled_indexes = []
# for i in chunks(indexes, 4):
#     suffled_indexes.append(i)
#     j = j + 1
# print(suffled_indexes)
# print(get_loaction(suffled_indexes, 11))
# i, j = get_loaction(suffled_indexes, 11)
# get_image_piece(tsetimg, i, j)
####

# imageA = cv2.imread("/Users/burakcokyildirim/Desktop/Screen Shot 2019-03-15 at 17.53.51.png")
# imageB = cv2.imread("/Users/burakcokyildirim/Desktop/Screen Shot 2019-03-15 at 17.53.51.png")
# root = Tk()
# app = MainFrame(root)
# app.pack(fill="both", expand=True)
# root.mainloop()


if __name__ == "__main__":
    # main()
    root = Tk()
    root.title("Puzzle Oyunu")
    Main(root)
    root.mainloop()
    '''
    https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
    https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    https://www.programcreek.com/python/example/89428/cv2.absdiff
    https://docs.opencv.org/2.4.13.7/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
    '''
