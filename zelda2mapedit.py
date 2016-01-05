#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A simple overworld-editor for Zelda 2 - The Adventure of Link

Author: Johan Björnell <johan@bjornell.se>

Version: 0.1.1

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

        # Call function mouseclick on left click on canvas
        self.canvas.bind("<Button 1>", self.mouseclick)
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

        # Labels
        self.coordlabeltext = StringVar()
        self.coordlabeltext.set("0 ( 00, 00)")
        self.coordlabel = Label(self.btnFrame, textvariable=self.coordlabeltext)
        self.coordlabel.grid(row=0, column=16)
        self.mapsizelabeltext = StringVar()
        self.mapsizelabeltext.set("000 / 000")
        self.mapsizelabel = Label(self.btnFrame, textvariable=self.mapsizelabeltext)
        self.mapsizelabel.grid(row=0, column=17)

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

        # Keep track of original mapsize from rom file
        self.origmapsize0 = 0
        self.origmapsize1 = 0
        self.origmapsize2 = 0
        self.origmapsize3 = 0

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
            #handle = open(self.filename)
            handle = open(self.filename,"r+b")
        except IOError:
            print ("Cannot open file %s" % self.filename)

        # Map 0 
        handle.seek(self.mapstart0)
        # read a byte at a time, decode to mapstring, until size == mapsizex*mapsizey
        mapstring = ""
        self.origmapsize0 = 0 
        while len(mapstring) < self.mapsizex*self.mapsizey:
            self.origmapsize0 += 1
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
        
        # Map 1 
        handle.seek(self.mapstart1)
        mapstring = ""
        self.origmapsize1 = 0 
        while len(mapstring) < self.mapsizex*self.mapsizey:
            self.origmapsize1 += 1
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

        # Map 2
        handle.seek(self.mapstart2)
        mapstring = ""
        self.origmapsize2 = 0 
        while len(mapstring) < self.mapsizex*self.mapsizey:
            self.origmapsize2 += 1
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

        # Map 3
        handle.seek(self.mapstart3)
        mapstring = ""
        self.origmapsize3 = 0 
        while len(mapstring) < self.mapsizex*self.mapsizey:
            self.origmapsize3 += 1
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

        # Close file
        handle.close()

        # Default to West Hyrule
        self.changemap("West Hyrule")
        self.drawmap()

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
        c = event.widget
        x, y = c.canvasx(event.x), c.canvasy(event.y)
        x = int(self.round_down(x, 16))/16
        y = int(self.round_down(y, 16))/16
                
        # y-axis is inverted on map compared to array
        stry = 74-y
        # Add a zero at the beginning if value less than 10
        # Make into a string in either case
        if stry < 10:
            stry = "0"+`stry`
        else:
            stry = `stry`
        if x < 10:
            strx = "0"+`x`
        else:
            strx = `x`

        text = `self.currentmap[x][y]` + " (" + strx + ", " + stry + ")"
        self.coordlabeltext.set(text)

    def mouseclick(self, event):
        if self.editenabled == 1:
            c = event.widget
            # Clicked position on canvas ..
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            # .. Relates to this position in the currentmap ..
            maparrayx = int(x)/16
            maparrayy = int(y)/16

            # .. and to this position to put the new terrain on the canvas
            x = int(self.round_down(x, 16))
            y = int(self.round_down(y, 16))

            # Update currentmap 
            self.currentmap[maparrayx][maparrayy] = self.selectedterrain
            # Draw tile
            self.drawtile(maparrayx,maparrayy)

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

    def round_down(self, num, divisor):
        return num - (num%divisor)


# End Class 

root = Tk()
app= Zelda2MapEdit(root)
root.mainloop()
