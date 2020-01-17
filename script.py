#libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt
import PIL.Image
import tkinter
from tkinter import ttk,StringVar,filedialog 
from tkinter import *


class GUI:
	def __init__(self, window):
		self.input_text = StringVar()
		self.input_text1 = StringVar()
		self.input_text2 = StringVar()
		self.input_text3 = StringVar()
		self.input_text4 = StringVar()
		self.input_text5 = StringVar()
		self.input_text6 = StringVar()
		self.input_text7 = StringVar()
		self.input_text8 = StringVar()
		self.input_text9 = StringVar()
		self.x1 = StringVar()
		self.x2 = StringVar()
		self.t1 = StringVar()
		self.t2 = StringVar()
		self.path = ''

		window.title('Thermography')
		
		window.geometry("400x400")

		ttk.Button(window, text='Upload thermogram', command = lambda: self.set_path_users_field()).grid(row=0, column=0, ipadx=5, ipady=15)
		ttk.Label(window, textvariable=self.input_text, width=50).grid(row=7, column=0, ipadx=1, ipady=1)

		ttk.Button(window, text='Detect face', command = lambda: self.detect_faces()).grid(row=15, column=0, ipadx=5, ipady=15)
		ttk.Label(window, text='', width=50).grid(row=22, column=0, ipadx=1, ipady=1)

		ttk.Button(window, text='Extract features', command = lambda: self.extract()).grid(row=29, column=0, ipadx=5, ipady=15)
		ttk.Label(window, textvariable=self.input_text2, width=50).grid(row=33, column=0, ipadx=1, ipady=1)

		ttk.Button(window, text='Show vector', command = lambda: self.vector()).grid(row=36, column=0, ipadx=5, ipady=15)
		ttk.Label(window, textvariable=self.input_text9, width=50).grid(row=40, column=0, ipadx=1, ipady=1)

		ttk.Label(text="x1- face width, \nx2- mouth width, \nt1- temperature from the middle of the nose, \nt2- temperature from the middle of the right eye").grid(row=43, column=0)

	def set_path_users_field(self):
		self.path = filedialog.askopenfilename()
		self.input_text.set(self.path)

	def get_user_path(self):
		return self.path

	def detect_faces(self):

		im = cv2.imread(self.path)
		im_copy = im.copy()
		#apply haar classifier
		haar_cascade_face = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
		faces_rects = haar_cascade_face.detectMultiScale(im_copy, scaleFactor = 1.1, minNeighbors = 2)
		#draw rect around the face 
		for (x,y,w,h) in faces_rects:
			x = int(x + w*0.1)
			w = int(w*0.8)
			cv2.rectangle(im_copy, (x,y), (x+w, y+h), (0, 255, 0), 2)
			frame = im_copy[y:y+h, x:x+w]
			x1 = np.size(frame, 1)
		cv2.imwrite('termo.png', frame)
		self.x1.set(x1)

	def extract(self):
		
		im = PIL.Image.open("termo.png")
		width, height = im.size

		w = int(width)
		h = int(height/5)
	
		#crop mouth
		im1 = im.crop(((0, 3*h, w, 5*h)))
		im1.save('mouth_termo.png', 'PNG')
		#crop nose
		im2 = im.crop(((0, 2*h, w, 4*h)))
		im2.save('nose_termo.png', 'PNG')
		#crop eyes
		im3 = im.crop(((0, 1*h, w/2, 3*h)))
		im3.save('eyes_termo.png', 'PNG')

	def detect_mouth(self):

		im = cv2.imread('mouth_termo.png')
		im_copy = im.copy()
		scaleFactor = 1.1
		minNeighbors = 2 #change this line
		haar_cascade_mouth = cv2.CascadeClassifier('haar/haarcascade_smile.xml')
		mouth_rects = haar_cascade_mouth.detectMultiScale(im_copy, scaleFactor, minNeighbors)
	
		for(x,y,w,h) in mouth_rects:
			cv2.rectangle(im_copy, (x,y), (x+w, y+h), (255, 0, 0), 3)
			frame = im_copy[y:y+h, x:x+w]
			x2 = np.size(frame, 1)
		self.x2.set(x2)

	def get_nose_temp(self):

		im = PIL.Image.open("nose_termo.png")
		im_copy = im.copy()
		rgb_im = im_copy.convert('RGB')
		width, height = rgb_im.size

		r, g, b = rgb_im.getpixel((width/2,height/2))
	
		temp = self.get_temp(r)
		self.t1.set(temp)

	def get_eye_temp(self):

		im = PIL.Image.open("eyes_termo.png")
		im_copy = im.copy()
		rgb_im = im_copy.convert('RGB')
		width, height = rgb_im.size

		r, g, b = rgb_im.getpixel((width/2,height/2))
		temp = self.get_temp(r)
		self.t2.set(temp)

	def get_temp(self,r):
		if(r>=0 and r<24): temp = 20000 
		elif(r>24 and r<49): temp = 20100
		elif(r>=49 and r<77): temp = 20200
		elif(r>=77 and r<101): temp = 20300
		elif(r>=101 and r<130): temp = 20400
		elif(r>=130 and r<154): temp = 20500
		elif(r>=154 and r<182): temp = 20600
		elif(r>=182 and r<206): temp = 20700
		elif(r>=206 and r<231): temp = 20800
		elif(r>=231 and r<255): temp = 20900
		elif(r>=255): temp = 21000
		return temp


	def vector(self):
	
		self.detect_mouth()
		self.get_nose_temp()
		self.get_eye_temp()
		self.input_text3.set('x1= ' + self.x1.get())
		self.input_text4.set(self.input_text3.get() + ', x2= ')
		self.input_text5.set(self.input_text4.get() + self.x2.get())
		self.input_text6.set(self.input_text5.get() + ', t1= ')
		self.input_text7.set(self.input_text6.get() + self.t1.get())
		self.input_text8.set(self.input_text7.get() + ' t2= ')
		self.input_text9.set(self.input_text8.get() + self.t2.get())


if __name__ == '__main__':
	window = tkinter.Tk()
	gui = GUI(window)
	window.mainloop()

