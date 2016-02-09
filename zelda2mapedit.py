#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A simple overworld-editor for Zelda 2 - The Adventure of Link

Author: Johan Björnell <johan@bjornell.se>

Version: 0.3.0

"""

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfile
import sys


class Zelda2MapEdit:

    def __init__(self, master):
        
        ###  User interface
        self.master = master
        self.master.title("Zelda2MapEdit")
        maxw = 1040
        maxh = 1260
        self.master.maxsize(width=maxw, height=maxh)

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        if sh > maxh:
            sh = maxh
        if sw > maxw:
            sw = maxw

        self.master.geometry('%dx%d+%d+%d' % (sw, sh-100, 0, 0))

        # Canvas to draw the map on
        self.canvas = Canvas(master)
        self.hsb = Scrollbar(master, orient="h", command=self.canvas.xview)
        self.vsb = Scrollbar(master, orient="v", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.hsb.grid(row=2, column=0, stick="ew")
        self.vsb.grid(row=1, column=1, sticky="ns")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.canvas.configure(scrollregion = (0, 0, 1024, 1200))

        # Call function leftclick when left click on canvas
        self.canvas.bind("<Button 1>", self.leftclick)
        # Call function rightpress on right mouse button press on canvas
        self.canvas.bind("<ButtonPress-3>", self.rightpress)
        # Call function rightmotion when right mouse is down and mouse is moved on canvas
        self.canvas.bind("<B3-Motion>", self.rightmotion)
        # Call function rightrelease on right mouse button release on canvas
        self.canvas.bind("<ButtonRelease-3>", self.rightrelease)
        # Call function mousemove on mouse movement over canvas
        self.canvas.bind("<Motion>", self.mousemove)

        # Terrain images 
        self.mountain_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQAEBAQEBAQEBAQEBAQEBAQEBAcBAAP/AQMBAAMBAAAEBAQEBAQEBAcBAAP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAcBAAAEBAQEBAQEBAcBAAP7+/gEBAcBAAAEBAQEBAQEBAQEBAQEBAf7+/sBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAP7+/gEBAQEBAcBAAAEBAQEBAf7+/sBAAMBAAAEBAQEBAcBAAMBAAAEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAcBAAMBAAP7+/sBAAAEBAcBAAMBAAAEBAQEBAcBAAMBAAP7+/gEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAP7+/gEBAcBAAMBAAMBAAMBAAAEBAQEBAQEBAcBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAP7+/gEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAAEBAQEBAcBAAMBAAMBAAP7+/sBAAMBAAAEBAQEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAP7+/gEBAQEBAQEBAcBAAMBAAP7+/sBAAAEBAQEBAcBAAMBAAAEBAQEBAcBAAMBAAMBAAP7+/gEBAcBAAMBAAAEBAcBAAAEBAQEBAQEBAcBAAAEBAQEBAcBAAMBAAP7+/sBAAP7+/v7+/gEBAcBAAAEBAcBAAAEBAQEBAQEBAQEBAQEBAcBAAMBAAAEBAcBAAP7+/sBAAP7+/gEBAQEBAcBAAMBAAAEBAQEBAcBAAAEBAQEBAcBAAMBAAAEBAcBAAMBAAMBAAMBAAP7+/gEBAcBAAMBAAAEBAcBAAMBAAAEBAcBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAP/AQAEBAcBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAf/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.town_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQICAgICAgICAgICAgICAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v/AQP/AQAEBAYCAgICAgICAgICAgP7+/v/AQP/AQP/AQP7+/v7+/gEBAQEBAf7+/v/AQAEBAYCAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP7+/v7+/gEBAQEBAf7+/gEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP/AQAEBAYCAgICAgP7+/gEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQAEBAYCAgICAgP7+/oCAgP7+/gEBAQEBAf7+/v7+/v7+/v7+/v7+/v/AQP/AQAEBAYCAgICAgP7+/v7+/v7+/oCAgP7+/gEBAQEBAQEBAQEBAf7+/v7+/v/AQAEBAYCAgICAgICAgP7+/v7+/v7+/oCAgICAgP7+/gEBAQEBAQEBAf7+/v7+/v/AQAEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/gEBAf7+/v7+/v7+/v7+/v/AQP/AQAEBAf7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAQEBAf7+/v7+/v7+/v7+/v/AQP/AQAEBAf7+/v7+/v7+/gEBAf7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/v7+/v7+/gEBAf7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.water_img = PhotoImage(data = "R0lGODlhEQAQAPEAAAEBAUDA/8DAwP7+/iH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABEAEAAAAi5cjmF5gsAORC7apuxK9caObIkBPhZQiSEjqIcbdBMzx57lwG5524zuo51SGlYBADs=")
        self.desert_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.road_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.forest_img = PhotoImage(data = "R0lGODlhEAAQAPcAAIDAAAEBAQCgAIDAAIDAAACgAIDAAAEBAQCgAIDAAIDAAIDAAAEBAQCgAIDAAIDAAAEBAQEBAQCgAACgAAEBAYDAAAEBAQEBAQCgAAEBAYDAAAEBAQCgAACgAACgAIDAAAEBAQCgAACgAAEBAQCgAAEBAQEBAQCgAACgAACgAIDAAAEBAQCgAACgAACgAIDAAAEBAQCgAAEBAQEBAQCgAACgAAEBAQCgAACgAACgAAEBAQEBAQEBAQCgAACgAACgAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAACgAACgAAEBAQCgAAEBAQCgAAEBAQCgAAEBAQEBAQCgAACgAACgAAEBAQEBAQEBAQCgAAEBAQCgAACgAAEBAQEBAYDAAAEBAQCgAAEBAQEBAQCgAACgAACgAAEBAQCgAACgAAEBAQCgAACgAACgAIDAAIDAAIDAAAEBAQEBAQCgAACgAACgAAEBAQEBAQCgAAEBAQEBAQEBAQCgAACgAACgAIDAAIDAAAEBAQEBAQCgAACgAACgAACgAACgAAEBAQEBAQEBAQCgAACgAACgAACgAIDAAAEBAQEBAQCgAAEBAQCgAACgAACgAACgAAEBAQEBAQCgAACgAACgAACgAACgAAEBAQEBAQEBAQEBAQCgAACgAACgAACgAAEBAQEBAQCgAAEBAQCgAACgAACgAACgAACgAAEBAQEBAQCgAAEBAQCgAACgAACgAIDAAAEBAQEBAQCgAACgAACgAACgAACgAAEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAQEBAYDAAAEBAQCgAAEBAQCgAACgAAEBAQCgAAEBAYDAAAEBAQEBAQEBAQEBAYDAAAEBAQEBAQEBAQEBAQCgAAEBAQEBAYDAAIDAAAEBAQCgAACgAAEBAQEBAYDAAAEBAQEBAQCgAAEBAYDAAAEBAQEBAYDAAIDAAIDAAIDAAAEBAQEBAQCgAIDAAIDAAAEBAQCgAACgAACgAIDAAAEBAQEBAYDAAACgAIDAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.water_walk_img = PhotoImage(data = "R0lGODlhEQAQAPEAAAEBAZnZ6sDAwP7+/iH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABEAEAAAAi5cjmF5gsAORC7apuxK9caObIkBPhZQiSEjqIcbdBMzx57lwG5524zuo51SGlYBADs=")
        self.lava_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.palace_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.cave_img = PhotoImage(data = "R0lGODlhEAAQAPAAAAEBAQAAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAAAg6Ej6nL7Q+jnLTai7M+BQA7")
        self.spider_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAf/AQAEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/v7+/gEBAf7+/v7+/gEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/gEBAQEBAQEBAf7+/gEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAQEBAQEBAQEBAQEBAf/AQAEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQAEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAf/AQAEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAf/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.graveyard_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v7+/v7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v7+/v7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAcBAAMBAAP/AQMBAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAcBAAP/AQMBAAP/AQP/AQMBAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.grass_img = PhotoImage(data = "R0lGODlhEAAQAPcAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.bridge_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBASH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.swamp_img = PhotoImage(data = "R0lGODlhEAAQAPcAAAEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAAEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAIDAAAEBAQCgAAEBAQCgAACgAACgAAEBAYDAAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAACgAACgAACgAAEBAYDAAAEBAYDAAAEBAQCgAACgAACgAAEBAYDAAAEBAYDAAAEBAQEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAAEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAIDAAAEBAQCgAAEBAQCgAACgAACgAAEBAYDAAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAACgAACgAACgAAEBAYDAAAEBAYDAAAEBAQCgAACgAACgAAEBAYDAAAEBAYDAAAEBASH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.rock_img = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/sBAAMBAAP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/sBAAMBAAP7+/v7+/sBAAP7+/v7+/sBAAAEBAf/AQP/AQP/AQP7+/v7+/sBAAMBAAP7+/v7+/sBAAMBAAMBAAMBAAMBAAP7+/sBAAAEBAf/AQP/AQP7+/sBAAP7+/v7+/sBAAP7+/v7+/v7+/sBAAMBAAMBAAMBAAMBAAAEBAf/AQP7+/v7+/sBAAP7+/sBAAMBAAMBAAMBAAP7+/v7+/sBAAMBAAMBAAAEBAQEBAQEBAf/AQP7+/v7+/sBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAAEBAQEBAf7+/v7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAAEBAQEBAQEBAf/AQP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAAEBAQEBAQEBAf/AQP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAAEBAQEBAf/AQMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAAEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAMBAAAEBAcBAAAEBAQEBAcBAAAEBAQEBAQEBAcBAAMBAAAEBAcBAAMBAAMBAAAEBAQEBAQEBAQEBAQEBAcBAAMBAAAEBAQEBAQEBAcBAAMBAAMBAAAEBAQEBAQEBAcBAAAEBAQEBAcBAAMBAAAEBAQEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAcBAAAEBAQEBAcBAAAEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAf/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.error_img = PhotoImage(data = "R0lGODlhEAAQAPAAAAEBAe0cJCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAAAiKMA6l5bcucW7LGWe3NiHK4NWB4jFynnA+ZAZq6siL0mUcBADs=")

        # Set window icon
        self.master.tk.call('wm', 'iconphoto', root._w, self.palace_img)

        # Frame with buttons
        self.btnFrame = Frame(root, height=60)
        self.btnFrame.grid(row=0, column=0)

        # Buttons
        self.townbtn = Button(self.btnFrame, image=self.town_img, command=lambda: self.selectterrain("Town"))
        self.townbtn.grid(row=0, column=0)
        self.cavebtn = Button(self.btnFrame, image=self.cave_img, command=lambda: self.selectterrain("Cave"))
        self.cavebtn.grid(row=0, column=1)
        self.palacebtn = Button(self.btnFrame, image=self.palace_img, command=lambda: self.selectterrain("Palace"))
        self.palacebtn.grid(row=0, column=2)
        self.bridgebtn = Button(self.btnFrame, image=self.bridge_img, command=lambda: self.selectterrain("Bridge"))
        self.bridgebtn.grid(row=0, column=3)
        self.desertbtn = Button(self.btnFrame, image=self.desert_img, command=lambda: self.selectterrain("Desert"))
        self.desertbtn.grid(row=0, column=4)
        self.grassbtn = Button(self.btnFrame, image=self.grass_img, command=lambda: self.selectterrain("Grass"))
        self.grassbtn.grid(row=0, column=5)
        self.forestbtn = Button(self.btnFrame, image=self.forest_img, command=lambda: self.selectterrain("Forest"))
        self.forestbtn.grid(row=0, column=6)
        self.swampbtn = Button(self.btnFrame, image=self.swamp_img, command=lambda: self.selectterrain("Swamp"))
        self.swampbtn.grid(row=0, column=7)
        self.graveyardbtn = Button(self.btnFrame, image=self.graveyard_img, command=lambda: self.selectterrain("Graveyard"))
        self.graveyardbtn.grid(row=0, column=8)
        self.roadbtn = Button(self.btnFrame, image=self.road_img, command=lambda: self.selectterrain("Road"))
        self.roadbtn.grid(row=0, column=9)
        self.lavabtn = Button(self.btnFrame, image=self.lava_img, command=lambda: self.selectterrain("Lava"))
        self.lavabtn.grid(row=0, column=10)
        self.mountainbtn = Button(self.btnFrame, image=self.mountain_img, command=lambda: self.selectterrain("Mountain"))
        self.mountainbtn.grid(row=0, column=11)
        self.waterbtn = Button(self.btnFrame, image=self.water_img, command=lambda: self.selectterrain("Water"))
        self.waterbtn.grid(row=0, column=12)
        self.water_walkbtn = Button(self.btnFrame, image=self.water_walk_img, command=lambda: self.selectterrain("Water_Walk"))
        self.water_walkbtn.grid(row=0, column=13)
        self.rockbtn = Button(self.btnFrame, image=self.rock_img, command=lambda: self.selectterrain("Rock"))
        self.rockbtn.grid(row=0, column=14)
        self.spiderbtn = Button(self.btnFrame, image=self.spider_img, command=lambda: self.selectterrain("Spider"))
        self.spiderbtn.grid(row=0, column=15)

        # Labels in btnFrame
        self.coordlabeltext = StringVar()
        self.coordlabeltext.set("'0' (0, 0)")
        self.coordlabel = Label(self.btnFrame, textvariable=self.coordlabeltext)
        self.coordlabel.grid(row=0, column=16)
        self.mapsizelabeltext = StringVar()
        self.mapsizelabeltext.set("000 / 000")
        self.mapsizelabel = Label(self.btnFrame, textvariable=self.mapsizelabeltext)
        self.mapsizelabel.grid(row=0, column=17)

        # Frame for label in the bottom
        self.labelFrame = Frame(root, height=60)
        self.labelFrame.grid(row=3, column=0)

        self.locationlabeltext = StringVar()
        self.locationlabeltext.set("")
        self.locationlabel = Label(self.labelFrame, textvariable=self.locationlabeltext)
        self.locationlabel.grid(row=0, column=0)
        

        # Menu
        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.openromfile)
        self.filemenu.add_command(label="Save", command=self.saveromfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.mapmenu = Menu(self.menubar, tearoff=0)
        self.mapmenu.add_command(label="West Hyrule", command=lambda: self.changemap("West Hyrule"))
        self.mapmenu.add_command(label="Death Mountain", command=lambda: self.changemap("Death Mountain"))
        self.mapmenu.add_command(label="East Hyrule", command=lambda: self.changemap("East Hyrule"))
        self.mapmenu.add_command(label="Maze Island", command=lambda: self.changemap("Maze Island"))
        self.menubar.add_cascade(label="Map", menu=self.mapmenu)

#        self.helpmenu = Menu(self.menubar, tearoff=0)
#        self.helpmenu.add_command(label="About...", command=self.about())
#        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

        
        ### Variables
        # Map size
        self.mapsizex = 64
        self.mapsizey = 75

        # Original mapsize
        self.origmapsize0 = 800 
        self.origmapsize1 = 802
        self.origmapsize2 = 793
        self.origmapsize3 = 802

        # Selected terrain to draw on map (0-f)
        self.selectedterrain = "c"

        # Arrays to contain decoded mapstrings
        self.maparray0 = [[0 for y in range(self.mapsizey)] for x in range(self.mapsizex)]
        self.maparray1 = [[0 for y in range(self.mapsizey)] for x in range(self.mapsizex)]
        self.maparray2 = [[0 for y in range(self.mapsizey)] for x in range(self.mapsizex)]
        self.maparray3 = [[0 for y in range(self.mapsizey)] for x in range(self.mapsizex)]
        # Array to work in
        self.currentmap = [[0 for y in range(self.mapsizey)] for x in range(self.mapsizex)]

        # Keep track of active map
        self.activemap = ""

        # Map data locations in ROM
        self.mapstart0 = int("506C", 16) # West Hyrule
        self.mapstart1 = int("665C", 16) # Death Mountain
        self.mapstart2 = int("9056", 16) # East Hyrule
        self.mapstart3 = int("A65C", 16) # Maze Island

        # Filename
        self.filename = ""

        # Enable edit after file open only
        self.editenabled = 0

        # Locations on map
        # Name, x address, y address, x offset, y offset, palace pointer address
        # West Hyrule
        self.map0locations = [[ "North Palace", "466E", "462F", 0, 0, 0, 0, 0 ],
                             [ "Trophy cave", "466F", "4630", 0, 0, 0, 0, 0 ],
                             [ "Forest with 50 exp. bag and Aches", "4670", "4631", 0, 0, 0, 0, 0 ],
                             [ "1st Magic Container cave", "4671", "4632", 0, 0, 0, 0, 0 ],
                             [ "Forest with 100 exp. bag and Megmets", "4672", "4633", 0, 0, 0, 0, 0 ],
                             [ "1st Heart Container area", "4673", "4634", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "4674", "4635", 0, 0, 0, 0, 0 ],
                             [ "Bubble path to 1st Heart Container", "4675", "4636", 0, 0, 0, 0, 0 ],
                             [ "Life doll in swamp", "4676", "4637", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar in graveyard", "4677", "4638", 0, 0, 0, 0, 0 ],
                             [ "Northern exit of cave to Palace 1", "4678", "4639", 0, 0, 0, 0, 0 ],
                             [ "Southern exit of cave to Palace 1", "4679", "463A", 0, 0, 64, 0, 0 ],
                             [ "Northern exit of Western Mt. caves", "467A", "463B", 0, 0, 0, 0, 0 ],
                             [ "Southern exit of Western Mt. caves", "467B", "463C", 0, 0, 64, 0, 0 ],
                             [ "Megmet cave and 200 exp. bag", "467C", "463D", 0, 0, 0, 0, 0 ],
                             [ "Water of Life cave", "467D", "463E", 0, 0, 0, 0, 0 ],
                             [ "2nd Heart Container cave", "467E", "463F", 0, 0, 0, 0, 0 ],
                             [ "Hole to Palace 3 cave", "467F", "4640", 0, 0, 0, 0, 0 ],
                             [ "Caves on Palace 3's island", "4680", "4641", 0, 0, 64, 0, 0 ],
                             [ "North and South bridge to island before Death Mt.", "4681", "4642", 0, 0, 0, 0, 0 ],
                             [ "East and West bridge to island before Death Mt.", "4682", "4643", 0, 0, 0, 0, 0 ],
                             [ "West exit of bridge after Death Mt.", "4683", "4644", 0, 0, 0, 0, 0 ],
                             [ "East exit of bridge after Death Mt.", "4684", "4645", 0, 0, 64, 0, 0 ],
                             [ "Forest with Fairy after Western Mt. cave", "4685", "4646", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar in swamp", "4686", "4647", 0, 0, 0, 0, 0 ],
                             [ "forest with Fairy East of island before Death Mt.", "4687", "4648", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "4688", "4649", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "4689", "464A", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "468A", "464B", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "468B", "464C", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar on trail in swamp", "468C", "464D", 0, 0, 0, 0, 0 ],
                             [ "Extra Red Magic Jar on beach (not used in original game)", "468D", "464E", 0, 0, 0, 0, 0 ],
                             [ "Life doll on beach", "468E", "464F", 0, 0, 0, 0, 0 ],
                             [ "Raft Dock to East Hyrule", "4697", "4658", 0, 0, 0, 128, 0 ],
                             [ "Cave entrance to Death Mountain", "4698", "4659", 0, 0, 0, 128, 0 ],
                             [ "Cave exit to Death Mountain", "4699", "465A", 0, 0, 0, 128, 0 ],
                             [ "King's Tomb", "469A", "465B", 0, 0, 0, 128, 0 ],
                             [ "Rauru", "469B", "465C", 0, 0, 64, 128, 0 ],
                             [ "Ruto", "469D", "465E", 0, 0, 64, 128, 0 ],
                             [ "Southern Saria", "469E", "465F", 0, 0, 0, 128, 0 ],
                             [ "Northern Saria", "469F", "4660", 0, 0, 64, 128, 0 ],
                             [ "Bagu's Cabin", "46A0", "4661", 0, 0, 0, 128, 0 ],
                             [ "Mido", "46A1", "4662", 0, 0, 64, 128, 0 ],
                             [ "Parapa Palace", "46A2", "4663", 0, 0, 0, 128, "479F" ],
                             [ "Swamp Palace", "46A3", "4664", 0, 0, 0, 128, "47A1" ],
                             [ "Island Palace", "46A4", "4665", 0, 0, 0, 128, "47A3" ]]


        self.map1locations = [[ "Cave B West Exit", "614B", "610C", 0, 0, 0, 0, 0 ],
                             [ "Cave B East Exit", "614C", "610D", 0, 0, 64, 0, 0 ],
                             [ "Cave C West Exit", "614D", "610E", 0, 0, 0, 0, 0 ],
                             [ "Cave C East Exit", "614E", "610F", 0, 0, 64, 0, 0 ],
                             [ "Cave E South Exit", "614F", "6110", 0, 0, 0, 0, 0 ],
                             [ "Cave E North Exit", "6150", "6111", 0, 0, 64, 0, 0 ],
                             [ "Cave D West Exit", "6151", "6112", 0, 0, 0, 0, 0 ],
                             [ "Cave D East Exit", "6152", "6113", 0, 0, 64, 0, 0 ],
                             [ "Cave F West Exit", "6153", "6114", 0, 0, 0, 0, 0 ],
                             [ "Cave F East Exit", "6154", "6115", 0, 0, 64, 0, 0 ],
                             [ "Cave J West Exit", "6155", "6116", 0, 0, 0, 0, 0 ],
                             [ "Cave J East Exit", "6156", "6117", 0, 0, 64, 0, 0 ],
                             [ "Cave I North Exit", "6157", "6118", 0, 0, 0, 0, 0 ],
                             [ "Cave I South Exit", "6158", "6119", 0, 0, 64, 0, 0 ],
                             [ "Cave L North Exit", "6159", "611A", 0, 0, 0, 0, 0 ],
                             [ "Cave L South Exit", "615A", "611B", 0, 0, 64, 0, 0 ],
                             [ "Cave O North Exit", "615B", "611C", 0, 0, 0, 0, 0 ],
                             [ "Cave O South Exit", "615C", "611D", 0, 0, 64, 0, 0 ],
                             [ "Cave M West Exit", "615D", "611E", 0, 0, 0, 0, 0 ],
                             [ "Cave M East Exit", "615E", "611F", 0, 0, 64, 0, 0 ],
                             [ "Cave P West Exit", "615F", "6120", 0, 0, 0, 0, 0 ],
                             [ "Cave P East Exit", "6160", "6121", 0, 0, 64, 0, 0 ],
                             [ "Cave Q West Exit", "6161", "6122", 0, 0, 0, 0, 0 ],
                             [ "Cave Q East Exit", "6162", "6123", 0, 0, 64, 0, 0 ],
                             [ "Cave R South Exit", "6163", "6124", 0, 0, 0, 0, 0 ],
                             [ "Cave R North Exit", "6164", "6125", 0, 0, 64, 0, 0 ],
                             [ "Cave N South Exit", "6165", "6126", 0, 0, 0, 0, 0 ],
                             [ "Cave N North Exit", "6166", "6127", 0, 0, 64, 0, 0 ],
                             [ "Hammer Cave", "6167", "6128", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave G West Exit (Bottom left)", "6168", "6129", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave G East Exit (Bottom right)", "6169", "612A", 0, 0, 64, 0, 0 ],
                             [ "Elevator Cave G West Exit (Top left)", "616A", "612B", 0, 0, 128, 0, 0 ],
                             [ "Elevator Cave G East Exit (Top Right)", "616B", "612C", 0, 0, 192, 0, 0 ],
                             [ "Elevator Cave H West Exit (Top left)", "616C", "612D", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave H East Exit (Top Right)", "616D", "612E", 0, 0, 64, 0, 0 ],
                             [ "Elevator Cave H North Exit (Bottom left)", "616E", "612F", 0, 0, 128, 0, 0 ],
                             [ "Elevator Cave H South Exit (Bottom right)", "616F", "6130", 0, 0, 192, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 2", "6170", "6131", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 1", "6171", "6132", 0, 0, 0, 0, 0 ],
                             [ "Maze Island's Magic Container", "6172", "6133", 0, 0, 0, 0, 0 ],
                             [ "Bridge back to East Hyrule", "6173", "6134", 0, 0, 0, 128, 0 ],
                             [ "Cave A back to West Hyrule", "6175", "6136", 0, 0, 0, 128, 0 ],
                             [ "Cave K back to West Hyrule", "6176", "6137", 0, 0, 0, 128, 0 ],
                             [ "Maze Palace in Death Mountain", "617F", "6140", 0, 0, 0, 128, "47A5" ],
                             [ "Maze Island Child", "6182", "6143", 0, 0, 0, 0, 0 ],
                             [ "Death Mountain's Magic Container", "6183", "6144", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 3", "6184", "6145", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 7", "6185", "6146", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 4", "6186", "6147", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 5", "6187", "6148", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 6", "6188", "6149", 0, 0, 0, 0, 0 ]]


        self.map2locations = [[ "Forest with 500 Exp. bag west of Nabooru", "866E", "862F", 0, 0, 0, 0, 0 ],
                             [ "Forest with 500 Exp. bag north of 3-Eye Rock", "866F", "8630", 0, 0, 0, 0, 0 ],
                             [ "1st Forced battle scene after River Devil", "8670", "8631", 0, 0, 0, 0, 0 ],
                             [ "2nd Forced battle scene after River Devil", "8671", "8632", 0, 0, 0, 0, 0 ],
                             [ "3rd Forced battle scene after River Devil", "8672", "8633", 0, 0, 0, 0, 0 ],
                             [ "Forced battle scene entering Path of Fire", "8673", "8634", 0, 0, 0, 0, 0 ],
                             [ "Bridge North of Old Kasuto", "8674", "8635", 0, 0, 0, 0, 0 ],
                             [ "Bridge East of Old Kasuto", "8675", "8636", 0, 0, 0, 0, 0 ],
                             [ "2nd battle scene before Darunia", "8676", "8637", 0, 0, 0, 0, 0 ],
                             [ "1st battle scene before Darunia", "8677", "8638", 0, 0, 0, 0, 0 ],
                             [ "Heart Container in Ocean", "8678", "8639", 0, 0, 0, 0, 0 ],
                             [ "South cave north of Nabooru", "8679", "863A", 0, 0, 0, 0, 0 ],
                             [ "North cave north of Nabooru", "867A", "863B", 0, 0, 64, 0, 0 ],
                             [ "Cave with 500 exp. bag south of Nabooru", "867B", "863C", 0, 0, 0, 0, 0 ],
                             [ "Cave with 500 exp. bag North of Old Kasuto", "867C", "863D", 0, 0, 0, 0, 0 ],
                             [ "West cave near New Kasuto", "867D", "863E", 0, 0, 0, 0, 0 ],
                             [ "East cave near New Kasuto", "867E", "863F", 0, 0, 64, 0, 0 ],
                             [ "Cave C on the way to Great Palace", "867F", "8640", 0, 0, 0, 0, 0 ],
                             [ "Cave D on the way to Great Palace", "8680", "8641", 0, 0, 64, 0, 0 ],
                             [ "Cave B on the way to Great Palace", "8681", "8642", 0, 0, 0, 0, 0 ],
                             [ "Cave A on the way to Great Palace", "8682", "8643", 0, 0, 64, 0, 0 ],
                             [ "Life doll in swamp", "8683", "8644", 0, 0, 0, 0, 0 ],
                             [ "Extra battle scene (same spot as 864B)", "8684", "8645", 0, 0, 0, 0, 0 ],
                             [ "500 exp. bag on beach near 5th Palace", "8685", "8646", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar on beach near Nabooru", "8686", "8647", 0, 0, 0, 0, 0 ],
                             [ "Life doll on beach", "8687", "8648", 0, 0, 0, 0, 0 ],
                             [ "Heart Container on beach east of 3-Eye Rock", "8688", "8649", 0, 0, 0, 0, 0 ],
                             [ "Forest with fairy southwest of Nabooru", "8689", "864A", 0, 0, 0, 0, 0 ],
                             [ "500 exp. bag in Path of Fire", "868A", "864B", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar in Path of Fire", "868B", "864C", 0, 0, 0, 0, 0 ],
                             [ "3rd Forced Battle scene in the Path of Fire", "868C", "864D", 0, 0, 0, 0, 0 ],
                             [ "2nd Forced Battle scene in the Path of Fire", "868D", "864E", 0, 0, 0, 0, 0 ],
                             [ "1st Forced Battle scene in the Path of Fire", "868E", "864F", 0, 0, 0, 0, 0 ],
                             [ "Bridge to Maze Island", "8696", "8657", 0, 0, 0, 128, 0 ],
                             [ "Raft dock back to West Hyrule", "8697", "8658", 0, 0, 0, 128, 0 ],
                             [ "Nabooru", "869B", "865C", 0, 0, 64, 128, 0 ],
                             [ "Darunia", "869D", "865E", 0, 0, 64, 128, 0 ],
                             # Not implemented (hidden) [ "New Kasuto *", "869F", "8660", 0, 0, 0, 0, 0 ],
                             [ "Old Kasuto", "86A1", "8662", 0, 0, 64, 128, 0 ],
                             [ "5th Palace", "86A2", "8663", 0, 0, 0, 128, "879F" ],
                             # Not implemented (hidden) [ "6th Palace", "86A3", "8664", 0, 0, 0, 0, "87A1"],
                             [ "Great Palace", "86A4", "8665", 0, 0, 0, 128, 0 ]]


        self.map3locations = [[ "Cave B West Exit", "A14B", "A10C", 0, 0, 0, 0, 0 ],
                             [ "Cave B East Exit", "A14C", "A10D", 0, 0, 64, 0, 0 ],
                             [ "Cave C West Exit", "A14D", "A10E", 0, 0, 0, 0, 0 ],
                             [ "Cave C East Exit", "A14E", "A10F", 0, 0, 64, 0, 0 ],
                             [ "Cave E South Exit", "A14F", "A110", 0, 0, 0, 0, 0 ],
                             [ "Cave E North Exit", "A150", "A111", 0, 0, 64, 0, 0 ],
                             [ "Cave D West Exit", "A151", "A112", 0, 0, 0, 0, 0 ],
                             [ "Cave D East Exit", "A152", "A113", 0, 0, 64, 0, 0 ],
                             [ "Cave F West Exit", "A153", "A114", 0, 0, 0, 0, 0 ],
                             [ "Cave F East Exit", "A154", "A115", 0, 0, 64, 0, 0 ],
                             [ "Cave J West Exit", "A155", "A116", 0, 0, 0, 0, 0 ],
                             [ "Cave J East Exit", "A156", "A117", 0, 0, 64, 0, 0 ],
                             [ "Cave I North Exit", "A157", "A118", 0, 0, 0, 0, 0 ],
                             [ "Cave I South Exit", "A158", "A119", 0, 0, 64, 0, 0 ],
                             [ "Cave L North Exit", "A159", "A11A", 0, 0, 0, 0, 0 ],
                             [ "Cave L South Exit", "A15A", "A11B", 0, 0, 64, 0, 0 ],
                             [ "Cave O North Exit", "A15B", "A11C", 0, 0, 0, 0, 0 ],
                             [ "Cave O South Exit", "A15C", "A11D", 0, 0, 64, 0, 0 ],
                             [ "Cave M West Exit", "A15D", "A11E", 0, 0, 0, 0, 0 ],
                             [ "Cave M East Exit", "A15E", "A11F", 0, 0, 64, 0, 0 ],
                             [ "Cave P West Exit", "A15F", "A120", 0, 0, 0, 0, 0 ],
                             [ "Cave P East Exit", "A160", "A121", 0, 0, 64, 0, 0 ],
                             [ "Cave Q West Exit", "A161", "A122", 0, 0, 0, 0, 0 ],
                             [ "Cave Q East Exit", "A162", "A123", 0, 0, 64, 0, 0 ],
                             [ "Cave R South Exit", "A163", "A124", 0, 0, 0, 0, 0 ],
                             [ "Cave R North Exit", "A164", "A125", 0, 0, 64, 0, 0 ],
                             [ "Cave N South Exit", "A165", "A126", 0, 0, 0, 0, 0 ],
                             [ "Cave N North Exit", "A166", "A127", 0, 0, 64, 0, 0 ],
                             [ "Hammer Cave", "A167", "A128", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave G West Exit (Bottom left)", "A168", "A129", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave G East Exit (Bottom right)", "A169", "A12A", 0, 0, 64, 0, 0 ],
                             [ "Elevator Cave G West Exit (Top left)", "A16A", "A12B", 0, 0, 128, 0, 0 ],
                             [ "Elevator Cave G East Exit (Top Right)", "A16B", "A12C", 0, 0, 192, 0, 0 ],
                             [ "Elevator Cave H West Exit (Top left)", "A16C", "A12D", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave H East Exit (Top Right)", "A16D", "A12E", 0, 0, 64, 0, 0 ],
                             [ "Elevator Cave H North Exit (Bottom left)", "A16E", "A12F", 0, 0, 128, 0, 0 ],
                             [ "Elevator Cave H South Exit (Bottom right)", "A16F", "A130", 0, 0, 192, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 2", "A170", "A131", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 1", "A171", "A132", 0, 0, 0, 0, 0 ],
                             [ "Maze Island's Magic Container", "A172", "A133", 0, 0, 0, 0, 0 ],
                             [ "Bridge back to East Hyrule", "A173", "A134", 0, 0, 0, 128, 0 ],
                             [ "Cave A back to West Hyrule", "A175", "A136", 0, 0, 0, 128, 0 ],
                             [ "Cave K back to West Hyrule", "A176", "A137", 0, 0, 0, 128, 0 ],
                             [ "Maze Palace in Maze Island", "A17F", "A140", 0, 0, 0, 128, "87A7" ],
                             [ "Maze Island Child", "A182", "A143", 0, 0, 0, 0, 0 ],
                             [ "Death Mountain's Magic Container", "A183", "A144", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 3", "A184", "A145", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 7", "A185", "A146", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 4", "A186", "A147", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 5", "A187", "A148", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 6", "A188", "A149", 0, 0, 0, 0, 0 ]]

        # Keep track of location to move
        self.movelocation = "-1"
        self.movelocationprevx = "-1"
        self.movelocationprevy = "-1"
                            
    # End __init__

    def selectterrain(self, terrain):
        # Raise buttons
        self.townbtn.config(relief=RAISED)
        self.cavebtn.config(relief=RAISED)
        self.palacebtn.config(relief=RAISED)
        self.bridgebtn.config(relief=RAISED)
        self.desertbtn.config(relief=RAISED)
        self.grassbtn.config(relief=RAISED)
        self.forestbtn.config(relief=RAISED)
        self.swampbtn.config(relief=RAISED)
        self.graveyardbtn.config(relief=RAISED)
        self.roadbtn.config(relief=RAISED)
        self.lavabtn.config(relief=RAISED)
        self.mountainbtn.config(relief=RAISED)
        self.waterbtn.config(relief=RAISED)
        self.water_walkbtn.config(relief=RAISED)
        self.rockbtn.config(relief=RAISED)
        self.spiderbtn.config(relief=RAISED)

        # Set terrain and sink the button
        if terrain == "Town":
            self.selectedterrain = "0"
            self.townbtn.config(relief=SUNKEN)
        elif terrain == "Cave":
            self.selectedterrain = "1"
            self.cavebtn.config(relief=SUNKEN)
        elif terrain == "Palace":
            self.selectedterrain = "2"
            self.palacebtn.config(relief=SUNKEN)
        elif terrain == "Bridge":
            self.selectedterrain = "3"
            self.bridgebtn.config(relief=SUNKEN)
        elif terrain == "Desert":
            self.selectedterrain = "4"
            self.desertbtn.config(relief=SUNKEN)
        elif terrain == "Grass":
            self.selectedterrain = "5"
            self.grassbtn.config(relief=SUNKEN)
        elif terrain == "Forest":
            self.selectedterrain = "6"
            self.forestbtn.config(relief=SUNKEN)
        elif terrain == "Swamp":
            self.selectedterrain = "7"
            self.swampbtn.config(relief=SUNKEN)
        elif terrain == "Graveyard":
            self.selectedterrain = "8"
            self.graveyardbtn.config(relief=SUNKEN)
        elif terrain == "Road":
            self.selectedterrain = "9"
            self.roadbtn.config(relief=SUNKEN)
        elif terrain == "Lava":
            self.selectedterrain = "a"
            self.lavabtn.config(relief=SUNKEN)
        elif terrain == "Mountain":
            self.selectedterrain = "b"
            self.mountainbtn.config(relief=SUNKEN)
        elif terrain == "Water":
            self.selectedterrain = "c"
            self.waterbtn.config(relief=SUNKEN)
        elif terrain == "Water_Walk":
            self.selectedterrain = "d"
            self.water_walkbtn.config(relief=SUNKEN)
        elif terrain == "Rock":
            self.selectedterrain = "e"
            self.rockbtn.config(relief=SUNKEN)
        elif terrain == "Spider":
            self.selectedterrain = "f"
            self.spiderbtn.config(relief=SUNKEN)

    def openromfile(self):
        options = {}
        options['defaultextension'] = '.nes'
        options['filetypes'] = [('Rom files', '.nes'), ('all files', '.*')]
        options['title'] = 'Open romfile'

        self.filename = askopenfilename(**options)
        if self.filename:
            try:
                print self.filename
            except:
                showerror(title=Error, message="Unable to open file")
        # Open rom file
        try:
            handle = open(self.filename,"r+b")
        except IOError:
            print ("Cannot open file %s" % self.filename)

        # Map 0 
        handle.seek(self.mapstart0)
        # read a byte at a time, decode to mapstring, until size == mapsizex*mapsizey
        mapstring = ""
        #self.origmapsize0 = 0 
        while len(mapstring) < self.mapsizex*self.mapsizey:
            #self.origmapsize0 += 1
            rawmapdata = handle.read(1)
            # Convert rawmapdata to string 
            strmapdata = rawmapdata.encode("hex")
            # Calculate map data
            terraintype = strmapdata[1]
            terraincount = int(strmapdata[0], 16)+1

            # Add to output_string
            for x in range(terraincount):
                mapstring += terraintype
    
        # Populate maparray0 with the decoded string
        x = 0
        y = 0
        for c in mapstring:
            self.maparray0[x][y] = c
            x += 1
            if x == self.mapsizex:
                y += 1
                x = 0
            if y == self.mapsizey:
                break
        
        # Read locations
        for i, _ in enumerate(self.map0locations):
             handle.seek(int(self.map0locations[i][1], 16))
             self.map0locations[i][3] = int(handle.read(1).encode("hex"), 16)
             handle.seek(int(self.map0locations[i][2], 16))
             self.map0locations[i][4] = int(handle.read(1).encode("hex"), 16)

        # Map 1 
        handle.seek(self.mapstart1)
        mapstring = ""
        #self.origmapsize1 = 0 
        while len(mapstring) < self.mapsizex*self.mapsizey:
            #self.origmapsize1 += 1
            rawmapdata = handle.read(1)
            strmapdata = rawmapdata.encode("hex")
            terraintype = strmapdata[1]
            terraincount = int(strmapdata[0], 16)+1

            for x in range(terraincount):
                mapstring += terraintype
    
        x = 0
        y = 0
        for c in mapstring:
            self.maparray1[x][y] = c
            x += 1
            if x == self.mapsizex:
                y += 1
                x = 0
            if y == self.mapsizey:
                break

        # Read locations
        for i, _ in enumerate(self.map1locations):
             handle.seek(int(self.map1locations[i][1], 16))
             self.map1locations[i][3] = int(handle.read(1).encode("hex"), 16)
             handle.seek(int(self.map1locations[i][2], 16))
             self.map1locations[i][4] = int(handle.read(1).encode("hex"), 16)

        # Map 2
        handle.seek(self.mapstart2)
        mapstring = ""
        #self.origmapsize2 = 0 
        while len(mapstring) < self.mapsizex*self.mapsizey:
            #self.origmapsize2 += 1
            rawmapdata = handle.read(1)
            strmapdata = rawmapdata.encode("hex")
            terraintype = strmapdata[1]
            terraincount = int(strmapdata[0], 16)+1

            for x in range(terraincount):
                mapstring += terraintype
    
        x = 0
        y = 0
        for c in mapstring:
            self.maparray2[x][y] = c
            x += 1
            if x == self.mapsizex:
                y += 1
                x = 0
            if y == self.mapsizey:
                break

        # Read locations
        for i, _ in enumerate(self.map2locations):
             handle.seek(int(self.map2locations[i][1], 16))
             self.map2locations[i][3] = int(handle.read(1).encode("hex"), 16)
             handle.seek(int(self.map2locations[i][2], 16))
             self.map2locations[i][4] = int(handle.read(1).encode("hex"), 16)

        # Map 3
        handle.seek(self.mapstart3)
        mapstring = ""
        #self.origmapsize3 = 0 
        while len(mapstring) < self.mapsizex*self.mapsizey:
            #self.origmapsize3 += 1
            rawmapdata = handle.read(1)
            strmapdata = rawmapdata.encode("hex")
            terraintype = strmapdata[1]
            terraincount = int(strmapdata[0], 16)+1

            for x in range(terraincount):
                mapstring += terraintype
    
        x = 0
        y = 0
        for c in mapstring:
            self.maparray3[x][y] = c
            x += 1
            if x == self.mapsizex:
                y += 1
                x = 0
            if y == self.mapsizey:
                break

        # Read locations
        for i, _ in enumerate(self.map3locations):
             handle.seek(int(self.map3locations[i][1], 16))
             self.map3locations[i][3] = int(handle.read(1).encode("hex"), 16)
             handle.seek(int(self.map3locations[i][2], 16))
             self.map3locations[i][4] = int(handle.read(1).encode("hex"), 16)

        # Close file
        handle.close()

        # Default to West Hyrule
        self.changemap("West Hyrule")

        # Enable editing
        self.editenabled = 1

    def saveromfile(self):
        # Save self.currentmap to correct self.maparray[0-3]
        if self.activemap == "West Hyrule":
            self.maparray0 = self.currentmap[:]
        elif self.activemap == "Death Mountain":
            self.maparray1 = self.currentmap[:]
        elif self.activemap == "East Hyrule":
            self.maparray2 = self.currentmap[:]
        elif self.activemap == "Maze Island":
            self.maparray3 = self.currentmap[:]

        # open file handle in write binary mode
        try:
            handle = open(self.filename, "r+b")
        except IOError:
            print "Cannot open file for saving"

        # Convert every maparray to encoded string and save to correct location in romfile
        # Map 0
        mapstring = ""
        for y in range(self.mapsizey):
            for x in range(self.mapsizex):
                mapstring += str(self.maparray0[x][y])

        encodedstring = self.mapencode(mapstring)
        handle.seek(self.mapstart0)

        # Read two characters, convert to a byte, write to file
        i = 0
        while i+1 < len(encodedstring):
            byte = encodedstring[i]+encodedstring[i+1]
            byte = byte.decode("hex")
            handle.write(byte)
            i += 2

        # Save locations map 0
        for i, _ in enumerate(self.map0locations):
            # Convert integer value to hex-string without 0x, and pad with 0 if needed
            x = hex(self.map0locations[i][3])[2:].zfill(2)
            y = hex(self.map0locations[i][4])[2:].zfill(2)
            # Convert string to binary value
            x = x.decode("hex")
            y = y.decode("hex")
            # Find address in romfile and write value
            handle.seek(int(self.map0locations[i][1], 16))
            handle.write(x) 
            handle.seek(int(self.map0locations[i][2], 16))
            handle.write(y)
            
            # Save offset for palace locations
            if self.map0locations[i][7] != 0:
                offset_in_array = (self.map0locations[i][4]-self.map0locations[i][6]-30)*64+self.map0locations[i][3]
                
                offsetsum = 0
                j = 0
                bytecounter = 0
                while j+1 < len(encodedstring):
                    offsetsum += int(encodedstring[j], 16)+1
                    j += 2
                    bytecounter += 1
                    if offsetsum == offset_in_array:
                        # Offset base is 0x7C00 (31744)
                        # Add offset to base, write as table at address
                        offsetstring = hex(j/2+31744)[2:].zfill(2)
                        byte1 = offsetstring[2:]
                        byte2 = offsetstring[:2]
                        byte1 = byte1.decode("hex")
                        byte2 = byte2.decode("hex")
                        handle.seek(int(self.map0locations[i][7], 16))
                        handle.write(byte1)
                        handle.write(byte2)
                        break

        # Map 1
        mapstring = ""
        for y in range(self.mapsizey):
            for x in range(self.mapsizex):
                mapstring += str(self.maparray1[x][y])

        encodedstring = self.mapencode(mapstring)
        handle.seek(self.mapstart1)

        i = 0
        while i+1 < len(encodedstring):
            byte = encodedstring[i]+encodedstring[i+1]
            byte = byte.decode("hex")
            handle.write(byte)
            i += 2

        # Save locations map 1
        for i, _ in enumerate(self.map1locations):
            x = hex(self.map1locations[i][3])[2:].zfill(2)
            y = hex(self.map1locations[i][4])[2:].zfill(2)
            xa = x.decode("hex")
            ya = y.decode("hex")
            handle.seek(int(self.map1locations[i][1], 16))
            handle.write(xa) 
            handle.seek(int(self.map1locations[i][2], 16))
            handle.write(ya)

            # Save offset for palace locations
            if self.map1locations[i][7] != 0:
                offset_in_array = (self.map1locations[i][4]-self.map1locations[i][6]-30)*64+self.map1locations[i][3]
                
                offsetsum = 0
                j = 0
                bytecounter = 0
                while j+1 < len(encodedstring):
                    offsetsum += int(encodedstring[j], 16)+1
                    j += 2
                    bytecounter += 1
                    if offsetsum == offset_in_array:
                        # Offset base is 0x7C00 (31744)
                        # Add offset to base, write as table at address
                        offsetstring = hex(j/2+31744)[2:].zfill(2)
                        byte1 = offsetstring[2:]
                        byte2 = offsetstring[:2]
                        byte1 = byte1.decode("hex")
                        byte2 = byte2.decode("hex")
                        handle.seek(int(self.map1locations[i][7], 16))
                        handle.write(byte1)
                        handle.write(byte2)
                        break

        # Map 2
        mapstring = ""
        for y in range(self.mapsizey):
            for x in range(self.mapsizex):
                mapstring += str(self.maparray2[x][y])

        encodedstring = self.mapencode(mapstring)
        handle.seek(self.mapstart2)

        i = 0
        while i+1 < len(encodedstring):
            byte = encodedstring[i]+encodedstring[i+1]
            byte = byte.decode("hex")
            handle.write(byte)
            i += 2

        # Save locations map 2
        for i, _ in enumerate(self.map2locations):
            x = hex(self.map2locations[i][3])[2:].zfill(2)
            y = hex(self.map2locations[i][4])[2:].zfill(2)
            xa = x.decode("hex")
            ya = y.decode("hex")
            handle.seek(int(self.map2locations[i][1], 16))
            handle.write(xa) 
            handle.seek(int(self.map2locations[i][2], 16))
            handle.write(ya)

            # Save offset for palace locations
            if self.map2locations[i][7] != 0:
                offset_in_array = (self.map2locations[i][4]-self.map2locations[i][6]-30)*64+self.map2locations[i][3]
                
                offsetsum = 0
                j = 0
                bytecounter = 0
                while j+1 < len(encodedstring):
                    offsetsum += int(encodedstring[j], 16)+1
                    j += 2
                    bytecounter += 1
                    if offsetsum == offset_in_array:
                        # Offset base is 0x7C00 (31744)
                        # Add offset to base, write as table at address
                        offsetstring = hex(j/2+31744)[2:].zfill(2)
                        byte1 = offsetstring[2:]
                        byte2 = offsetstring[:2]
                        byte1 = byte1.decode("hex")
                        byte2 = byte2.decode("hex")
                        handle.seek(int(self.map2locations[i][7], 16))
                        handle.write(byte1)
                        handle.write(byte2)
                        break


        # Map 3
        mapstring = ""
        for y in range(self.mapsizey):
            for x in range(self.mapsizex):
                mapstring += str(self.maparray3[x][y])

        encodedstring = self.mapencode(mapstring)
        handle.seek(self.mapstart3)

        i = 0
        while i+1 < len(encodedstring):
            byte = encodedstring[i]+encodedstring[i+1]
            byte = byte.decode("hex")
            handle.write(byte)
            i += 2

        
        # Save locations map 3
        for i, _ in enumerate(self.map3locations):
            x = hex(self.map3locations[i][3])[2:].zfill(2)
            y = hex(self.map3locations[i][4])[2:].zfill(2)
            xa = x.decode("hex")
            ya = y.decode("hex")
            handle.seek(int(self.map3locations[i][1], 16))
            handle.write(xa) 
            handle.seek(int(self.map3locations[i][2], 16))
            handle.write(ya)


            # Save offset for palace locations
            if self.map3locations[i][7] != 0:
                offset_in_array = (self.map3locations[i][4]-self.map3locations[i][6]-30)*64+self.map3locations[i][3]
                
                offsetsum = 0
                j = 0
                bytecounter = 0
                while j+1 < len(encodedstring):
                    offsetsum += int(encodedstring[j], 16)+1
                    j += 2
                    bytecounter += 1
                    if offsetsum == offset_in_array:
                        # Offset base is 0x7C00 (31744)
                        # Add offset to base, write as table at address
                        offsetstring = hex(j/2+31744)[2:].zfill(2)
                        byte1 = offsetstring[2:]
                        byte2 = offsetstring[:2]
                        byte1 = byte1.decode("hex")
                        byte2 = byte2.decode("hex")
                        handle.seek(int(self.map3locations[i][7], 16))
                        handle.write(byte1)
                        handle.write(byte2)
                        break


        handle.close()


    def changemap(self, overworldmap):
        # Put currentmap back to original self.maparray
        if self.activemap == "West Hyrule":
            self.maparray0 = self.currentmap[:]
        elif self.activemap == "Death Mountain":
            self.maparray1 = self.currentmap[:]
        elif self.activemap == "East Hyrule":
            self.maparray2 = self.currentmap[:]
        elif self.activemap == "Maze Island":
            self.maparray3 = self.currentmap[:]
        self.activemap = overworldmap

        # Put data for overworldmap in currentmap
        if overworldmap == "West Hyrule":
            self.currentmap = self.maparray0[:]
        elif overworldmap == "Death Mountain":
            self.currentmap = self.maparray1[:]
        elif overworldmap == "East Hyrule":
            self.currentmap = self.maparray2[:]
        elif overworldmap == "Maze Island":
            self.currentmap = self.maparray3[:]

        self.drawmap()


    def mapencode(self, input_string):
        tilecount = 1
        charcount = 0 # Encoding must stop at 64 tiles per line of map
        prev = ''
        output_string = ""
        for character in input_string:
            if character != prev:
                if prev:
                    output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
                prev = character
                if (charcount > 63):
                    charcount = 0
            elif (tilecount == 16):
                output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
            elif (charcount > 63):
                output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
                charcount = 0
            else:
                tilecount += 1
            charcount += 1
    
        output_string += str(hex(tilecount-1)[2:])+character


        return output_string


    def mapdecode(self, input_string):
        output_string = ""
        # Read byte from mapdata
        for c in input_string:
            # Convert byte to string 
            byte = c.encode("hex")
            # Calculate map data
            terraintype = byte[1]
            terraincount = int(byte[0], 16)+1
            debugcounter += terraincount

            # Add to output_string
            for x in range(terraincount):
                output_string += terraintype

        return output_string

    def drawlocations(self):
        if self.activemap == "West Hyrule":
            locations = self.map0locations
        elif self.activemap == "Death Mountain":
            locations = self.map1locations
        elif self.activemap == "East Hyrule":
            locations = self.map2locations
        elif self.activemap == "Maze Island":
            locations = self.map3locations

        # loop over locations, print square around
        for l in locations:
            x = l[3]-l[5]
            y = l[4]-l[6]
            self.canvas.create_rectangle((x*16), ((y-30)*16), (x*16+16)-1, ((y-30)*16+16)-1, outline="blue", width=1)
            #self.canvas.create_rectangle((x*16)-1, ((y-30)*16)-1, (x*16+16)+1, ((y-30)*16+16)+1, outline="blue", width=2)


    def drawmap(self):
        canvasposx = 0
        canvasposy = 0

        for y in range(self.mapsizey):
            for x in range(self.mapsizex):
                self.drawtile(canvasposx,canvasposy)
                canvasposx+=1
                if canvasposx== 64:
                    canvasposx = 0
                    canvasposy+= 1

        self.drawlocations()

    def drawtile(self, x, y):
        if self.currentmap[x][y] == "0":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.town_img)
        elif self.currentmap[x][y] == "1":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.cave_img)
        elif self.currentmap[x][y] == "2":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.palace_img)
        elif self.currentmap[x][y] == "3":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.bridge_img)
        elif self.currentmap[x][y] == "4":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.desert_img)
        elif self.currentmap[x][y] == "5":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.grass_img)
        elif self.currentmap[x][y] == "6":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.forest_img)
        elif self.currentmap[x][y] == "7":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.swamp_img)
        elif self.currentmap[x][y] == "8":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.graveyard_img)
        elif self.currentmap[x][y] == "9":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.road_img)
        elif self.currentmap[x][y] == "a":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.lava_img)
        elif self.currentmap[x][y] == "b":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.mountain_img)
        elif self.currentmap[x][y] == "c":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.water_img)
        elif self.currentmap[x][y] == "d":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.water_walk_img)
        elif self.currentmap[x][y] == "e":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.rock_img)
        elif self.currentmap[x][y] == "f":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.spider_img)
        else:
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.error_img)

    def quit(self):
        # Save before exit?
        self.master.quit()

    def mousemove(self, event):
        if self.editenabled == 1:
            c = event.widget
            # Position on canvas
            x, y = c.canvasx(event.x), c.canvasy(event.y)
            # Calculate position on map
            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
           
            # Make sure we are inside borders of the map
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0:
                # Y-axis seems to be offset with 30 on map compared to array
                text = `self.currentmap[x][y]` + " (" + `x` + "," + `y+30` + ")"
                self.coordlabeltext.set(text)
    
                # Print location under cursor
                if self.activemap == "West Hyrule":
                    locations = self.map0locations
                elif self.activemap == "Death Mountain":
                    locations = self.map1locations
                elif self.activemap == "East Hyrule":
                    locations = self.map2locations
                elif self.activemap == "Maze Island":
                    locations = self.map3locations

                self.locationlabeltext.set("")
                for l in locations:
                    if l[3]-l[5] == x and l[4]-l[6] == y+30:
                        text = l[0] + " (" + `l[3]-l[5]` + "," + `l[4]-l[6]` + ") (offset by: " + `l[5]` + "," + `l[6]` + ")"
                        self.locationlabeltext.set(text)
                        break


    def leftclick(self, event):
        if self.editenabled == 1:
            c = event.widget
            # Clicked position on canvas ..
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            # .. Relates to this position in the currentmap ..
            maparrayx = int(x)/16
            maparrayy = int(y)/16

            # Update currentmap 
            self.currentmap[maparrayx][maparrayy] = self.selectedterrain
            # Draw tile
            self.drawtile(maparrayx,maparrayy)
            # Also draw locations over tiles
            self.drawlocations()


            # Calculate map size and update label
            mapstring = ""
            for y in range(self.mapsizey):
                for x in range(self.mapsizex):
                    mapstring += str(self.currentmap[x][y])
            encmapstring = self.mapencode(mapstring)
        
            if self.activemap == "West Hyrule":
                text = `len(encmapstring)/2` + "/" + `self.origmapsize0`
            elif self.activemap == "Death Mountain":
                text = `len(encmapstring)/2` + "/" + `self.origmapsize1`
            elif self.activemap == "East Hyrule":
                text = `len(encmapstring)/2` + "/" + `self.origmapsize2`
            elif self.activemap == "Maze Island":
                text = `len(encmapstring)/2` + "/" + `self.origmapsize3`
            self.mapsizelabeltext.set(text)

    def rightpress(self, event):
        if self.editenabled == 1:
            c = event.widget
            # Mouse down coordinates
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            # Calculate position on map
            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0:
                #print "rightpress", x, ",", y+30
                
                # Find a location to move
                if self.activemap == "West Hyrule":
                    locations = self.map0locations
                elif self.activemap == "Death Mountain":
                    locations = self.map1locations
                elif self.activemap == "East Hyrule":
                    locations = self.map2locations
                elif self.activemap == "Maze Island":
                    locations = self.map3locations

                for p, l in enumerate(locations):
                    if l[3]-l[5] == x and l[4]-l[6] == y+30:
                        #text = "Found:" + l[0] + " (" + `l[3]-l[5]` + "," + `l[4]-l[6]` + ") (offset by: " + `l[5]` + "," + `l[6]` + ")"
                        #print text
                        self.movelocation = p
                        self.movelocationprevx = x
                        self.movelocationprevy = y
                        #print "Start move ", self.movelocation
                        break

    def rightmotion(self, event):
        if self.editenabled == 1:
            c = event.widget
            # Mouse down coordinates
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            # Calculate position on map
            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map, and we found a location to move
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0 and self.movelocation >= 0:
                #print "Moving", self.movelocation, "to", x, ",", y+30
                self.drawtile(self.movelocationprevx,self.movelocationprevy)
                self.canvas.create_rectangle((x*16), ((y)*16), (x*16+16)-1, ((y)*16+16)-1, outline="red", width=1)
                self.movelocationprevx = x
                self.movelocationprevy = y

    def rightrelease(self, event):
        if self.editenabled == 1:
            c = event.widget
            # Mouse down coordinates
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            # Calculate position on map
            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map, and we found a location to move
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0 and self.movelocation >= 0:
                #print "Dropping", self.movelocation, "at", x, ",", y+30

                # Update location
                if self.activemap == "West Hyrule":
                    locations = self.map0locations
                elif self.activemap == "Death Mountain":
                    locations = self.map1locations
                elif self.activemap == "East Hyrule":
                    locations = self.map2locations
                elif self.activemap == "Maze Island":
                    locations = self.map3locations

                locations[self.movelocation][3] = x+locations[self.movelocation][5]
                locations[self.movelocation][4] = y+30+locations[self.movelocation][6]

                self.movelocation = -1 
                self.drawmap()

    def round_down(self, num, divisor):
        return num - (num%divisor)


# End Class 

root = Tk()
app= Zelda2MapEdit(root)
root.mainloop()
