#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A simple overworld-editor for Zelda 2 - The Adventure of Link

Author: Johan Björnell <johan@bjornell.se>

"""

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfile
import sys, tkMessageBox


class Zelda2MapEdit:

    def __init__(self, master):
        
        ###  User interface
        self.master = master
        self.master.title("Zelda2MapEdit")
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        maxw = 1040
        maxh = 1260
        self.master.maxsize(width=maxw, height=maxh)

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        if sh > maxh:
            sh = maxh
        if sw > maxw:
            sw = maxw

        self.master.geometry('%dx%d+%d+%d' % (sw, sh-100, 100, 0))

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

        # Bind mouse actions to functions
        self.canvas.bind("<ButtonPress-1>", self.leftpress)
        self.canvas.bind("<B1-Motion>", self.leftmotion)
        self.canvas.bind("<ButtonRelease-1>", self.leftrelease)
        self.canvas.bind("<ButtonPress-3>", self.rightpress)
        self.canvas.bind("<B3-Motion>", self.rightmotion)
        self.canvas.bind("<ButtonRelease-3>", self.rightrelease)
        self.canvas.bind("<Motion>", self.mousemove)

        # Tool images
        self.img_breakpoint = PhotoImage(data = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACO0lEQVQ4T5XTX0hTURwH8O+5d+6fs5nTwiUy6CESESywIoz8V0FIvQkLgoiiyIigKCLoqRcpMdJCifYU6x80htayPzgXKIXRiB4Ks5ESue50tnt3/58TE4oWGvO8nu/3A+f8ziEocMk1NQH2cdoPl8VEiXPAsdZ2iUxMLZBC+krrhi42Jpxl1ARWWUGcBPA4ZOrxrC8IUA9vD7HP2EdHXgO+ChA3D5KDyt1DBQH68ZYw19Larpy5AY5JQKUbpMwBUl2BJQG2rcoBjRKIJbxWjTvc3sZ2Qg2whAA2+Q3MxsCtWw1G7T/yALarrlizsYdM0WpZSqK822HnO9rWgOOhR2LQZgRYbaWAzMAUE9D55jxA9W+JoKx0NzISaCoN6/5mQDehDo9CmZqD9F0GLxsHKymNSCLjXJBm8wDt6M6XqNvUhGQSNJtB0UYftNAw5K8/IScV6PPmLZ+SPvL35PKBAw3H4PHcZIoBkpiBbuGQnZ6HMqsCoqHzPPV6MxlhWSC3QRurorBYdygyAxEkyBKFumCgmBHYCddgzabe/BcIB4N3m66e77CmszBVDpxoAhoFwGCA1buk9LtlgaEnz3vjJk7UX7l4aM/b9/5skbONqOZingAfHOJc7b8v988dhMKPL6uSeOH2q/HOp33dfbmg5CzfDJ6eBIOXJ1ynPSN8WhKIxsZPCclkz+Dgo3OBQKCrkP/xO0Mm4vGtXyYTY9HRaM/1a92nV1JePNqLkdiD+8F7z/r7ewdWWs7lfwHT2viKQFiEyQAAAABJRU5ErkJggg==")
        self.img_breakpoint = PhotoImage(data = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACOklEQVQ4T53RX0hTURwH8O+5m3e77s67jSCxG5ZYoA89JGHzwSL6hxL9kXoqIUG0pGiEUVKtQIuiGsuSUVBIZOWD2INEklBZueQ2SdKyWv+u5JxlbjavG+uccFHz0XYefpyH8/3w5fwIAFy92Rq2RKd92yvKV7N2d0n0R7gYwTE7QpMcJrR0EuFeGppbKjTX4UW67CwJcRj4Hft7Z7JkZrz48GVkaUDNJI2143yObKORCJj/I+hoGBifAiBhKmdxf5o5tiwtex50jIPR1ZbIJsbjt3616Gm3/Mu5G7SsFESygb1/lwC4UAzxrxq+hSZgzhYhLM+FngGGG0+SQNerN6rd55Vxshpc2UYQyQr6egg0MAEuHEM8GMXYZARilgBTYR70eh0MnvtJoLNvQF3p88ppp/eCbC0FsUigg0Ogo3ME7vYoarGvVxZcDqBsE4gkgQ4Mgo6G/jQY0TA2FYG4QISpIBccAYRrD5MNWh48Utf2++QMz1GwzetABGEY/k9eGgy34bsWpVG+LhgIFogLRaTny9AzCuMtbxK4fq9rZIu3O9PS3HBb27a+Mf1Cx7OZz/17VPsGG/ncd56fb+oQ87OGuXg8w3jneee/LTS1trOC6Z89heU7i2YH53JP1LjovsysS/KUXSVrVswlNPtNAqg/dZZZbValproyNeD4iXpmNotK7cEDqQGHjhxjJqOgOJ11qQEORy3T8bxy7kxDakDVnn2MEE7xNLlTAyqraiKEEOWK59Kq/93Cb5Ba6BH9oub7AAAAAElFTkSuQmCC")
        self.img_open = PhotoImage(data = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACHElEQVQ4T6WTTUgVURiGn+/MHRWviyCodT+S3oXLdq2CgnBn0f8P1KaNC5dBixYRolBB0jXBkktZiasWtXBTLYwCN5mCYKlFkFSCxUXvzDlfnDNjdxcXmuHwzQznPO/7/Yzwn5fM9tDT3FYsO+INFIzYlqT6q680QaURtsxf2mH3XHtgJLKIVdLNKsv9vewbXpWGAB96u7R0+xGsz4Jz0Frk/eWLdI1+bwzw6myHHhi9C6sLYBWaYxbKE/z+9Jm4zaCa+1DF34hBxKcq/FyeuyoBMFKGb/OocwgOtu3K3ISlYC04v/JvYqBgeHeljwxQHoLVOdRKdgCH+Lh1yKaQppAkYDfwRrzT1wPDyNSpTj14zwPm0cRBbQ2trmUbvWKaQGohKkLUAoU2RB3SVGDqxh3k2dF27S5fRxefo5vrmYpXS1PUx1zdP6tNEI0xxZ2Y7bt5cethDug/ja7MoM6EQqpXtLVMOYAc6t89LKkhtSqF2DA5vow87m7X4zfPo0tvshpYi3rbQdnifNyqgfXuHKgjloTJJys5YOAkujSNS6O6ZestZw7+ppGDjLMUIsf4069I5fBePTN4DP04jQsOHC6tBdt1ZYsGJ0mokajSFBsqHjB2pEPPDZ2AxZeQmrpi2Jyrh/blrfTDFgGxYWzkCzJYar2//1DnhWb7A+tVQ+815OmXsw7jHM63NJ/KQgSbCbydWa80NO//+qn+AMFxYT4s9F/IAAAAAElFTkSuQmCC")
        self.img_save = PhotoImage(data = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC+UlEQVQ4T5WSX2hbdRTHP7+be9Om6domW5YmsVlry7q0KlXonpRJsRXFF1GYMPFFcAi+jLHB9iAKk6IoPshEEHxRFFHBBy2rWrQ43WxXt6nZktqUrbQbbf41MSY39yb3SJIJ+jDB83Yezud8+ZyjXv4xI0rXsdHx1kt0trfhuKRIXbpQCgW4XDqGboAI+dw25wsGW9tl/9lDe/LqxbMZOTjm5+uc4qE/U4zuC4E0xgABNA+p1WsspjYZHwzibnPzoRVm7sIGuXwtrE58tyV39nexUHDx6B8JHh4JUqxrzc11Rwjt7uHEmx9xdeB+prILDI3G+HbnPficMrMXsqhj32xKbKCbxaLBVOEyDw4HKDk6CsERoc/fyfRnP5GdnGT0+xnCgQAz/nH62y2WEjnU0dkNGRrwNQGTuSUm9gYoyS2AI/Tt7uH46c9JDE8xsTZL7K4YZ/z7CRtmC/Dcxyty91iYhbzBZOYcj4wEKIq7mUAc2LHDy9wv10mvLNMT7aetXeer7nEihsnPV7Oow5+kZGgkxKLt4d7EPBN97ZRVC/C3R2+HB7cLdLvKF8sF4iMH6LVK/BrfRD3/6ar07o3w+w/n0deTODUb0bTWFW5VCwWa44DLwN0/TNvYfpKX11BPv58Q32Avh30ZRvcN/mvwdk08keKlG362kpuoZz5IihENciSQIeDrYebLOaRmUzbLVComVqVCxapimybpdJrp16dJ57c5ds1HIbmBOvTeFZE9QU6G880EIjQe8D+rkeCFlS5KiRuop979TcxokFPRwv9K8Gy8Eyu5jnri7UtSioZ5Y7BIJLSTbG4bl6YhIoiS1luLoDSwqzV27fJzcyvPwYteWF5DPX56SdKhCO/ESs0Es2fmqdkWFbNCpVym2nBhVrGqJrlslldePdV08Ng5D0ZqDfXAW3GpDoV5rXuVA/fdQSVbRHO1FDRUNE/YEIOiXq/T4fcxf2mdJ6/34bl4BRU5Pi+OKKyyTcGq/UPe7U26dQ2vqtPR3cFfLQlxpBs2xAwAAAAASUVORK5CYII=")
        self.img_edit = PhotoImage(data = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACTElEQVQ4T5WTX0hTcRTHv3eh7k7c2oTC9RdkrrFdJdd0kom1lJIwcA+h0Muit4oegsKKoCSjNwlfQguySCU0M0vDSiqdmjXZdql770DNbLh/rpjOed0KJ63GjNnv+Xw/n/PjnEPgP964kXynrCnQLdCu+VCvc7d8yD9FrDc/fe4gy+SXKnKGbmCbRwjfSBB+MalcF8BSvd3mPW7SlB6+gq7LZ0DV3YIiDZjdkYGkgFFjLqt7pFd8cd3Gm64TqD7ZhI6zp6BtaIRMmQRgPkrZ8tv2aoi0ZqQ4ebheAW20CceuN8NyvhaZ/fVj/+xg8IiK1baXKARkE5aZMIR+IDQlhrntB6zZJhgkATt1qZ1aE/BSv8lW1GvQpEg6wDOhaNhjl8JDC5AhXoRzeJ4r6EPOygASAL1aGbvnzi6FNNeKEBuAcG417LYREEmX4OEkdt2DGer39OIAz6iNtsKHKo1MzSDI+GJmN01AJObhspJcYacrak4APM1NZ/X38xSZ1GcEWd8fM02AlPD4Ni60Fz92x8xxgNbN6Cm+p6vYUk4jyCz89WcCpJjH9EchV9LtjjPHAfortj439Lw+xE+qIfi6BB8nhde+2vbE+1R7aY83wRwDPDkgKddeuNYnLzsNTNZibrARzpEw0mUbwJkFXNkL/5rmGOCqCNqalptj2VVFgMeKyMxbOFo6QQ+k0FUfAppkt0I0qIQXzZ8W6+rvViJrZwSO1mEwo8Fuo2W+Mlk4ugeNatFP9/fF5azUyP59ZXKSD4cdeU2zE+sJr9T8Aolx7FvIXRiTAAAAAElFTkSuQmCC")

        # Terrain images 
        self.img_0 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQICAgICAgICAgICAgICAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v/AQP/AQAEBAYCAgICAgICAgICAgP7+/v/AQP/AQP/AQP7+/v7+/gEBAQEBAf7+/v/AQAEBAYCAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP7+/v7+/gEBAQEBAf7+/gEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP/AQAEBAYCAgICAgP7+/gEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQAEBAYCAgICAgP7+/oCAgP7+/gEBAQEBAf7+/v7+/v7+/v7+/v7+/v/AQP/AQAEBAYCAgICAgP7+/v7+/v7+/oCAgP7+/gEBAQEBAQEBAQEBAf7+/v7+/v/AQAEBAYCAgICAgICAgP7+/v7+/v7+/oCAgICAgP7+/gEBAQEBAQEBAf7+/v7+/v/AQAEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/gEBAf7+/v7+/v7+/v7+/v/AQP/AQAEBAf7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAQEBAf7+/v7+/v7+/v7+/v/AQP/AQAEBAf7+/v7+/v7+/gEBAf7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/v7+/v7+/gEBAf7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_1 = PhotoImage(data = "R0lGODlhEAAQAPAAAAEBAQAAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAAAg6Ej6nL7Q+jnLTai7M+BQA7")
        self.img_2 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_3 = PhotoImage(data = "R0lGODlhEAAQAPcAAP7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBASH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_4 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_5 = PhotoImage(data = "R0lGODlhEAAQAPcAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_6 = PhotoImage(data = "R0lGODlhEAAQAPcAAIDAAAEBAQCgAIDAAIDAAACgAIDAAAEBAQCgAIDAAIDAAIDAAAEBAQCgAIDAAIDAAAEBAQEBAQCgAACgAAEBAYDAAAEBAQEBAQCgAAEBAYDAAAEBAQCgAACgAACgAIDAAAEBAQCgAACgAAEBAQCgAAEBAQEBAQCgAACgAACgAIDAAAEBAQCgAACgAACgAIDAAAEBAQCgAAEBAQEBAQCgAACgAAEBAQCgAACgAACgAAEBAQEBAQEBAQCgAACgAACgAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAACgAACgAAEBAQCgAAEBAQCgAAEBAQCgAAEBAQEBAQCgAACgAACgAAEBAQEBAQEBAQCgAAEBAQCgAACgAAEBAQEBAYDAAAEBAQCgAAEBAQEBAQCgAACgAACgAAEBAQCgAACgAAEBAQCgAACgAACgAIDAAIDAAIDAAAEBAQEBAQCgAACgAACgAAEBAQEBAQCgAAEBAQEBAQEBAQCgAACgAACgAIDAAIDAAAEBAQEBAQCgAACgAACgAACgAACgAAEBAQEBAQEBAQCgAACgAACgAACgAIDAAAEBAQEBAQCgAAEBAQCgAACgAACgAACgAAEBAQEBAQCgAACgAACgAACgAACgAAEBAQEBAQEBAQEBAQCgAACgAACgAACgAAEBAQEBAQCgAAEBAQCgAACgAACgAACgAACgAAEBAQEBAQCgAAEBAQCgAACgAACgAIDAAAEBAQEBAQCgAACgAACgAACgAACgAAEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAQEBAYDAAAEBAQCgAAEBAQCgAACgAAEBAQCgAAEBAYDAAAEBAQEBAQEBAQEBAYDAAAEBAQEBAQEBAQEBAQCgAAEBAQEBAYDAAIDAAAEBAQCgAACgAAEBAQEBAYDAAAEBAQEBAQCgAAEBAYDAAAEBAQEBAYDAAIDAAIDAAIDAAAEBAQEBAQCgAIDAAIDAAAEBAQCgAACgAACgAIDAAAEBAQEBAYDAAACgAIDAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_7 = PhotoImage(data = "R0lGODlhEAAQAPcAAAEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAAEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAIDAAAEBAQCgAAEBAQCgAACgAACgAAEBAYDAAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAACgAACgAACgAAEBAYDAAAEBAYDAAAEBAQCgAACgAACgAAEBAYDAAAEBAYDAAAEBAQEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAAEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAIDAAAEBAQCgAAEBAQCgAACgAACgAAEBAYDAAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAACgAACgAACgAAEBAYDAAAEBAYDAAAEBAQCgAACgAACgAAEBAYDAAAEBAYDAAAEBASH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_8 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v7+/v7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v7+/v7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAcBAAMBAAP/AQMBAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAcBAAP/AQMBAAP/AQP/AQMBAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_9 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_a = PhotoImage(data = "R0lGODlhEAAQAPcAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_b = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQAEBAQEBAQEBAQEBAQEBAQEBAcBAAP/AQMBAAMBAAAEBAQEBAQEBAcBAAP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAcBAAAEBAQEBAQEBAcBAAP7+/gEBAcBAAAEBAQEBAQEBAQEBAQEBAf7+/sBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAP7+/gEBAQEBAcBAAAEBAQEBAf7+/sBAAMBAAAEBAQEBAcBAAMBAAAEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAcBAAMBAAP7+/sBAAAEBAcBAAMBAAAEBAQEBAcBAAMBAAP7+/gEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAP7+/gEBAcBAAMBAAMBAAMBAAAEBAQEBAQEBAcBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAP7+/gEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAAEBAQEBAcBAAMBAAMBAAP7+/sBAAMBAAAEBAQEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAP7+/gEBAQEBAQEBAcBAAMBAAP7+/sBAAAEBAQEBAcBAAMBAAAEBAQEBAcBAAMBAAMBAAP7+/gEBAcBAAMBAAAEBAcBAAAEBAQEBAQEBAcBAAAEBAQEBAcBAAMBAAP7+/sBAAP7+/v7+/gEBAcBAAAEBAcBAAAEBAQEBAQEBAQEBAQEBAcBAAMBAAAEBAcBAAP7+/sBAAP7+/gEBAQEBAcBAAMBAAAEBAQEBAcBAAAEBAQEBAcBAAMBAAAEBAcBAAMBAAMBAAMBAAP7+/gEBAcBAAMBAAAEBAcBAAMBAAAEBAcBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAP/AQAEBAcBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAf/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_c = PhotoImage(data = "R0lGODlhEQAQAPEAAAEBAUDA/8DAwP7+/iH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABEAEAAAAi5cjmF5gsAORC7apuxK9caObIkBPhZQiSEjqIcbdBMzx57lwG5524zuo51SGlYBADs=")
        self.img_d = PhotoImage(data = "R0lGODlhEQAQAPEAAAEBAZnZ6sDAwP7+/iH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABEAEAAAAi5cjmF5gsAORC7apuxK9caObIkBPhZQiSEjqIcbdBMzx57lwG5524zuo51SGlYBADs=")
        self.img_e = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/sBAAMBAAP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/sBAAMBAAP7+/v7+/sBAAP7+/v7+/sBAAAEBAf/AQP/AQP/AQP7+/v7+/sBAAMBAAP7+/v7+/sBAAMBAAMBAAMBAAMBAAP7+/sBAAAEBAf/AQP/AQP7+/sBAAP7+/v7+/sBAAP7+/v7+/v7+/sBAAMBAAMBAAMBAAMBAAAEBAf/AQP7+/v7+/sBAAP7+/sBAAMBAAMBAAMBAAP7+/v7+/sBAAMBAAMBAAAEBAQEBAQEBAf/AQP7+/v7+/sBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAAEBAQEBAf7+/v7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAAEBAQEBAQEBAf/AQP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAAEBAQEBAQEBAf/AQP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAAEBAQEBAf/AQMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAAEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAMBAAAEBAcBAAAEBAQEBAcBAAAEBAQEBAQEBAcBAAMBAAAEBAcBAAMBAAMBAAAEBAQEBAQEBAQEBAQEBAcBAAMBAAAEBAQEBAQEBAcBAAMBAAMBAAAEBAQEBAQEBAcBAAAEBAQEBAcBAAMBAAAEBAQEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAcBAAAEBAQEBAcBAAAEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAf/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_f = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAf/AQAEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/v7+/gEBAf7+/v7+/gEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/gEBAQEBAQEBAf7+/gEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAQEBAQEBAQEBAQEBAf/AQAEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQAEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAf/AQAEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAf/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_error = PhotoImage(data = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC3UlEQVQ4T42Tz2tcVRTHP+e+H/N7pk2acSYzyoAmC38hRJBQqW5E6s6FWKktDaVVof0PhNKFf4GiUIUiuBDBjQu7EoQWleqiSCGxlRiSmNS0k8wk8978eO/dK+++LFx6Npd7zzmfc7jnewQgXDozouDkSEx6zcwRQEDSE4g1cOgXhRlG49KXX+UlWHrXOK/NwTgBkwaJzTHdAWYysTnieZipImJMxhCD8T2iH/6M5eC9c8Z/cRYzGJH6UzNhwMTMU3h/yTYx/Ow6vl5BSqUMoDVS8hnfeYD0z582uYVZTDABVEbv9Ujqi5QvX7TAwcfXcLZvIbUj2CoaVNFlmAJ6594xhRea6DCy1WwHvT2S9gnKly5kgE8+x9n4Ean+B1BwCO/uIHtnT5ni83V0OAFR4LiYfo8oN0f16ocWsH/lI9xwGVU7ClEESYLkPcI/usjumbdM6Zk6OnYxSQTDIWZrk1B1OHb9mgU8On+R/GQVp9mCfMEWUk7CYGUXebR02lQ6ZeLVNcxuF0ZD9PYD+qV52r/8ZAGbi8ep9ZdRjSb4OWTqGOrJNoP1IbL96nFT8/ZIDkagFLiuhXSDIq3bd+zb3wvPMVUIIFeAOII4wSnm6Ztp5K9W3Tw2N0Uc2QGnM8JJEh6u9Wj+fg8RYevZOWYer5CIn/2y1niOsL22h6x2WqY5WyaKEjueFJP3HP5Z3mC91sBzc8zsrtN4qkk8yQJSufmOsPUwRO63mqbVOAQYUCLog33u1To0PriAoNn69Avmu2s45Qr6UI2eUmz0QmSl2TBPTJeIUq1rgxLFeHOTu2+8ySvffG07vvn2KZ7+7lty7TY6ybpIAav7IbJcr5tOrcTYOgwKIdrZ4dfFl3n9xg0L+P7kSV66dRN/ZgatM70XRHE/CJHfjkxHC7WKG6WLlPrS5dGafr9vz2x5FNVqFXO4maLBFbgdBLEV78+VoyMfyWVf/P8s0Hp8Iujl/wU4gUfgnVm30AAAAABJRU5ErkJggg==")

        # Set window icon
        self.master.tk.call('wm', 'iconphoto', root._w, self.img_2)

        # Frame with labelframes
        self.btnFrame = Frame(root, height=60, padx=5)
        self.btnFrame.grid(row=0, column=0, sticky="W")

        # Labelframes
        self.fileFrame = LabelFrame(self.btnFrame, text="File", padx=5, pady=5)
        self.fileFrame.grid(row=0, column=0)
        self.terrainFrame = LabelFrame(self.btnFrame, text="Terrain", padx=5, pady=5)
        self.terrainFrame.grid(row=0, column=1)
        self.toolFrame = LabelFrame(self.btnFrame, text="Tools", padx=5, pady=5)
        self.toolFrame.grid(row=0, column=2)
        self.coordFrame = LabelFrame(self.btnFrame, text="Coordinates", padx=5, pady=5, width=70)
        self.coordFrame.grid(row=0, column=3)
        #self.coordFrame.grid_propagate(0)
        self.sizeFrame = LabelFrame(self.btnFrame, text="Size", padx=5, pady=5)
        self.sizeFrame.grid(row=0, column=4)

        # Buttons
        self.openbtn = Button(self.fileFrame, image=self.img_open, command=self.openromfile)
        self.openbtn.grid(row=0, column=0)
        self.savebtn = Button(self.fileFrame, image=self.img_save, state="disabled", command=self.saveromfile)
        self.savebtn.grid(row=0, column=1)

        self.tile_0_btn = Button(self.terrainFrame, image=self.img_0, command=lambda: self.selectterrain("0"))
        self.tile_0_btn.grid(row=0, column=0)
        self.tile_1_btn = Button(self.terrainFrame, image=self.img_1, command=lambda: self.selectterrain("1"))
        self.tile_1_btn.grid(row=0, column=1)
        self.tile_2_btn = Button(self.terrainFrame, image=self.img_2, command=lambda: self.selectterrain("2"))
        self.tile_2_btn.grid(row=0, column=2)
        self.tile_3_btn = Button(self.terrainFrame, image=self.img_3, command=lambda: self.selectterrain("3"))
        self.tile_3_btn.grid(row=0, column=3)
        self.tile_4_btn = Button(self.terrainFrame, image=self.img_4, command=lambda: self.selectterrain("4"))
        self.tile_4_btn.grid(row=0, column=4)
        self.tile_5_btn = Button(self.terrainFrame, image=self.img_5, command=lambda: self.selectterrain("5"))
        self.tile_5_btn.grid(row=0, column=5)
        self.tile_6_btn = Button(self.terrainFrame, image=self.img_6, command=lambda: self.selectterrain("6"))
        self.tile_6_btn.grid(row=0, column=6)
        self.tile_7_btn = Button(self.terrainFrame, image=self.img_7, command=lambda: self.selectterrain("7"))
        self.tile_7_btn.grid(row=0, column=7)
        self.tile_8_btn = Button(self.terrainFrame, image=self.img_8, command=lambda: self.selectterrain("8"))
        self.tile_8_btn.grid(row=0, column=8)
        self.tile_9_btn = Button(self.terrainFrame, image=self.img_9, command=lambda: self.selectterrain("9"))
        self.tile_9_btn.grid(row=0, column=9)
        self.tile_a_btn = Button(self.terrainFrame, image=self.img_a, command=lambda: self.selectterrain("a"))
        self.tile_a_btn.grid(row=0, column=10)
        self.tile_b_btn = Button(self.terrainFrame, image=self.img_b, command=lambda: self.selectterrain("b"))
        self.tile_b_btn.grid(row=0, column=11)
        self.tile_c_btn = Button(self.terrainFrame, image=self.img_c, command=lambda: self.selectterrain("c"))
        self.tile_c_btn.grid(row=0, column=12)
        self.tile_d_btn = Button(self.terrainFrame, image=self.img_d, command=lambda: self.selectterrain("d"))
        self.tile_d_btn.grid(row=0, column=13)
        self.tile_e_btn = Button(self.terrainFrame, image=self.img_e, command=lambda: self.selectterrain("e"))
        self.tile_e_btn.grid(row=0, column=14)
        self.tile_f_btn = Button(self.terrainFrame, image=self.img_f, command=lambda: self.selectterrain("f"))
        self.tile_f_btn.grid(row=0, column=15)
        
        self.breakpointbtn = Button(self.toolFrame, image=self.img_breakpoint, command=lambda: self.selectterrain("x"))
        self.breakpointbtn.grid(row=0, column=0)
        self.editlocationbtn = Button(self.toolFrame, image=self.img_edit, command=lambda: self.selectterrain("y"))
        self.editlocationbtn.grid(row=0, column=1)

        # Labels 
        self.coordlabeltext = StringVar()
        self.coordlabeltext.set("'0' (0, 0)")
        self.coordlabel = Label(self.coordFrame, textvariable=self.coordlabeltext)
        self.coordlabel.grid(row=0, column=0, pady=2)

        self.mapsizelabeltext = StringVar()
        self.mapsizelabeltext.set("000 / 000")
        self.mapsizelabel = Label(self.sizeFrame, textvariable=self.mapsizelabeltext)
        self.mapsizelabel.grid(row=0, column=0, pady=2)

        # Frame for label in the bottom
        self.labelFrame = Frame(root, height=60)
        self.labelFrame.grid(row=3, column=0)

        self.locationlabeltext = StringVar()
        self.locationlabeltext.set("")
        self.locationlabel = Label(self.labelFrame, textvariable=self.locationlabeltext)
        self.locationlabel.grid(row=0, column=0)
        
        ### Menues
        self.menubar = Menu(self.master)
        # File
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open..", command=self.openromfile)
        self.filemenu.add_command(label="Save", command=self.saveromfile)
        self.filemenu.entryconfig("Save", state="disabled")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        # Map
        self.mapmenu = Menu(self.menubar, tearoff=0)
        self.mapmenu.add_command(label="West Hyrule", command=lambda: self.changemap(0))
        self.mapmenu.entryconfig("West Hyrule", state="disabled")
        self.mapmenu.add_command(label="Death Mountain", command=lambda: self.changemap(1))
        self.mapmenu.entryconfig("Death Mountain", state="disabled")
        self.mapmenu.add_command(label="East Hyrule", command=lambda: self.changemap(2))
        self.mapmenu.entryconfig("East Hyrule", state="disabled")
        self.mapmenu.add_command(label="Maze Island", command=lambda: self.changemap(3))
        self.mapmenu.entryconfig("Maze Island", state="disabled")
        self.menubar.add_cascade(label="Map", menu=self.mapmenu)
        # Options
        self.optionsmenu = Menu(self.menubar, tearoff=0)
        self.optionsmenu.add_command(label="Hidden locations..", command=self.hiddenlocations)
        self.menubar.add_cascade(label="Options", menu=self.optionsmenu)
        # Help
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About..", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

        ### Variables
        # Map size
        self.mapsizex = 64
        self.mapsizey = 75

        # Original mapsizes
        self.origmapsizes = [ 801, 803, 794, 803 ]

        # Selected terrain to draw on map (0-f)
        self.selectedterrain = "c"
        self.tile_c_btn.config(relief=SUNKEN)

        # Array to contain decoded mapstrings
        self.maparray = [[0 for y in range(self.mapsizey * 4)] for x in range(self.mapsizex)]

        # Map data locations in ROM
        self.mapstartlocations = [ int("506C", 16),  # West Hyrule
                                   int("665C", 16),  # Death Mountain
                                   int("9056", 16),  # East Hyrule
                                   int("A65C", 16) ] # Maze Island

        # Keep track of active map
        # 0 = West Hyrule, 3 = Maze Island etc.
        self.activemap = 0

        # Filename
        self.filename = ""

        # Enable edit after file open
        self.editenabled = 0
        # Ask to save if edited
        self.edited = 0

        # List of list of breakpoints
        self.breakpoints = [ [], [], [], [] ]

        # Locations on map
        # Format:
        # [ Name, Rom address for x-value, Rom address for y-value, x.value, y-value, x-offset, y-offset, Rom address for palace pointer ]
        self.maplocations = [[[ "North Castle", "466E", "462F", 0, 0, 0, 0, 0 ],
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
                             [ "Parapa Palace", "46A2", "4663", 0, 0, 0, 128, 0 ],
                             [ "Midoro Swamp Palace", "46A3", "4664", 0, 0, 0, 128, 0 ]],
                             [[ "Island Palace", "46A4", "4665", 0, 0, 0, 128, 0 ],
                             [ "Cave B West Exit", "614B", "610C", 0, 0, 0, 0, 0 ],
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
                             [ "Maze Palace", "617F", "6140", 0, 0, 0, 128, 0 ],
                             [ "Maze Island Child", "6182", "6143", 0, 0, 0, 0, 0 ],
                             [ "Death Mountain's Magic Container", "6183", "6144", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 3", "6184", "6145", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 7", "6185", "6146", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 4", "6186", "6147", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 5", "6187", "6148", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 6", "6188", "6149", 0, 0, 0, 0, 0 ]],
                             [[ "Forest with 500 Exp. bag west of Nabooru", "866E", "862F", 0, 0, 0, 0, 0 ],
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
                             [ "500 exp. bag on beach near Ocean Palace", "8685", "8646", 0, 0, 0, 0, 0 ],
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
                             [ "New Kasuto *", "869F", "8660", 0, 0, 0, 0, 0 ],
                             [ "Old Kasuto", "86A1", "8662", 0, 0, 64, 128, 0 ],
                             [ "Ocean Palace", "86A2", "8663", 0, 0, 0, 128, 0 ],
                             #[ "Call location for Hidden Palace", "8388", "8382", 0, 0, 0, 0, 0 ],
                             #[ "Hidden Palace", "86A3", "1DF78", 0, 0, 0, 128, 0 ],
                             #[ "Hidden Palace", "86A3", "8664", 0, 0, 0, 128, 0 ],
                             [ "Great Palace", "86A4", "8665", 0, 0, 0, 128, 0 ]],
                             [[ "Cave B West Exit", "A14B", "A10C", 0, 0, 0, 0, 0 ],
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
                             [ "Maze Palace", "A17F", "A140", 0, 0, 0, 128, 0 ],
                             [ "Maze Island Child", "A182", "A143", 0, 0, 0, 0, 0 ],
                             [ "Death Mountain's Magic Container", "A183", "A144", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 3", "A184", "A145", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 7", "A185", "A146", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 4", "A186", "A147", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 5", "A187", "A148", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 6", "A188", "A149", 0, 0, 0, 0, 0 ]]]

        # Keep track of location to move
        self.movelocation = -1
        self.movelocationprevx = -1
        self.movelocationprevy = -1

        # Palace 6 and new Kasuto hidden or visible
        # (not implemented yet)
        self.palace6hidden = IntVar()
        # New Kasuto hidden
        self.newkasutohidden = IntVar()

    # End __init__

    def hiddenlocations(self):
        hlWindow = Toplevel(self.master, padx=5, pady=5)
        hlWindow.resizable(0,0)
        hiddenLocationsLF = LabelFrame(hlWindow, text="Hidden locations", padx=5, pady=5)
        hiddenLocationsLF.grid(row=1, column=1, columnspan=3)
        palace6CB = Checkbutton(hiddenLocationsLF, text="Palace 6", variable=self.palace6hidden).grid(row=1, column=1, sticky=W)
        newKasutoCB = Checkbutton(hiddenLocationsLF, text="New Kasuto", variable=self.newkasutohidden).grid(row=2, column=1, sticky=W)
        Button(hlWindow, text="Close", command=hlWindow.destroy).grid(row=5,column=3)


    def about(self):
        aboutWindow = Toplevel(self.master)
        Label(aboutWindow, text="Zelda2MapEdit - by matal3a0\n\nLatest source available from:\nhttps://github.com/matal3a0/Zelda2MapEdit").pack(padx=10, pady=10)
        Button(aboutWindow, text="Close", command=aboutWindow.destroy).pack(pady=10)

    def selectterrain(self, terrain):
        # Raise buttons
        self.tile_0_btn.config(relief=RAISED)
        self.tile_1_btn.config(relief=RAISED)
        self.tile_2_btn.config(relief=RAISED)
        self.tile_3_btn.config(relief=RAISED)
        self.tile_4_btn.config(relief=RAISED)
        self.tile_5_btn.config(relief=RAISED)
        self.tile_6_btn.config(relief=RAISED)
        self.tile_7_btn.config(relief=RAISED)
        self.tile_8_btn.config(relief=RAISED)
        self.tile_9_btn.config(relief=RAISED)
        self.tile_a_btn.config(relief=RAISED)
        self.tile_b_btn.config(relief=RAISED)
        self.tile_c_btn.config(relief=RAISED)
        self.tile_d_btn.config(relief=RAISED)
        self.tile_e_btn.config(relief=RAISED)
        self.tile_f_btn.config(relief=RAISED)
        self.breakpointbtn.config(relief=RAISED)
        self.editlocationbtn.config(relief=RAISED)

        # Set terrain and sink the button
        self.selectedterrain = terrain
        if terrain == "0":
            self.tile_0_btn.config(relief=SUNKEN)
        elif terrain == "1":
            self.tile_1_btn.config(relief=SUNKEN)
        elif terrain == "2":
            self.tile_2_btn.config(relief=SUNKEN)
        elif terrain == "3":
            self.tile_3_btn.config(relief=SUNKEN)
        elif terrain == "4":
            self.tile_4_btn.config(relief=SUNKEN)
        elif terrain == "5":
            self.tile_5_btn.config(relief=SUNKEN)
        elif terrain == "6":
            self.tile_6_btn.config(relief=SUNKEN)
        elif terrain == "7":
            self.tile_7_btn.config(relief=SUNKEN)
        elif terrain == "8":
            self.tile_8_btn.config(relief=SUNKEN)
        elif terrain == "9":
            self.tile_9_btn.config(relief=SUNKEN)
        elif terrain == "a":
            self.tile_a_btn.config(relief=SUNKEN)
        elif terrain == "b":
            self.tile_b_btn.config(relief=SUNKEN)
        elif terrain == "c":
            self.tile_c_btn.config(relief=SUNKEN)
        elif terrain == "d":
            self.tile_d_btn.config(relief=SUNKEN)
        elif terrain == "e":
            self.tile_e_btn.config(relief=SUNKEN)
        elif terrain == "f":
            self.tile_f_btn.config(relief=SUNKEN)
        elif terrain == "x":
            self.breakpointbtn.config(relief=SUNKEN)
        elif terrain == "y":
            self.editlocationbtn.config(relief=SUNKEN)

    def openromfile(self):
        # Save before?
        if self.edited != 0:
            result = tkMessageBox.askyesnocancel("Zelda2MapEdit", "Save before opening new file?") 
            if result is True:
                self.saveromfile()

        # Open file dialog
        options = {}
        options['defaultextension'] = '.nes'
        options['filetypes'] = [('Rom files', '.nes'), ('all files', '.*')]
        options['title'] = 'Open romfile'
        self.filename = askopenfilename(**options)
        
        # Open rom file
        if self.filename:
            try:
                handle = open(self.filename,"r+b")
            except IOError:
                message = "Cannot open file %s" % self.filename
                tkMessageBox.showerror("Cannot open file", message)
                return
        else:
            return
        # Clean breakpoints
        self.breakpoints = [ [], [], [], [] ]

        # Loop over the four startlocations in rom
        for index, maplocation in enumerate(self.mapstartlocations):
            yoffset = index*self.mapsizey # Offset in maparray depending on which map
            handle.seek(maplocation)
            # Read a byte at a time, decode to mapstring, until size == mapsizex*mapsizey
            # Also find breakpoints in map
            mapstring = ""
            prevterrain = ""
            prevcount = ""
            xcount = 0
            ycount = 0
            while len(mapstring) < self.mapsizex*self.mapsizey:
                rawmapdata = handle.read(1)
                # Convert rawmapdata to string 
                strmapdata = rawmapdata.encode("hex")

                #if index == 2:
                #    print strmapdata,

                # Calculate map data
                terraintype = strmapdata[1]
                terraincount = int(strmapdata[0], 16)+1
                # Keep track of coordinates in map 
                xcount += terraincount

                # Add to output_string
                for x in range(terraincount):
                    mapstring += terraintype

                # Find breakpoints 
                # A breakpoint can be identified by two bytes of the same terrain
                # and the the counting-part of the previous byte is not 16.
                # Also check that we are not on the edge of the map,
                # the encoding algorithm will place those breakpoints automatically
                if terraintype == prevterrain and prevcount != 16 and xcount-terraincount-1 >= 0: 
                    #sys.stdout.write("breakpoint! "+str(hex(prevcount-1)[2:])+str(prevterrain)+" "+str(hex(terraincount-1)[2:])+str(terraintype)+" "+str(xcount)+","+str(ycount)+"\n")
                    bp = [ xcount-terraincount, ycount ]
                    self.breakpoints[index].append(bp)
                prevterrain = terraintype
                prevcount = terraincount

                # If end of line, wrap around
                if xcount == 64:
                    xcount = 0
                    ycount += 1

            # Populate maparray with the decoded string
            y = 0+yoffset 
            x = 0
            for c in mapstring:
                self.maparray[x][y] = c
                x += 1
                if x == self.mapsizex:
                    y += 1
                    x = 0
                if y == self.mapsizey+yoffset:
                    break
            #print mapstring 

        # Read locations
        for i, _ in enumerate(self.maplocations):
            for j, _ in enumerate(self.maplocations[i]):
                handle.seek(int(self.maplocations[i][j][1], 16))
                self.maplocations[i][j][3] = int(handle.read(1).encode("hex"), 16)
                handle.seek(int(self.maplocations[i][j][2], 16))
                self.maplocations[i][j][4] = int(handle.read(1).encode("hex"), 16)

        # Special handling for hidden locations
        # Read Palace 6 y-value
        #handle.seek(int("8664", 16))
        #l = int(handle.read(1).encode("hex"), 16)
        #print "palace 6 y: ", l
        #if l == 0:
        #    self.palace6hidden.set(1)
        #else:
        #    self.palace6hidden.set(0)
           

        # Close file
        handle.close()

        # Default to West Hyrule
        self.changemap(0)

        # Enable editing
        self.editenabled = 1
        self.mapmenu.entryconfig("West Hyrule", state="normal")
        self.mapmenu.entryconfig("Death Mountain", state="normal")
        self.mapmenu.entryconfig("East Hyrule", state="normal")
        self.mapmenu.entryconfig("Maze Island", state="normal")
        self.filemenu.entryconfig("Save", state="normal")
        self.savebtn.config(state="normal")

        # Not edited
        self.edited = 0

    def saveromfile(self):
        currentactivemap = self.activemap

        # open file handle in write binary mode
        try:
            handle = open(self.filename, "r+b")
        except IOError:
            print "Cannot open file for saving"

        # Loop over the four startlocations in rom
        for index, maplocation in enumerate(self.mapstartlocations):
            self.activemap = index
            yoffset = index*self.mapsizey # Offset in maparray depending on which map

            # Convert maparray to encoded string and save to correct location in romfile
            mapstring = ""
            for y in range(self.mapsizey):
                for x in range(self.mapsizex):
                    mapstring += str(self.maparray[x][y+yoffset])

            encodedstring = self.mapencode(mapstring)
            handle.seek(maplocation)

            # Read two characters, convert to a byte, write to file
            i = 0
            while i+1 < len(encodedstring):
                byte = encodedstring[i]+encodedstring[i+1]
                byte = byte.decode("hex")
                handle.write(byte)
                i += 2

        # Save locations
        for i, _ in enumerate(self.maplocations):
            for j, _ in enumerate(self.maplocations[i]):
                # Convert integer value to hex-string without 0x, and pad with 0 if needed
                x = hex(self.maplocations[i][j][3])[2:].zfill(2)
                y = hex(self.maplocations[i][j][4])[2:].zfill(2)
                # Convert string to binary value
                x = x.decode("hex")
                y = y.decode("hex")
                # Find address in romfile and write value
                handle.seek(int(self.maplocations[i][j][1], 16))
                handle.write(x) 
                handle.seek(int(self.maplocations[i][j][2], 16))
                handle.write(y)
                
                # Save offset for palace locations
                if self.maplocations[i][j][7] != 0:
                    offset_in_array = (self.maplocations[i][j][4]-self.maplocations[i][j][6]-30)*64+self.maplocations[i][j][3]
                    
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
                            handle.seek(int(self.maplocations[i][j][7], 16))
                            handle.write(byte1)
                            handle.write(byte2)
                            break

        # Special handling for hidden locations
        # Write Palace 6 y-value
        if self.palace6hidden.get() == 0:
            y = hex(self.maplocations[2][41][4])[2:].zfill(2)
        else:
            y = "00"
        handle.seek(int("8664", 16))
        y = y.decode("hex")
        handle.write(y) 

        handle.close()
        self.edited = 0
        self.activemap = currentactivemap

    def changemap(self, mapnumber):
        self.activemap = mapnumber
        self.drawmap()

        # Update sizelabel
        mapsize = self.mapsizeinbytes()
        self.updatemapsizelabel(mapsize)
        
    def mapencode(self, input_string):
        ycount = 0
        xcount = 0 # Encoding must stop at 64 tiles per line of map
        tilecount = 1
        prev = ''
        output_string = ""
        for character in input_string:
            pos = [xcount,ycount]
            if character != prev:
                if prev:
                    output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
                prev = character
                if (xcount > 63):
                    xcount = 0
                    ycount += 1
            elif (tilecount == 16):
                output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
                if (xcount > 63):
                    xcount = 0
                    ycount += 1
            elif (xcount > 63):
                output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
                xcount = 0
                ycount += 1
            elif (pos in self.breakpoints[self.activemap]):
                output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
            else:
                tilecount += 1
            xcount += 1
    
        output_string += str(hex(tilecount-1)[2:])+character
        #print output_string
        return output_string

    def drawlocations(self):
        # loop over locations, print square around
        for l in self.maplocations[self.activemap]:
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
        self.drawbreakpoints()

    def drawtile(self, x, y):
        #print "drawtile"
        offset = self.activemap

        if self.maparray[x][y+(self.mapsizey*offset)] == "0":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_0)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "1":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_1)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "2":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_2)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "3":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_3)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "4":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_4)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "5":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_5)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "6":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_6)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "7":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_7)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "8":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_8)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "9":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_9)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "a":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_a)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "b":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_b)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "c":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_c)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "d":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_d)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "e":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_e)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "f":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_f)
        else:
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_error)

    def drawbreakpoints(self):
        #print "drawbreakpoints"
        for b in self.breakpoints[self.activemap]:
            #print "for b in self.breakpoints"
            x = b[0]
            y = b[1]
            self.canvas.create_line(((x-1)*16)+16, (y*16), ((x-1)*16)+16, (y*16)+16, fill="red", width=1)
            self.canvas.create_line(((x-1)*16)+13, (y*16), ((x-1)*16)+19, (y*16), fill="red", width=1)
            self.canvas.create_line(((x-1)*16)+13, (y*16)+15, ((x-1)*16)+19, (y*16)+15, fill="red", width=1)

    def quit(self):
        # Save before exit?
        if self.edited != 0:
            result = tkMessageBox.askyesnocancel("Zelda2MapEdit", "Save before exit?") 
            if result is True:
                self.saveromfile()
                self.master.destroy()
            elif result is False:
                self.master.destroy()
        else:
            self.master.destroy()

    def mousemove(self, event):
        #print "mousemove"
        if self.editenabled == 1:
            c = event.widget
            # Position on canvas
            x, y = c.canvasx(event.x), c.canvasy(event.y)
            # Calculate position on map
            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            offset = self.activemap

            # Make sure we are inside borders of the map
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0:
                # Y-axis seems to be offset with 30 on map compared to array
                #text = "(" + `x` + "," + `y+30` + ")"
                text = `self.maparray[x][y+(self.mapsizey*offset)]` + " (" + `x` + "," + `y+30` + ")"
                self.coordlabeltext.set(text)
   
                self.locationlabeltext.set("")
                for l in self.maplocations[self.activemap]:
                    if l[3]-l[5] == x and l[4]-l[6] == y+30:
                        text = l[0] + " (" + `l[3]-l[5]` + "," + `l[4]-l[6]` + ") (offset by: " + `l[5]` + "," + `l[6]` + ")"
                        self.locationlabeltext.set(text)
                        break

    def mapsizeinbytes(self):
        #print "mapsizeinbytes"
        yoffset = self.activemap*self.mapsizey
        # Generate mapstring
        mapstring = ""
        for y in range(self.mapsizey):
            for x in range(self.mapsizex):
                mapstring += str(self.maparray[x][y+yoffset])
        # Encode it
        encmapstring = self.mapencode(mapstring)

        # Return length/2 (BBF332 = 3 bytes)
        return len(encmapstring)/2

    def updatemapsizelabel(self,mapsize):
        #print "updatemapsizelabel"
        origmapsize = self.origmapsizes[self.activemap]

        text = `mapsize` + "/" + `origmapsize`
        self.mapsizelabeltext.set(text)

        # Change to red if larger then original mapsize
        if mapsize > origmapsize:
            self.mapsizelabel.config(fg="red")
        else:
            self.mapsizelabel.config(fg="black")

    def leftpress(self, event):
        #print "leftpress"
        yoffset = self.mapsizey*self.activemap

        if self.editenabled == 1:
            c = event.widget
            # Mouse down coordinates 
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            # Position in the map
            maparrayx = int(x)/16
            maparrayy = int(y)/16
            # Position to put breakpoint
            maparraybreakpointx = (abs(int(x)-8)/16)+1

            # Update maparray
            if self.selectedterrain == 'x':
                #Toggle breakpoint at location
                self.togglebreakpoint(maparraybreakpointx, maparrayy)
            elif self.selectedterrain == 'y':
                #
                #print "y"    
            else:
                # Update tile
                self.maparray[maparrayx][maparrayy+yoffset] = self.selectedterrain

            # Draw surrounding tiles, locations and breakpoints
            self.drawtile(maparrayx,maparrayy)
            self.drawtile(maparrayx-1,maparrayy)
            if maparrayx+1 < self.mapsizex: # Don't draw out of bounds
                self.drawtile(maparrayx+1,maparrayy)
            self.drawlocations()
            self.drawbreakpoints()

            # Edited
            self.edited = 1

    def leftmotion(self, event):
        #print "leftmotion"
        yoffset = self.mapsizey*self.activemap

        if self.editenabled == 1:
            c = event.widget
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            maparrayx = int(x)/16
            maparrayy = int(y)/16

            if self.selectedterrain != 'x':
                if self.maparray[maparrayx][maparrayy+yoffset] != self.selectedterrain:
                    self.maparray[maparrayx][maparrayy+yoffset] = self.selectedterrain
                    self.drawtile(maparrayx,maparrayy)
                    #self.drawlocations()
                    #self.drawbreakpoints()

    def leftrelease(self, event):
        #print "leftrelease"
        if self.editenabled == 1:
            # Calculate map size and update label
            mapsize = self.mapsizeinbytes()
            self.updatemapsizelabel(mapsize)
            self.drawlocations()
            self.drawbreakpoints()

    def rightpress(self, event):
        if self.editenabled == 1:
            c = event.widget
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0:
                # Find a location to move
                for p, l in enumerate(self.maplocations[self.activemap]):
                    if l[3]-l[5] == x and l[4]-l[6] == y+30:
                        self.movelocation = p
                        self.movelocationprevx = x
                        self.movelocationprevy = y
                        break

    def rightmotion(self, event):
        if self.editenabled == 1:
            c = event.widget
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map, and we found a location to move
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0 and self.movelocation >= 0:
                self.drawtile(self.movelocationprevx,self.movelocationprevy)
                self.canvas.create_rectangle((x*16), ((y)*16), (x*16+16)-1, ((y)*16+16)-1, outline="red", width=1)
                self.movelocationprevx = x
                self.movelocationprevy = y

    def rightrelease(self, event):
        if self.editenabled == 1:
            c = event.widget
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map, and we found a location to move
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0 and self.movelocation >= 0:
                self.maplocations[self.activemap][self.movelocation][3] = x+self.maplocations[self.activemap][self.movelocation][5]
                self.maplocations[self.activemap][self.movelocation][4] = y+30+self.maplocations[self.activemap][self.movelocation][6]

                self.movelocation = -1 
                self.drawmap()
                self.edited = 1

    def round_down(self, num, divisor):
        return num - (num%divisor)

    def togglebreakpoint(self, x, y):
        breakpoint = [x,y]
        #If breakpoint already exists at location, remove it. Otherwise add breakpoint
        if breakpoint in self.breakpoints[self.activemap]:
            self.breakpoints[self.activemap].remove(breakpoint) 
        else:
            self.breakpoints[self.activemap].append(breakpoint)

# End Class 

root = Tk()
app= Zelda2MapEdit(root)
root.mainloop()
