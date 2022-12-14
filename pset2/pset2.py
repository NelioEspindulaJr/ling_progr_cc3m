#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from turtle import width
from PIL import Image as PILImage

# NO ADDITIONAL IMPORTS ALLOWED!
def kernelMaker(n):
        kernel = [[1/n**2 for index in range(n)]for index in range(n)]
        return kernel

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def get_pixel(self, x, y):

        # CONDICIONAIS QUE, SE X < 0 ou Y < 0, OS PIXELS FORA DO LIMITE X Y
        # TERÃO O MESMO VALOR DO SEU PIXEL ADJACENTE.
        if x < 0:
            x = 0
        elif x >= self.width:
            x = self.width - 1

        if y < 0:
            y = 0
        elif y >= self.height:
            y = self.height - 1

        return self.pixels[(x + y * self.width)]

    def set_pixel(self, x, y, c):
        self.pixels[(x + y * self.width)] = c

    def apply_per_pixel(self, func):
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)
        return result

    def inverted(self):
        return self.apply_per_pixel(lambda c: 255-c)

    def correlated(self, n):
        kernelSize = len(n)
        img = Image.new(self.width, self.height)

        for x in range(self.width):
            for y in range(self.height):
                correlationSum = 0
                for z in range(kernelSize):
                    for w in range(kernelSize):
                        correlationSum += self.get_pixel((x-(kernelSize//2)+z), (y-(kernelSize//2))+w)*n[z][w]
                        # MENÇÃO HONROSA AO COLEGA LUCAS ZANON GUARNIER QUE ME AJUDOU COM ESTE CÓDIGO
                img.set_pixel(x, y, correlationSum)
        return img
                    

    def blurred(self, n):
        kernel = self.correlated(kernelMaker(n))
        kernel.normalizedPixel()
        return kernel


    def normalizedPixel(self):
        for x in range(self.width):
            for y in range(self.height):
                analyzedPixel = self.get_pixel(x,y)

                # CONDICIONAIS IMPEDEM PIXELS DE TEREM VALORES MENORES QUE 0
                # OU MAIORES QUE 255
                if  analyzedPixel < 0:
                    analyzedPixel = 0

                elif analyzedPixel > 255:
                    analyzedPixel = 255
                
                analyzedPixel = round(analyzedPixel)
                # OS PIXELS NAO PODEM TER VALOR FLUTUANTE, POR ISSO ARRENDONDAMOS
                # UTILIZANDO A FUNÇÃO ROUND

                self.set_pixel(x,y, analyzedPixel)
    
    def sharpened(self, n):
        blurredImage = self.blurred(n)
        img = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                sharpenedImageFormula = round(2*self.get_pixel(x,y)-(blurredImage.get_pixel(x,y)))
                img.set_pixel(x, y, sharpenedImageFormula)
        img.normalizedPixel()
        return img

    def edges(self):
        img = Image.new(self.width, self.height)
        kernelSobelX = [[1, 0, -1],
                        [2, 0, -2],
                        [1, 0, -1]]

        kernelSobelY = [[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]]

        SobelXApllied = self.correlated(kernelSobelX)
        SobelYApllied = self.correlated(kernelSobelY)


        for x in range(self.width):
            for y in range(self.height):
                sobelOperation = round(math.sqrt(SobelXApllied.get_pixel(x,y)**2 + SobelYApllied.get_pixel(x,y)**2))
                img.set_pixel(x, y, sobelOperation)
        img.normalizedPixel()
        
        return img



    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    def __repr__(self):
        return "Image(%s, %s, %s)" % (self.width, self.height, self.pixels)

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.
        Invoked as, for example:
           i = Image.load('test_imgs/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.
        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.
        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()

    def reafter():
        tcl.after(500, reafter)
    tcl.after(500, reafter)
except:
    tk_root = None
WINDOWS_OPENED = False




# 3.2 DEBUGGING - INVERSAO DA FOTO DO PEIXE bluegill.png
if __name__ == '__main__':

    # QUESTÃO 2:
    fish = Image.load('test_imgs/bluegill.png')
    InvertedFish = fish.inverted()
    Image.save(InvertedFish, 'question_answers_images/peixe.png')
    
    
    # QUESTAO 4:
    kernel = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    pig = Image.load('test_imgs/pigbird.png')
    correlatedPig = pig.correlated(kernel)
    Image.save(correlatedPig, 'question_answers_images/porco_e_passaro.png')

    #SEÇÃO 5.1 EXERCÍCIO

    cat = Image.load('test_imgs/cat.png')
    BlurredCat = cat.blurred(5)
    Image.save(BlurredCat,'question_answers_images/gato.png')

    #QUESTÃO 5

    python = Image.load('test_imgs/python.png')
    sharpenedPython = python.sharpened(11)
    Image.save(sharpenedPython,'question_answers_images/piton.png')


    #QUESTÃO 6:
    #RESULTADOS INDIVIDUAIS DA APLICAÇÃO DOS KERNELS DA OPERAÇÃO DE SOBEL 

    kernelSobelX = [[1, 0, -1],
                    [2, 0, -2],
                    [1, 0, -1]]

    kernelSobelY = [[1, 2, 1],
                    [0, 0, 0],
                    [-1, -2, -1]]

    construct = Image.load('test_imgs/construct.png')
    constructSobelX = construct.correlated(kernelSobelX)
    Image.save(constructSobelX, 'question_answers_images/construc_sobel_X.png')

    constructSobelY = construct.correlated(kernelSobelY)
    Image.save(constructSobelY, 'question_answers_images/construc_sobel_Y.png')

    edgedConstruct = construct.edges()
    Image.save(edgedConstruct, 'question_answers_images/construcao.png')

    pass

    Image.show(InvertedFish)
    Image.show(BlurredCat)
    Image.show(correlatedPig)
    Image.show(sharpenedPython)
    Image.show(edgedConstruct)

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()


