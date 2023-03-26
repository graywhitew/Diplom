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
        self.KoefSizeMon = 1
        if (self.width*self.height) < 1980*1080:
            self.KoefSizeMon = (self.width*self.height)/(1980*1080)*1.3
        print(self.width, self.height, self.KoefSizeMon)
        self.root.title("Хищник-жертва")
        self.style = ttk.Style()
        ttk.Style().theme_use('alt')
        # self.root.tk.call('lappend', 'auto_path', 'awthemes-10.4.0')
        # self.root.tk.call('package', 'require', 'awthemes')
        # self.root.tk.call('::themeutils::setHighlightColor', 'awdark', '#007000')
        # self.root.tk.call('package', 'require', 'awdark')
        # self.style.theme_use('awdark')

        self.Formula = ""

        self.frame_Choice = LabelFrame(text = "Выбор режима:", height=str(self.height*0.09), width=str(self.width*0.65), bd = 2)#height=str(self.height*0.09), width=str(self.width*0.65), bg="grey30", borderwidth=2, relief=RIDGE
        self.frame_Choice.grid(row=0, column=0, columnspan=4)
        self.frame_Choice.propagate(False)
        
        self.ParamsFrameHeight = str(self.height*0.72/7-10)
        self.ParamsFrameWidth = str(self.width*0.65 - 30)
        # self.ParamsFrameWidth = np.linspace(10, self.width/2, 4)

        self.frame_Parameters = LabelFrame(text = "Настройка параметров:", height=str(self.height*0.72), width=str(self.width*0.65), bd = 2)#height=str(self.height*0.09), width=str(self.width*0.65), bg="grey30", borderwidth=2, relief=RIDGE
        self.frame_Parameters.grid(row=1, column=0, columnspan=4, rowspan=8)
       
        self.frame_Graphics = LabelFrame(text = "Графики популяций", height=str(self.height*0.09+self.height*0.72), width=str(self.width*0.3), bd = 2)#height=str(self.height*0.09), width=str(self.width*0.65), bg="grey30", borderwidth=2, relief=RIDGE
        self.frame_Graphics.grid(row=0, column=4, rowspan = 8)
        self.frame_Graphics.propagate(False)
    
        self.frame_Formula = LabelFrame(text = "Формула", height=str(self.height*0.18), width=str(self.width*0.3), bd = 2)#height=str(self.height*0.09), width=str(self.width*0.65), bg="grey30", borderwidth=2, relief=RIDGE
        self.frame_Formula.grid(row=7, column=4)
        self.frame_Formula.propagate(False)

        self.label_Formula = Label(self.frame_Formula, text = self.Formula)
        self.label_Formula.pack(side=LEFT)
        

        self.current_value = tk.DoubleVar(value=1.2)

        self.DefaultValues = (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95)
        self.DefaultStartValues = (0,1,2,3,4,5,6,7,8,9,10)

        self.Go = ttk.Button(self.root, text="Моделирование", command=self.plot, width=20)
        self.Info = ttk.Button(self.root, text="Методичка", command=self.plot, width=20)
        self.OtherWindow = ttk.Button(self.root, text="В отдельном окне", command=self.NewWindow, width=20)
        self.DopKoef = ttk.Button(self.root, text="Дополнительные коэффициенты", command=self.Update, width=20)

        self.frame0 = Frame(self.root,height=self.ParamsFrameHeight, width=str(self.width*0.65), bd=2, relief=GROOVE)
        self.frame0.grid(row=1,column=0, columnspan=4)
        self.frame0.propagate(False)

        self.frame1 = Frame(self.root,height=self.ParamsFrameHeight, width=str(self.width*0.65), bd=2, relief=GROOVE)
        self.frame1.grid(row=2,column=0, columnspan=4)
        self.frame1.propagate(False)

        self.frame2 = Frame(self.root,height=self.ParamsFrameHeight, width=str(self.width*0.65), bd=2, relief=GROOVE)
        self.frame2.grid(row=3,column=0, columnspan=4)
        self.frame2.propagate(False)
 
        self.frame3 = Frame(self.root,height=self.ParamsFrameHeight, width=str(self.width*0.65), bd=2, relief=GROOVE)
        self.frame3.grid(row=4,column=0, columnspan=4)
        self.frame3.propagate(False)

        self.frame4 = Frame(self.root,height=self.ParamsFrameHeight, width=str(self.width*0.65), bd=2, relief=GROOVE)
        self.frame4.grid(row=5,column=0, columnspan=4)
        self.frame4.propagate(False)

        self.frame5 = Frame(self.root,height=self.ParamsFrameHeight, width=str(self.width*0.65), bd=2, relief=GROOVE)
        self.frame5.grid(row=6,column=0, columnspan=4)
        self.frame5.propagate(False)

        self.frame6 = Frame(self.root,height=self.ParamsFrameHeight, width=str(self.width*0.65),bd=2, relief=GROOVE)
        self.frame6.grid(row=7,column=0, columnspan=4)
        self.frame6.propagate(False)

        self.frame_Written = Frame(self.root,height=str(self.height*0.72/7-40), width=str(int(self.width*0.95)),bd=2, relief=GROOVE)
        self.frame_Written.grid(row=10,column=0, columnspan=5)
        self.frame_Written.propagate(False)
        self.label_Written = ttk.Label(self.frame_Written,text = "Written Sergey Scherstobitov Volgograd University 2023", font="Times 12")
        self.label_Written.pack(side=LEFT)

        self.Vers = tk.IntVar(value=0)
        self.Choise = tk.IntVar(value=0)

        self.checkbutton1 = ttk.Radiobutton(self.frame_Choice, text="Лисы-Кролики", value=0, variable=self.Vers)
        self.checkbutton1.pack(side=LEFT)

        self.checkbutton2 = ttk.Radiobutton(self.frame_Choice, text="Лисы-Кролики-Мыши", value=1, variable=self.Vers)
        self.checkbutton2.pack(side=LEFT)

        self.checkbutton3 = ttk.Radiobutton(self.frame_Choice, text="Лисы-Кролики-Мыши-Совы", value=2, variable=self.Vers)
        self.checkbutton3.pack(side=LEFT)

        
        self.CreateKoefSpinBox(0,'Количество растительности:',self.frame0, 1.2)
        self.CreateKoefSpinBox(1,'Значение коэф. \nрождаемости кроликов:',self.frame1, 0.2)
        self.CreateKoefSpinBox(2,'Значение коэф. \nсмертности кроликов:',self.frame1, 0.2)
        self.CreateKoefSpinBox(3,'Значение коэф. \nрождаемости лис:',self.frame2, 0.1)
        self.CreateKoefSpinBox(4,'Значение коэф. \nсмертности лис:',self.frame2, 0.07)
        self.CreateKoefSpinBox(9,'Коэф. \nантропогенного фактора:',self.frame3, 0.1)
        self.CreateKoefSpinBox(10,'Коэф. \nабиотического фактора:',self.frame3, 0.2)
        self.StartValueSpinBox('Начальные \nзначения популяций',self.frame4)

        self.Go.grid(row=9, column=0, sticky="ew")
        self.Info.grid(row=9, column=1, sticky="ew")
        self.DopKoef.grid(row=9, column=2, sticky="ew")
        self.OtherWindow.grid(row=9, column=3, sticky="ew")

        
        self.root.mainloop()
    
    def plot(self):
        self.G = float(globals()['spin_box%s' % 0].get())
        self.t0 = 0.0
        self.tmax = 350
        self.tspan = [self.t0, self.tmax]
        self.t = np.linspace(self.t0, self.tmax, 350)  # the points of evaluation of solution                   # initial value
        self.num = 350
        self.h = (self.tmax - self.t0) / self.num

        if self.Vers.get() == 0:
            
            self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) +\n+ B * sin(omega * t)) * R - kdb * R * F,\nПопуляция Лис: krf * R * F - kdf * F"""
            self.label_Formula.config(text=self.Formula)
           
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
            try:
                self.canvas5.get_tk_widget().pack_forget()
            except RecursionError:
                pass
            self.fig = Figure(figsize=(int(4), int(4)))
            a = self.fig.add_subplot(111)
            a.plot(self.t, self.x[:,0], label ="Кролики")
            a.plot(self.t, self.x[:,1], label ="Лисы")
            a.grid(alpha=.6, linestyle='--')
            a.legend(fontsize=12)

            self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.frame_Graphics)

            self.canvas5.get_tk_widget().pack(side = LEFT)
            self.canvas5.draw()
            # self.toolbar = NavigationToolbar2Tk(self.canvas5, self.root)
            # self.toolbar.update()
            

        if self.Vers.get() == 1:
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) +\n+ B * sin(omega * t)) * R - krd * R * F,\nПопуляция Лис: kfb * (R + M) * F - kfd * F
    \nПопуляция Мышей:kmb * (G + A * np.sin(omega * t) + B * np.sin(omega * t)) * M - self.kmd * F * M """
                self.label_Formula.config(text=self.Formula)

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
                try:
                    self.canvas5.get_tk_widget().pack_forget()
                except RecursionError:
                    pass
                self.fig = Figure(figsize=(int(4), int(4)))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x[:,0], label ="Кролики")
                a.plot(self.t, self.x[:,1], label ="Лисы")
                a.plot(self.t, self.x[:,2], label ="Мыши")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.root)
                self.canvas5.draw()
                self.canvas5.get_tk_widget().grid(row=1, column=4, sticky='NW', rowspan=9, padx=10)
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')
        if self.Vers.get() == 2:
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * (F + O),\nПопуляция Лис: kfb * (R + M) * F - kfd * F
\nПопуляция Мышей:kmb * (G + A * np.sin(omega * t) + B * np.sin(omega * t)) * M - self.kmd * F * M \nПопуляция Сов: kob * (R + M) * O - kod * O"""
                self.label_Formula.config(text=self.Formula)

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
                try:
                    self.canvas5.get_tk_widget().pack_forget()
                except RecursionError:
                    pass
                self.fig = Figure(figsize=(int(4), int(4)))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x[:,0], label ="Кролики")
                a.plot(self.t, self.x[:,1], label ="Лисы")
                a.plot(self.t, self.x[:,2], label ="Мыши")
                a.plot(self.t, self.x[:,3], label ="Совы")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.root)
                self.canvas5.get_tk_widget().grid(row=1, column=4, sticky='NW', rowspan=9, padx=10)
                self.canvas5.draw()
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')

    def Update(self):
        self.CreateKoefSpinBox(5,'Значение коэф.\n рождаемости мышей:',self.frame5)
        self.CreateKoefSpinBox(6,'Значение коэф.\n смертности мышей:',self.frame5)
        self.CreateKoefSpinBox(7,'Значение коэф.\n рождаемости сов:',self.frame6)
        self.CreateKoefSpinBox(8,'Значение коэф.\n смертности сов:',self.frame6)
        self.DopKoef.grid_forget()
        self.DopKoef2 = ttk.Button(self.root, text="Убрать доп. коэффициенты", command=self.UbrDopKoef)
        self.DopKoef2.grid(row=9, column=2, sticky="w")

    def UbrDopKoef(self):
        for widget in self.frame5.winfo_children():
            widget.destroy()
        for widget in self.frame6.winfo_children():
            widget.destroy()
        # for i in range(5,9):
        #     globals()['label_koef%s' % i].grid_forget()
        #     globals()['spin_box%s' % i].grid_forget()
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

    def CreateKoefSpinBox(self,number,text,frame,startvalue):
        globals()['label_koef%s' % number] = ttk.Label(frame, text=text, font = 'Times 12')
        globals()['label_koef%s' % number].pack(side=LEFT)
        globals()['current_value%s' % number] = tk.StringVar(value=startvalue)
        globals()['spin_box%s' % number] = ttk.Spinbox(
        frame,
        values=self.DefaultValues,
        font=('sans-serif', 14),
        textvariable=globals()['current_value%s' % number],
        width=5)
        globals()['spin_box%s' % number].pack(side=LEFT)
        # self.canvas2.create_text(xlabel,ylabel,text = text, fill = "white",anchor = NW, font = ("Times New Romance", int(14*self.KoefSizeMon)))
        # # self.canvas2.create_window(xlabel, ylabel, anchor= NW, window = globals()['label_koef%s' % number])
        # self.canvas2.create_window(xbox, ybox, window = globals()['spin_box%s' % number])
        # # 


    def StartValueSpinBox(self,text,frame):
        globals()['label_koef_start%s' % 1] = ttk.Label(frame, text=text, font = 'Times 12')
        globals()['label_koef_start%s' % 1].pack(side=LEFT)
        # globals()['label_koef_start%s' % 1].grid(row=rowlabel,
        #                                             column=columnlabel,
        #                                             sticky='w',
        #                                             padx=10)
        for i in range(4):
            globals()['current_value_start%s' % (i+1)] = tk.StringVar(value=i+2)
            globals()['spin_box_start%s' % (i+1)] = ttk.Spinbox(
            frame,
            values=self.DefaultStartValues,
            font=('sans-serif', 14),
            textvariable=globals()['current_value_start%s' % (i+1)],
            width=2)
            globals()['spin_box_start%s' % (i+1)].pack(side=LEFT)

            # self.canvas2.create_text(xlabel,ylabel,text = text, fill = "white",anchor = NW, font = ("Times New Romance", int(14*self.KoefSizeMon)))
            # # self.canvas2.create_window(xlabel, ylabel, anchor= NW, window = globals()['label_koef_start%s' % 1])
            # self.canvas2.create_window(xbox+i*45, ybox, window = globals()['spin_box_start%s' % (i+1)])
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
