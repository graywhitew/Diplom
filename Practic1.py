import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import font as tkFont
from PIL import Image, ImageTk
import matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import ttk
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
import tkinter.filedialog as fd
import sys
from tkinter import messagebox
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd

matplotlib.use('TkAgg')



class App(tk.Tk):
    def __init__(self):
        self.root = tk.Tk()

        self.width= self.root.winfo_screenwidth()
        self.height= self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (self.width, self.height))
        if (self.width*self.height) != 1980*1080:
            self.KoefSizeMon = (self.width*self.height)/(1980*1080)*1.3
        print(self.width, self.height, self.KoefSizeMon)
        self.root.title("Хищник-жертва")
        self.style = ttk.Style()
        self.root.tk.call('lappend', 'auto_path', '/home/graywhite/Загрузки/awthemes-10.4.0')
        self.root.tk.call('package', 'require', 'awthemes')
        self.root.tk.call('::themeutils::setHighlightColor', 'awdark', '#007000')
        self.root.tk.call('package', 'require', 'awdark')
        self.style.theme_use('awdark')

        self.Formula = ""

        self.canvas1 = tk.Canvas(self.root, height=str(self.height*0.09), width=str(self.width*0.65), bg="grey30", borderwidth=2, relief=RIDGE)
        self.canvas1.grid(row=0, column=0, columnspan=4)
        # self.canvas1.create_text(65,10,text = "Режимы работы:", fill = "white", font = int(14*self.KoefSizeMon))

        self.canvasHeight = np.linspace(30, self.height*0.65, 7)
        self.canvasWidth = np.linspace(10, self.width/2, 4)
        # print(self.canvasHeight, self.canvasWidth)

        self.canvas2 = tk.Canvas(self.root, height=str(self.height*0.72), width=str(self.width*0.65), bg="grey30")
        self.canvas2.grid(row=1, column=0, columnspan=4,rowspan=8)
        self.canvas2.create_text(110,10,text = "Настройка параметров:", fill = "white", font = ("Times New Romance", int(15*self.KoefSizeMon)))

        self.canvas3 = tk.Canvas(self.root, height=str(self.height*0.09), width=str(self.width*0.35), bg="grey30", borderwidth=2, relief=RIDGE)
        self.canvas3.grid(row=0, column=4)
        self.canvas3.create_text(100,10,text = "Графики популяций:", fill = "white", font = ("Times New Romance", int(15*self.KoefSizeMon)))
    
        self.canvas4 = tk.Canvas(self.root, height=str(self.height*0.54), width=str(self.width*0.35), bg="grey30")
        self.canvas4.grid(row=1, column=4, rowspan=6)

        self.canvas7 = tk.Canvas(self.root, height=str(self.height*0.18), width=str(self.width*0.35), bg="grey30", borderwidth=2, relief=RIDGE)
        self.canvas7.create_text(320,25,text = self.Formula, fill = "white", font = ("Times New Romance", int(10*self.KoefSizeMon)), tag = "formula")
        self.canvas7.grid(row=7, column=4)

        self.canvas6 = tk.Canvas(self.root, height=str(self.height*0.09), width=self.width, bg="grey30", borderwidth=2, relief=RIDGE)
        self.canvas6.create_text(165,10,text = "Written by Scherstobitov S.O. Russia. Volgograd. 2023", fill = "white", font = ("Times New Romance", int(12*self.KoefSizeMon)))
        self.canvas6.grid(row=10, column=0, columnspan=5)

        self.current_value = tk.DoubleVar(value=1.2)

        self.DefaultValues = (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95)
        self.DefaultStartValues = (0,1,2,3,4,5,6,7,8,9,10)

        # self.slider_label = ttk.Label(
        #     self.root,
        #     text='Начальное значение травы:', font = 14
        # )
        # self.slider_label.grid(
        #     column=0,
        #     row=2,
        #     sticky='w',
        #     padx=10
        # )
        # self.slider = ttk.Scale(
        #     self.root,
        #     from_=0,
        #     to=2,
        #     orient='horizontal',
        #     command=self.slider_changed,
        #     variable=self.current_value
        # )

        self.Vers = tk.IntVar(value=0)
        self.Choise = tk.IntVar(value=0)
        # self.helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
        self.checkbutton1 = ttk.Radiobutton(text="Лисы-Кролики", value=0, variable=self.Vers)
        self.checkbutton1.grid(row=0, column=0, sticky="w", padx=10)

        self.checkbutton2 = ttk.Radiobutton(text="Лисы-Кролики-Мыши", value=1, variable=self.Vers)
        self.checkbutton2.grid(row=0, column=1, sticky="w", padx=10)

        self.checkbutton3 = ttk.Radiobutton(text="Лисы-Кролики-Мыши-Совы", value=2, variable=self.Vers)
        self.checkbutton3.grid(row=0, column=2, sticky="w", padx=10)

        self.Go = ttk.Button(self.root, text="Моделирование", command=self.plot, width=20)
        self.Info = ttk.Button(self.root, text="Методичка", command=self.plot, width=20)
        self.OtherWindow = ttk.Button(self.root, text="В отдельном окне", command=self.NewWindow, width=20)
        self.DopKoef = ttk.Button(self.root, text="Дополнительные коэффициенты", command=self.Update, width=20)

        self.CreateKoefSpinBox(0,'Количество травы:',self.canvasWidth[0],self.canvasHeight[0],self.canvasWidth[1],self.canvasHeight[0]+10)
        self.CreateKoefSpinBox(1,'Значение коэф. \nрождаемости кроликов:',self.canvasWidth[0],self.canvasHeight[1],self.canvasWidth[1],self.canvasHeight[1]+10)
        self.CreateKoefSpinBox(2,'Значение коэф. \nсмертности кроликов:',self.canvasWidth[2],self.canvasHeight[1],self.canvasWidth[3],self.canvasHeight[1]+10)
        self.CreateKoefSpinBox(3,'Значение коэф. \nрождаемости лис:',self.canvasWidth[0],self.canvasHeight[2],self.canvasWidth[1],self.canvasHeight[2]+10)
        self.CreateKoefSpinBox(4,'Значение коэф. \nсмертности лис:',self.canvasWidth[2],self.canvasHeight[2],self.canvasWidth[3],self.canvasHeight[2]+10)
        self.CreateKoefSpinBox(9,'Коэф. \nантропогенного фактора:',self.canvasWidth[0],self.canvasHeight[3],self.canvasWidth[1],self.canvasHeight[3]+10)
        self.CreateKoefSpinBox(10,'Коэф. \nабиотического фактора:',self.canvasWidth[2],self.canvasHeight[3],self.canvasWidth[3],self.canvasHeight[3]+10)
        self.StartValueSpinBox('Начальные \nзначения популяций', self.canvasWidth[0],self.canvasHeight[4],self.canvasWidth[1],self.canvasHeight[4]+10)

        self.Go.grid(row=9, column=0, sticky="ew")
        self.Info.grid(row=9, column=1, sticky="ew")
        self.DopKoef.grid(row=9, column=2, sticky="ew")
        self.OtherWindow.grid(row=9, column=3, sticky="ew")

        # self.slider.grid(
        #              column=1,
        #              row=2,
        #              sticky='w')
        # self.current_value_label = ttk.Label(
        #     self.root,
        #     text='Значение:'
        # )
        # self.current_value_label.grid(
        #     row=2,
        #     column=2,
        #     sticky='w'
        # )
        # self.value_label = ttk.Label(
        #     self.root,
        #     text=self.get_current_value()
        # )

        # self.value_label.grid(
        #     row=2,
        #     column=3,
        #     sticky='w'
        # )
        # self.running = True
        # while self.running:
        #     if self.root.state()!= 'normal':
        #         self.root.destroy()
        #         sys.exit(0)
        # if self.root.state()!= 'normal':
        #     print("бибабоба")
        #     sys.exit(0)
            
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing())
        self.root.mainloop()
    # def on_closing(self):
    #     if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #         self.root.destroy()
    def plot(self):
        self.G = float(globals()['spin_box%s' % 0].get())
        self.t0 = 0.0
        self.tmax = 350
        self.tspan = [self.t0, self.tmax]
        # self.x0 = [1, 1, 6, 2]
        self.t = np.linspace(self.t0, self.tmax, 350)  # the points of evaluation of solution                   # initial value
        self.num = 350
        self.h = (self.tmax - self.t0) / self.num
        # решение методом Рунге-Кутты
        # self.x = np.zeros((len(self.t), len(self.x0)))  # array for solution
        # self.x[0, :] = self.x0

        if self.Vers.get() == 0:
            self.canvas7.delete("all")
            self.TextFormula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - kdb * R * F,\nПопуляция Лис: krf * R * F - kdf * F"""
            # self.Formula = """Популяция зайцев: Коэф. рождаемости кроликов * (Трава + Коэф.  * sin(omega * t) + Коэф. * sin(omega * t)) * 
            #                   Количество кроликов - Коэф. смертности кроликов * Количество кроликов * Количество лис,
            #                   Популяция Лис:Коэф. рождаемости лис * Количество кроликов * Количество лис - Коэф. смертности лис * Количество лис"""
            self.canvas7.create_text(400,35,text = self.TextFormula, fill = "white", font = ("Times New Romance", int(14*self.KoefSizeMon)), tag = 'folmula')
            self.krb = float(globals()['spin_box%s' % 1].get())
            self.krd = float(globals()['spin_box%s' % 2].get())
            self.kfb = float(globals()['spin_box%s' % 3].get())
            self.kfd = float(globals()['spin_box%s' % 4].get())
            self.a = float(globals()['spin_box%s' % 9].get())
            self.b = float(globals()['spin_box%s' % 10].get())

            self.x0 = [float(globals()['spin_box_start%s' % 1].get()), float(globals()['spin_box_start%s' % 2].get())]
            self.x = np.zeros((len(self.t), len(self.x0)))  # array for solution
            self.x[0, :] = self.x0
            self.i = 0
            while self.i < self.num - 1:
                self.k1 = self.h * self.Fone(self.t, self.x[self.i, :], self.i)

                self.k2 = self.h * self.Fone(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                self.k3 = self.h * self.Fone(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                self.k4 = self.h * self.Fone(self.t, self.x[self.i, :] + self.k3, self.i)

                self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                self.i = self.i + 1
            self.fig = Figure(figsize=(3, 3))
            a = self.fig.add_subplot(111)
            a.plot(self.t, self.x)
            plt.xlabel('t axis')
            plt.ylabel('x axis,Blue-Rabbits, Orange-Foxes')
            plt.grid(alpha=.6, linestyle='--')
            self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.root)
            self.canvas5.get_tk_widget().grid(row=1, column=4, sticky='NW', rowspan=9, padx=10)
            self.canvas5.draw()
            self.toolbar = NavigationToolbar2Tk(self.canvas5, self.root)
            self.toolbar.update()
            

        if self.Vers.get() == 1:
            try:
                self.canvas7.delete("all")
                self.TextFormula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * F,\nПопуляция Лис: kfb * (R + M) * F - kfd * F
\nПопуляция Мышей:kmb * (G + A * np.sin(omega * t) + B * np.sin(omega * t)) * M - self.kmd * F * M """
                self.canvas7.create_text(375,55,text = self.TextFormula, fill = "white", font = ("Times New Romance", int(13*self.KoefSizeMon)), tag = "formula")
                self.krb = float(globals()['spin_box%s' % 1].get())
                self.krd = float(globals()['spin_box%s' % 2].get())
                self.kfb = float(globals()['spin_box%s' % 3].get())
                self.kfd = float(globals()['spin_box%s' % 4].get())
                self.a = float(globals()['spin_box%s' % 9].get())
                self.b = float(globals()['spin_box%s' % 10].get())
                self.kmb = float(globals()['spin_box%s' % 5].get())
                self.kmd = float(globals()['spin_box%s' % 6].get())
                self.x0 = [float(globals()['spin_box_start%s' % 1].get()),
                            float(globals()['spin_box_start%s' % 2].get()),
                              float(globals()['spin_box_start%s' % 3].get())]
                self.x = np.zeros((len(self.t), len(self.x0)))  # array for solution
                self.x[0, :] = self.x0
                self.i = 0
                while self.i < self.num - 1:
                    self.k1 = self.h * self.Ftwo(self.t, self.x[self.i, :], self.i)

                    self.k2 = self.h * self.Ftwo(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                    self.k3 = self.h * self.Ftwo(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                    self.k4 = self.h * self.Ftwo(self.t, self.x[self.i, :] + self.k3, self.i)

                    self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                    self.i = self.i + 1
                self.fig = Figure(figsize=(6, 6))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x)
                plt.xlabel('t axis')
                plt.ylabel('x axis, Blue-Rabbits, Orange-Foxes, Green-Mice')
                plt.grid(alpha=.6, linestyle='--')

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.root)
                self.canvas5.get_tk_widget().grid(row=1, column=4, sticky='NW', rowspan=9, padx=10)
                self.canvas5.draw()
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')

        if self.Vers.get() == 2:
            try:
                self.canvas7.delete("all")
                self.TextFormula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * (F + O),\nПопуляция Лис: kfb * (R + M) * F - kfd * F
\nПопуляция Мышей:kmb * (G + A * np.sin(omega * t) + B * np.sin(omega * t)) * M - self.kmd * F * M \nПопуляция Сов: kob * (R + M) * O - kod * O"""
                self.canvas7.create_text(375,65,text = self.TextFormula, fill = "white", font = ("Times New Romance", int(13*self.KoefSizeMon)), tag = "formula")
                self.krb = float(globals()['spin_box%s' % 1].get())
                self.krd = float(globals()['spin_box%s' % 2].get())
                self.kfb = float(globals()['spin_box%s' % 3].get())
                self.kfd = float(globals()['spin_box%s' % 4].get())
                self.a = float(globals()['spin_box%s' % 9].get())
                self.b = float(globals()['spin_box%s' % 10].get())
                self.kmb = float(globals()['spin_box%s' % 5].get())
                self.kmd = float(globals()['spin_box%s' % 6].get())
                self.kob = float(globals()['spin_box%s' % 7].get())
                self.kod = float(globals()['spin_box%s' % 8].get())
                self.x0 = [float(globals()['spin_box_start%s' % 1].get()),
                            float(globals()['spin_box_start%s' % 2].get()),
                              float(globals()['spin_box_start%s' % 3].get()),
                               float(globals()['spin_box_start%s' % 4].get())]
                self.x = np.zeros((len(self.t), len(self.x0)))  # array for solution
                self.x[0, :] = self.x0
                self.i = 0
                while self.i < self.num - 1:
                    self.k1 = self.h * self.Fall(self.t, self.x[self.i, :], self.i)

                    self.k2 = self.h * self.Fall(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                    self.k3 = self.h * self.Fall(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                    self.k4 = self.h * self.Fall(self.t, self.x[self.i, :] + self.k3, self.i)

                    self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                    self.i = self.i + 1
                self.fig = Figure(figsize=(6, 6))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x)
                plt.xlabel('t axis')
                plt.ylabel('x axis, Blue-Rabbits, Orange-Foxes, Green-Mice, Red-Owls')
                plt.grid(alpha=.6, linestyle='--')

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.root)
                self.canvas5.get_tk_widget().grid(row=1, column=4, sticky='NW', rowspan=9, padx=10)
                self.canvas5.draw()
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')

    def Update(self):
        self.CreateKoefSpinBox(5,'Значение коэф. рождаемости мышей:',self.canvasWidth[0],self.canvasHeight[5],self.canvasWidth[1],self.canvasHeight[5])
        self.CreateKoefSpinBox(6,'Значение коэф. смертности мышей:',self.canvasWidth[2],self.canvasHeight[5],self.canvasWidth[3],self.canvasHeight[5])
        self.CreateKoefSpinBox(7,'Значение коэф. рождаемости сов:',self.canvasWidth[0],self.canvasHeight[6],self.canvasWidth[1],self.canvasHeight[6])
        self.CreateKoefSpinBox(8,'Значение коэф. смертности сов:',self.canvasWidth[2],self.canvasHeight[6],self.canvasWidth[3],self.canvasHeight[6])
        self.DopKoef.grid_forget()
        self.DopKoef2 = ttk.Button(self.root, text="Убрать доп. коэффициенты", command=self.UbrDopKoef)
        self.DopKoef2.grid(row=9, column=2, sticky="w")

    def UbrDopKoef(self):
        for i in range(5,9):
            globals()['label_koef%s' % i].grid_forget()
            globals()['spin_box%s' % i].grid_forget()
        self.DopKoef2.grid_forget()
        self.DopKoef = ttk.Button(self.root, text="Дополнительные коэффициенты", command=self.Update)
        self.DopKoef.grid(row=9, column=2, sticky="w")

    def NewWindow(self):
        self.G = float(globals()['spin_box%s' % 0].get())
        self.t0 = 0.0
        self.tmax = 350
        self.tspan = [self.t0, self.tmax]
        # self.x0 = [1, 1, 6, 2]
        self.t = np.linspace(self.t0, self.tmax, 350)  # the points of evaluation of solution                   # initial value
        self.num = 350
        self.h = (self.tmax - self.t0) / self.num
        # решение методом Рунге-Кутты
        # self.x = np.zeros((len(self.t), len(self.x0)))  # array for solution
        # self.x[0, :] = self.x0

        if self.Vers.get() == 0:

            self.krb = float(globals()['spin_box%s' % 1].get())
            self.krd = float(globals()['spin_box%s' % 2].get())
            self.kfb = float(globals()['spin_box%s' % 3].get())
            self.kfd = float(globals()['spin_box%s' % 4].get())
            self.a = float(globals()['spin_box%s' % 9].get())
            self.b = float(globals()['spin_box%s' % 10].get())

            self.x0 = [float(globals()['spin_box_start%s' % 1].get()),
                            float(globals()['spin_box_start%s' % 2].get())]
            self.x = np.zeros((len(self.t), len(self.x0)))  # array for solution
            self.x[0, :] = self.x0
            self.i = 0
            while self.i < self.num - 1:
                self.k1 = self.h * self.Fone(self.t, self.x[self.i, :], self.i)

                self.k2 = self.h * self.Fone(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                self.k3 = self.h * self.Fone(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                self.k4 = self.h * self.Fone(self.t, self.x[self.i, :] + self.k3, self.i)

                self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                self.i = self.i + 1
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 0]))
            fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 1]))
            self.num_steps = len(self.x[:, 0])
            fig = go.Figure(data=[go.Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='Кролики'),
                                go.Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='Лисы')])

            self.frames=[]
            for self.i in range(0, len(self.x[:, 0]), 5):
                self.frames.append(go.Frame(name=str(self.i),
                                    data=[go.Scatter(x=self.t[:self.i+1], y=self.x[:self.i+1,0], mode='lines', name='Кролики'),
                                            go.Scatter(x=self.t[:self.i+1], y=self.x[:self.i+1,1], mode='lines', name='Лисы')]))

            self.steps = []
            for self.i in range(self.num_steps):
                self.step = dict(
                    label=str(self.i),
                    method="animate",
                    args=[[str(self.i)]]
                )
                self.steps.append(self.step)

            self.sliders = [dict(
                steps=self.steps,
            )]

            fig.update_layout(xaxis_title="Ось X", yaxis_title="Ось Y",
                              updatemenus=[dict(direction="left",
                                                x=1,

                                                xanchor="center",
                                                y=1,
                                                showactive=False,
                                                type="buttons", 
                                                buttons=[dict(label="►", method="animate", args=[None, {"fromcurrent": True}]),
                                                        dict(label="❚❚", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False},
                                                                                                        "mode": "immediate",
                                                                                                        "transition": {"duration": 0}}])])])
            fig.layout.sliders = self.sliders
            fig.frames = self.frames  

            fig.show()
        if self.Vers.get() == 1:
            try:
                self.krb = float(globals()['spin_box%s' % 1].get())
                self.krd = float(globals()['spin_box%s' % 2].get())
                self.kfb = float(globals()['spin_box%s' % 3].get())
                self.kfd = float(globals()['spin_box%s' % 4].get())
                self.a = float(globals()['spin_box%s' % 9].get())
                self.b = float(globals()['spin_box%s' % 10].get())
                self.kmb = float(globals()['spin_box%s' % 5].get())
                self.kmd = float(globals()['spin_box%s' % 6].get())
                self.x0 = [float(globals()['spin_box_start%s' % 1].get()),
                            float(globals()['spin_box_start%s' % 2].get()),
                              float(globals()['spin_box_start%s' % 3].get())]
                self.x = np.zeros((len(self.t), len(self.x0)))  # array for solution
                self.x[0, :] = self.x0
                self.i = 0
                while self.i < self.num - 1:
                    self.k1 = self.h * self.Ftwo(self.t, self.x[self.i, :], self.i)

                    self.k2 = self.h * self.Ftwo(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                    self.k3 = self.h * self.Ftwo(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                    self.k4 = self.h * self.Ftwo(self.t, self.x[self.i, :] + self.k3, self.i)

                    self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                    self.i = self.i + 1
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 0]))
                fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 1]))
                fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 2]))

                self.num_steps = len(self.x[:, 0])
                fig = go.Figure(data=[go.Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='Кролики'),
                                      go.Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='Лисы'),
                                      go.Scatter(x=self.t, y=self.x[:, 2], mode='lines', name='Мыши')])

                self.frames = []
                for self.i in range(0, len(self.x[:, 0]), 4):
                    self.frames.append(go.Frame(name=str(self.i),
                                                data=[go.Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 0],
                                                                 mode='lines', name='Кролики'),
                                                      go.Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 1],
                                                                 mode='lines', name='Лисы'),
                                                      go.Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 2],
                                                                 mode='lines', name='Мыши')]))
                                                      

                self.steps = []
                for self.i in range(self.num_steps):
                    self.step = dict(
                        label=str(self.i),
                        method="animate",
                        args=[[str(self.i)]]
                    )
                    self.steps.append(self.step)

                self.sliders = [dict(
                    steps=self.steps,
                )]

                fig.update_layout(xaxis_title="Ось X", yaxis_title="Ось Y",updatemenus=[dict(direction="left",
                                                    x=1,
                                                    xanchor="center",
                                                    y=1,
                                                    showactive=False,
                                                    type="buttons",
                                                    buttons=[dict(label="►", method="animate",
                                                                  args=[None, {"fromcurrent": True}]),
                                                             dict(label="❚❚", method="animate", args=[[None], {
                                                                 "frame": {"duration": 0, "redraw": False},
                                                                 "mode": "immediate",
                                                                 "transition": {"duration": 0}}])])],
                                  )
                fig.layout.sliders = self.sliders
                fig.frames = self.frames

                fig.show()
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')
        if self.Vers.get() == 2:
            try: 
                self.krb = float(globals()['spin_box%s' % 1].get())
                self.krd = float(globals()['spin_box%s' % 2].get())
                self.kfb = float(globals()['spin_box%s' % 3].get())
                self.kfd = float(globals()['spin_box%s' % 4].get())
                self.a = float(globals()['spin_box%s' % 9].get())
                self.b = float(globals()['spin_box%s' % 10].get())
                self.kmb = float(globals()['spin_box%s' % 5].get())
                self.kmd = float(globals()['spin_box%s' % 6].get())
                self.kob = float(globals()['spin_box%s' % 7].get())
                self.kod = float(globals()['spin_box%s' % 8].get())
                self.x0 = [float(globals()['spin_box_start%s' % 1].get()),
                            float(globals()['spin_box_start%s' % 2].get()),
                              float(globals()['spin_box_start%s' % 3].get()),
                               float(globals()['spin_box_start%s' % 4].get())]
                self.x = np.zeros((len(self.t), len(self.x0)))  # array for solution
                self.x[0, :] = self.x0
                self.i = 0
                while self.i < self.num - 1:
                    self.k1 = self.h * self.Fall(self.t, self.x[self.i, :], self.i)

                    self.k2 = self.h * self.Fall(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                    self.k3 = self.h * self.Fall(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                    self.k4 = self.h * self.Fall(self.t, self.x[self.i, :] + self.k3, self.i)

                    self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                    self.i = self.i + 1
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 0]))
                fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 1]))
                fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 2]))
                fig.add_trace(go.Scatter(x=self.t, y=self.x[:, 3]))

                self.num_steps = len(self.x[:, 0])
                fig = go.Figure(data=[go.Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='Кролики'),
                                      go.Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='Лисы'),
                                      go.Scatter(x=self.t, y=self.x[:, 2], mode='lines', name='Мыши'),
                                      go.Scatter(x=self.t, y=self.x[:, 3], mode='lines', name='Совы')])

                self.frames = []
                for self.i in range(0, len(self.x[:, 0]), 5):
                    self.frames.append(go.Frame(name=str(self.i),
                                                data=[go.Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 0],
                                                                 mode='lines', name='Кролики'),
                                                      go.Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 1],
                                                                 mode='lines', name='Лисы'),
                                                      go.Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 2],
                                                                 mode='lines', name='Мыши'),
                                                      go.Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 3],
                                                                 mode='lines', name='Совы')]))

                self.steps = []
                for self.i in range(self.num_steps):
                    self.step = dict(
                        label=str(self.i),
                        method="animate",
                        args=[[str(self.i)]]
                    )
                    self.steps.append(self.step)

                self.sliders = [dict(
                    steps=self.steps,
                )]

                fig.update_layout(xaxis_title="Ось X", yaxis_title="Ось Y",updatemenus=[dict(direction="left",
                                                    x=1,
                                                    xanchor="center",
                                                    y=1,
                                                    showactive=False,
                                                    type="buttons",
                                                    buttons=[dict(label="►", method="animate",
                                                                  args=[None, {"fromcurrent": True}]),
                                                             dict(label="❚❚", method="animate", args=[[None], {
                                                                 "frame": {"duration": 0, "redraw": False},
                                                                 "mode": "immediate",
                                                                 "transition": {"duration": 0}}])])],
                                  )
                fig.layout.sliders = self.sliders
                fig.frames = self.frames

                fig.show()
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')

    def CreateKoefSpinBox(self,number,text,xlabel,ylabel,xbox,ybox):
        globals()['label_koef%s' % number] = ttk.Label(self.root, text=text, font = int(14*self.KoefSizeMon))
        # globals()['label_koef%s' % number].grid(row=rowlabel,
        #                                         column=columnlabel,
        #                                         sticky='w',
        #                                         padx=10)
        globals()['current_value%s' % number] = tk.StringVar(value=0.05)
        globals()['spin_box%s' % number] = ttk.Spinbox(
        values=self.DefaultValues,
        font=('sans-serif', int(12)),
        textvariable=globals()['current_value%s' % number],
        width=5)
        self.canvas2.create_text(xlabel,ylabel,text = text, fill = "white", font = ("Times New Romance", int(14*self.KoefSizeMon)))
        # self.canvas2.create_window(xlabel, ylabel, anchor= NW, window = globals()['label_koef%s' % number])
        self.canvas2.create_window(xbox, ybox, window = globals()['spin_box%s' % number])
        # globals()['spin_box%s' % number].grid(row=rowbox, column=columnbox, sticky="w", padx = 10)


    def StartValueSpinBox(self,text,xlabel,ylabel,xbox,ybox):
        globals()['label_koef_start%s' % 1] = ttk.Label(self.root, text=text, font = int(14*self.KoefSizeMon))
        # globals()['label_koef_start%s' % 1].grid(row=rowlabel,
        #                                             column=columnlabel,
        #                                             sticky='w',
        #                                             padx=10)
        for i in range(4):
            globals()['current_value_start%s' % (i+1)] = tk.StringVar(value=i+2)
            globals()['spin_box_start%s' % (i+1)] = ttk.Spinbox(
            values=self.DefaultStartValues,
            font=('sans-serif', int(12)),
            textvariable=globals()['current_value_start%s' % (i+1)],
            width=2)
            self.canvas2.create_text(xlabel,ylabel,text = text, fill = "white", font = ("Times New Romance", int(14*self.KoefSizeMon)))
            # self.canvas2.create_window(xlabel, ylabel, anchor= NW, window = globals()['label_koef_start%s' % 1])
            self.canvas2.create_window(xbox+i*45, ybox, window = globals()['spin_box_start%s' % (i+1)])
            # .grid(row=rowbox, column=columnbox, sticky="w", padx = i*45)

    # def slider_changed(self,event):
    #     self.value_label.configure(text=self.get_current_value())

    # def get_current_value(self):
    #     return '{: .2f}'.format(self.current_value.get())

    # def Plus(self,numb):
    #     return float(numb)+1

   
    def Fone(self, t, x, i):
        self.omega = 1.0
        return np.array([self.krb * (self.G + self.a * np.sin(self.omega * t[i]) + self.b * np.sin(self.omega * t[i])) * x[0] - self.krd * x[0] * x[1],
                         self.kfb * x[0] * x[1] - self.kfd * x[1]])  # start and end

    def Ftwo(self, t, x, i):
        self.a = 0.5
        self.omega = 1.0
        return np.array([self.krb * (self.G + self.a * np.sin(self.omega * t[i]) + self.b * np.sin(self.omega * t[i])) * x[0] - self.krd * x[1]  * x[0],
                         self.kfb * (x[0] + x[2]) * x[1] - self.kfd * x[1],
                         self.kmb * (self.G + self.a * np.sin(self.omega * t[i]) + self.b * np.sin(self.omega * t[i])) * x[2] - self.kmd * x[1]  * x[2]])


    def Fall(self, t, x, i):
        self.omega = 1.0
        return np.array([self.krb * (self.G + self.a * np.sin(self.omega * t[i]) + self.b * np.sin(self.omega * t[i])) * x[0] - self.krd * (x[1] + x[3]) * x[0],
                         self.kfb * (x[0] + x[2]) * x[1] - self.kfd * x[1],
                         self.kmb * (self.G + self.a * np.sin(self.omega * t[i]) + self.b * np.sin(self.omega * t[i])) * x[2] - self.kmd * (x[1] + x[3]) * x[2],
                         self.kob * (x[2] + x[0]) * x[3] - self.kod * x[3]])  # start and end


app = App()
