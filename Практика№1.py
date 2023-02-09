import math
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
import random
import ttkthemes
from PIL import Image, ImageTk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
import tkinter.filedialog as fd
import sys
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd

matplotlib.use('TkAgg')



class App(tk.Tk):
    def __init__(self):
        self.root = tk.Tk()
        self.root.tk.state('zoomed')
        self.root.title("Хищник-жертва")
        self.root.style = ttkthemes.ThemedStyle()
        self.root.tk.eval("""
set base_theme_dir /home/graywhite/Загрузки/awthemes-10.4.0

package ifneeded awthemes 10.4.0 \
    [list source [file join $base_theme_dir awthemes.tcl]]
package ifneeded colorutils 4.8 \
    [list source [file join $base_theme_dir colorutils.tcl]]
package ifneeded awdark 7.12 \
    [list source [file join $base_theme_dir awdark.tcl]]
package ifneeded awlight 7.6 \
    [list source [file join $base_theme_dir awlight.tcl]]
""")
# load the awdark and awlight themes
        self.root.tk.call("package", "require", 'awdark')
        self.root.tk.call("package", "require", 'awlight')
        self.root.style.theme_use('awdark')
        
        # создаем рабочую область
        self.canvas = tk.Canvas(self.root, height="100%", width='50%', bg="grey30", relief=tk.GROOVE, borderwidth=5)
        self.canvas.grid(row=0, column=0, columnspan=4, rowspan=9, sticky=W)
        self.current_value = tk.DoubleVar(value=1.2)
        self.DefaultValues = (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95)
        self.DefaultStartValues = (0,1,2,3,4,5,6,7,8,9,10)
        self.slider_label = ttk.Label(
            self.root,
            text='Начальное значение травы:'
        )
        self.slider_label.grid(
            column=0,
            row=2,
            sticky='w',
            padx=20
        )
        self.slider = ttk.Scale(
            self.root,
            from_=0,
            to=2,
            orient='horizontal',
            command=self.slider_changed,
            variable=self.current_value
        )

        self.Vers = tk.IntVar(value=0)
        self.Choise = tk.IntVar(value=0)

        self.checkbutton = ttk.Radiobutton(text="Лисы-Кролики", value=0, variable=self.Vers)
        self.checkbutton.grid(row=0, column=0, sticky=tk.W)

        self.checkbutton = ttk.Radiobutton(text="Лисы-Кролики-Мыши", value=1, variable=self.Vers)
        self.checkbutton.grid(row=0, column=1, sticky=tk.W)

        self.checkbutton = ttk.Radiobutton(text="Лисы-Кролики-Мыши-Совы", value=2, variable=self.Vers)
        self.checkbutton.grid(row=0, column=2, sticky=tk.W)

        self.Go = ttk.Button(self.root, text="Моделирование", command=self.plot)
        self.OtherWindow = ttk.Button(self.root, text="В отдельном окне", command=self.NewWindow)
        self.DopKoef = ttk.Button(self.root, text="Дополнительные коэффициенты", command=self.Update)

        self.CreateKoefSpinBox(1,'Значение коэф. рождаемости кроликов:',3,0,3,1)
        self.CreateKoefSpinBox(2,'Значение коэф. смертности кроликов:',3,2,3,3)
        self.CreateKoefSpinBox(3,'Значение коэф. рождаемости лис:',4,0,4,1)
        self.CreateKoefSpinBox(4,'Значение коэф. смертности лис:',4,2,4,3)
        self.CreateKoefSpinBox(9,'Коэф. антропогенного фактора:',5,0,5,1)
        self.CreateKoefSpinBox(10,'Коэф. абиотического фактора:', 5,2,5,3)
        self.StartValueSpinBox('Начальные значения попудяций', 6,0,6,1)

        self.Go.grid(row=9, column=0,sticky="w",padx=0)
        self.OtherWindow.grid(row=9, column=3,sticky="w")
        self.DopKoef.grid(row=9, column=2, sticky="w")
        self.slider.grid(
                     column=1,
                     row=2,
                     sticky='w')
        self.current_value_label = ttk.Label(
            self.root,
            text='Значение:'
        )
        self.current_value_label.grid(
            row=2,
            column=2,
            sticky='w'
        )
        self.value_label = ttk.Label(
            self.root,
            text=self.get_current_value()
        )

        self.value_label.grid(
            row=2,
            column=3,
            sticky='w'
        )

        self.root.mainloop()



    def Update(self):
        self.CreateKoefSpinBox(5,'Значение коэф. рождаемости мышей:',7,0,7,1)
        self.CreateKoefSpinBox(6,'Значение коэф. смертности мышей:',7,2,7,3)
        self.CreateKoefSpinBox(7,'Значение коэф. рождаемости сов:',8,0,8,1)
        self.CreateKoefSpinBox(8,'Значение коэф. смертности сов:',8,2,8,3)
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
        self.G = self.current_value.get()

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

    def CreateKoefSpinBox(self,number,text,rowlabel,columnlabel,rowbox,columnbox):
        globals()['label_koef%s' % number] = ttk.Label(self.root, text=text)
        globals()['label_koef%s' % number].grid(row=rowlabel,
                                                column=columnlabel,
                                                sticky='w',
                                                padx=0)
        globals()['current_value%s' % number] = tk.StringVar(value=0.05)
        globals()['spin_box%s' % number] = ttk.Spinbox(
        values=self.DefaultValues,
        font=('sans-serif', 12),
        textvariable=globals()['current_value%s' % number],
        width=5)
        globals()['spin_box%s' % number].grid(row=rowbox, column=columnbox, sticky="w")


    def StartValueSpinBox(self,text,rowlabel,columnlabel,rowbox,columnbox):
        globals()['label_koef_start%s' % 1] = ttk.Label(self.root, text=text)
        globals()['label_koef_start%s' % 1].grid(row=rowlabel,
                                                    column=columnlabel,
                                                    sticky='w',
                                                    padx=0)
        for i in range(4):
            globals()['current_value_start%s' % (i+1)] = tk.StringVar(value=i+2)
            globals()['spin_box_start%s' % (i+1)] = ttk.Spinbox(
            values=self.DefaultStartValues,
            font=('sans-serif', 12),
            textvariable=globals()['current_value_start%s' % (i+1)],
            width=5)
            globals()['spin_box_start%s' % (i+1)].grid(row=rowbox, column=columnbox, sticky="w", padx = i*100)

    def slider_changed(self,event):
        self.value_label.configure(text=self.get_current_value())

    def get_current_value(self):
        return '{: .2f}'.format(self.current_value.get())

    def Plus(self,numb):
        return float(numb)+1

    def plot(self):
        self.G = self.current_value.get()

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
            self.fig = Figure(figsize=(6, 6))
            a = self.fig.add_subplot(111)
            a.plot(self.t, self.x)
            plt.xlabel('t axis')
            plt.ylabel('x axis,Blue-Rabbits, Orange-Foxes')
            plt.grid(alpha=.6, linestyle='--')
            self.canvas1 = FigureCanvasTkAgg(self.fig, master = self.root)
            self.canvas1.get_tk_widget().grid(row=0, column=4, sticky='N', rowspan=9)
            self.canvas1.draw()

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
                self.fig = Figure(figsize=(6, 6))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x)
                plt.xlabel('t axis')
                plt.ylabel('x axis, Blue-Rabbits, Orange-Foxes, Green-Mice')
                plt.grid(alpha=.6, linestyle='--')

                self.canvas1 = FigureCanvasTkAgg(self.fig, master=self.root)
                self.canvas1.get_tk_widget().grid(row=0, column=4, sticky='N', rowspan=9)
                self.canvas1.draw()
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
                self.fig = Figure(figsize=(6, 6))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x)
                plt.xlabel('t axis')
                plt.ylabel('x axis, Blue-Rabbits, Orange-Foxes, Green-Mice, Red-Owls')
                plt.grid(alpha=.6, linestyle='--')

                self.canvas1 = FigureCanvasTkAgg(self.fig, master=self.root)
                self.canvas1.get_tk_widget().grid(row=0, column=4, sticky='N', rowspan=9)
                self.canvas1.draw()
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')
    def Fone(self, t, x, i):
        self.omega = 1.0
        return np.array([self.krb * (self.G + self.a * np.sin(self.omega * t[i]) + self.b * np.sin(self.omega * t[i])) *
                         x[0] - self.krd * x[0] * x[1],
                         self.kfb * x[0] * x[1] - self.kfd * x[1]])  # start and end

    def Ftwo(self, t, x, i):
        self.a = 0.5
        self.omega = 1.0
        return np.array([self.krb * (self.G + self.a * np.sin(self.omega * t[i])) * x[0] - self.krd * x[0] * x[1],
                         self.kfb * (x[0] + x[2]) * x[1] - self.kfd * x[1],
                         self.kmb * (self.G + self.a * np.sin(self.omega * t[i])) * x[2] - self.kmd * (x[1] + x[3]) * x[2],
                         self.kob * x[2] * x[3] - self.kod * x[3]])  # start and end

    def Fall(self, t, x, i):
        self.omega = 1.0
        return np.array([self.krb * (self.G + self.a * np.sin(self.omega * t[i]) + self.b * np.sin(self.omega * t[i])) * x[0] - self.krd * (x[1] + x[3]) * x[0],
                         self.kfb * (x[0] + x[2]) * x[1] - self.kfd * x[1],
                         self.kmb * (self.G + self.a * np.sin(self.omega * t[i]) + self.b * np.sin(self.omega * t[i])) * x[2] - self.kmd * (x[1] + x[3]) * x[2],
                         self.kob * (x[2] + x[0]) * x[3] - self.kod * x[3]])  # start and end


app = App()
