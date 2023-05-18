import plotly.graph_objs as go
import tkinter as tk
import customtkinter
from numpy import linspace, zeros, array, sin
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk, LEFT, YES, GROOVE, TOP, BOTH
from ttkthemes import ThemedTk
from plotly.subplots import make_subplots
from collections.abc import Callable
from typing import Union
from time import sleep

customtkinter.set_appearance_mode("light") 
# customtkinter.set_default_color_theme ("dark") 
class Main(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Учебный модуль")
        self.width= self.winfo_screenwidth()/2
        self.height= self.winfo_screenheight()/2
        self.geometry("%dx%d" % (self.width, self.height))
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)

        # customtkinter.set_default_color_theme("light")
        

        self.MainFrame = MyMainFrame(self)
        self.MainFrame.grid(row=0, column=0, padx=10, pady=(10, 0))
    

class MyMainFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1), weight=1)
        self.toplevel_window = None
        self.title = customtkinter.CTkLabel(self, text="Электронный учебный модуль по предмету 'Биофизика'", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.button = customtkinter.CTkButton(self, text="Модифицированная модель хищник-жертва", command=self.open_toplevel, width=50, height=50, font=("Times", 20))
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(self, text="Модифицированная модель хищник-жертва", command=Lab2, width=50, height=50, font=("Times", 20))
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Lab1(self)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

class Lab1(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.width= self.winfo_screenwidth()-100
        self.height= self.winfo_screenheight()/2
        self.geometry("%dx%d" % (self.width, self.height))
        self.title("Хищник-жертва")
        

        self.Formula = ""

        self.operating_mode_frame = RadiobuttonFrame(self, "Выбор режима", values=["Лисы-Кролики", "Лисы-Кролики-Мыши","Лисы-Кролики-Мыши-Совы"])
        self.operating_mode_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="ew")

        self.Lab1ParamFrame = Lab1_Param_Frame(self)
        self.Lab1ParamFrame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")

        self.Lab1ButtonFrame = Lab1_Button_Frame(self)
        self.Lab1ButtonFrame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.Lab1GraphFrame = Lab1_Graph_Frame(self)
        self.Lab1GraphFrame.grid(row=0, rowspan = 2, column=6, padx=10, pady=(10, 0), sticky="w")

        self.Lab1FormulaFrame = Lab1_Formula_Frame(self)
        self.Lab1FormulaFrame.grid(row=2, column=6, padx=10, pady=(10, 0), sticky="n")
        
        # self.Lab1WrittenBy = Lab1_WrittenBy_Frame(self)
        # self.Lab1WrittenBy.grid(row=3, column=0, columnspan = 2, padx=10, pady=(10, 0), sticky="w")

    def Lab1_plot(self):
        self.G = self.Lab1ParamFrame.spinbox_0.get()
        self.t0 = 0.0
        self.tmax = 500
        self.num = 4000
        self.tspan = [self.t0, self.tmax]
        self.t = linspace(self.t0, self.tmax, self.num)  # the points of evaluation of solution                   # initial value
        
        self.h = (self.tmax - self.t0) / self.num

        if self.operating_mode_frame.get() == "Лисы-Кролики":
            self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (G + A * sin(w * t) + B * sin(w * t)) * R - kdb * R * F\nПопуляция Лис: krf * R * F - kdf * F"""
            self.Lab1FormulaFrame.title.configure(text=self.Formula)
        
            self.krb = self.Lab1ParamFrame.spinbox_1.get()
            self.krd = self.Lab1ParamFrame.spinbox_2.get()
            self.kfb = self.Lab1ParamFrame.spinbox_3.get()
            self.kfd = self.Lab1ParamFrame.spinbox_4.get()
            self.a = self.Lab1ParamFrame.spinbox_13.get()
            self.b = self.Lab1ParamFrame.spinbox_14.get()

            self.x0 = [self.Lab1ParamFrame.spinbox_9.get(), self.Lab1ParamFrame.spinbox_10.get()]
            self.x = zeros((len(self.t), len(self.x0)))  # array for solution
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
            except AttributeError:
                pass
            self.fig = Figure(figsize=(4, 4))
            a = self.fig.add_subplot(111)
            a.plot(self.t, self.x[:,0], label ="Кролики")
            a.plot(self.t, self.x[:,1], label ="Лисы")
            a.grid(alpha=.6, linestyle='--')
            a.legend(fontsize=12)

            self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab1GraphFrame)
            self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
            self.canvas5.draw()
            # self.toolbar = NavigationToolbar2TkAgg(self.canvas5, self.frame_Graphics)
            # self.toolbar.update()
        elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши":
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * F\nПопуляция Лис: kfb * (R + M) * F - kfd * F\nПопуляция Мышей:kmb * (G + A * sin(omega * t) + B * sin(omega * t)) * M - self.kmd * F * M """
                # self.label_Formula.config(text=self.Formula)

                self.krb = float(globals()['Lab1_spin_box%s' % 1].get())
                self.krd = float(globals()['Lab1_spin_box%s' % 2].get())
                self.kfb = float(globals()['Lab1_spin_box%s' % 3].get())
                self.kfd = float(globals()['Lab1_spin_box%s' % 4].get())
                self.a = float(globals()['Lab1_spin_box%s' % 9].get())
                self.b = float(globals()['Lab1_spin_box%s' % 10].get())
                self.kmb = float(globals()['Lab1_spin_box%s' % 5].get())
                self.kmd = float(globals()['Lab1_spin_box%s' % 6].get())
                self.x0 = [float(globals()['Lab1_spin_box_start%s' % 1].get()),
                            float(globals()['Lab1_spin_box_start%s' % 2].get()),
                                float(globals()['Lab1_spin_box_start%s' % 3].get())]
                self.x = zeros((len(self.t), len(self.x0)))  # array for solution
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
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x[:,0], label ="Кролики")
                a.plot(self.t, self.x[:,1], label ="Лисы")
                a.plot(self.t, self.x[:,2], label ="Мыши")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.frame_Graphics)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши-Совы":
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * (F + O)\nПопуляция Лис: kfb * (R + M) * F - kfd * F\nПопуляция Мышей:kmb * (G + A * sin(omega * t) + B * sin(omega * t)) * M - self.kmd * F * M \nПопуляция Сов: kob * (R + M) * O - kod * O"""
                self.label_Formula.config(text=self.Formula)

                self.krb = float(globals()['Lab1_spin_box%s' % 1].get())
                self.krd = float(globals()['Lab1_spin_box%s' % 2].get())
                self.kfb = float(globals()['Lab1_spin_box%s' % 3].get())
                self.kfd = float(globals()['Lab1_spin_box%s' % 4].get())
                self.a = float(globals()['Lab1_spin_box%s' % 9].get())
                self.b = float(globals()['Lab1_spin_box%s' % 10].get())
                self.kmb = float(globals()['Lab1_spin_box%s' % 5].get())
                self.kmd = float(globals()['Lab1_spin_box%s' % 6].get())
                self.kob = float(globals()['Lab1_spin_box%s' % 7].get())
                self.kod = float(globals()['Lab1_spin_box%s' % 8].get())
                self.x0 = [float(globals()['Lab1_spin_box_start%s' % 1].get()),
                            float(globals()['Lab1_spin_box_start%s' % 2].get()),
                              float(globals()['Lab1_spin_box_start%s' % 3].get()),
                               float(globals()['Lab1_spin_box_start%s' % 4].get())]
                self.x = zeros((len(self.t), len(self.x0)))  # array for solution
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
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x[:,0], label ="Кролики")
                a.plot(self.t, self.x[:,1], label ="Лисы")
                a.plot(self.t, self.x[:,2], label ="Мыши")
                a.plot(self.t, self.x[:,3], label ="Совы")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.frame_Graphics)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                tk.messagebox.showerror(title=None, message='Введите коэффициенты')
    def Fone(self, t, x, i):
        self.omega = 1.0
        return array([self.krb * (self.G + self.a * sin(self.omega * t[i]) + self.b * sin(self.omega * t[i])) * x[0] - self.krd * x[0] * x[1],
                         self.kfb * x[0] * x[1] - self.kfd * x[1]])  # start and end

    def Ftwo(self, t, x, i):
        self.a = 0.5
        self.omega = 1.0
        return array([self.krb * (self.G + self.a * sin(self.omega * t[i]) + self.b * sin(self.omega * t[i])) * x[0] - self.krd * x[1]  * x[0],
                         self.kfb * (x[0] + x[2]) * x[1] - self.kfd * x[1],
                         self.kmb * (self.G + self.a * sin(self.omega * t[i]) + self.b * sin(self.omega * t[i])) * x[2] - self.kmd * x[1]  * x[2]])


    def Fall(self, t, x, i):
        self.omega = 1.0
        return array([self.krb * (self.G + self.a * sin(self.omega * t[i]) + self.b * sin(self.omega * t[i])) * x[0] - self.krd * (x[1] + x[3]) * x[0],
                         self.kfb * (x[0] + x[2]) * x[1] - self.kfd * x[1],
                         self.kmb * (self.G + self.a * sin(self.omega * t[i]) + self.b * sin(self.omega * t[i])) * x[2] - self.kmd * (x[1] + x[3]) * x[2],
                         self.kob * (x[2] + x[0]) * x[3] - self.kod * x[3]])  # start and end
        

class Lab1_Graph_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class Lab1_Formula_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.title = customtkinter.CTkLabel(self, text="", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

class Lab1_WrittenBy_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class Lab1_Param_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = customtkinter.CTkLabel(self, text="Количество растительности:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.spinbox_0 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 1.2)
        self.spinbox_0.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

        self.title = customtkinter.CTkLabel(self, text="Значение коэф. \nрождаемости кроликов:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.spinbox_1 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0.2)
        self.spinbox_1.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Значение коэф. \nсмертности кроликов:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=1, column=2, padx=10, pady=(10, 0))
        self.spinbox_2 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0.2)
        self.spinbox_2.grid(row=1, column=3, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Нач. значения\n популяции", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=1, column=4, padx=10, pady=(10, 0))
        self.spinbox_9 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 1)
        self.spinbox_9.grid(row=1, column=5, padx=(0, 10), pady=(10, 10))

        self.title = customtkinter.CTkLabel(self, text="Значение коэф. \nрождаемости лис:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.spinbox_3 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0.2)
        self.spinbox_3.grid(row=2, column=1, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Значение коэф. \nсмертности лис:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=2, column=2, padx=10, pady=(10, 0))
        self.spinbox_4 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0.2)
        self.spinbox_4.grid(row=2, column=3, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Нач. значения\n популяции", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=2, column=4, padx=10, pady=(10, 0))
        self.spinbox_10 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 2)
        self.spinbox_10.grid(row=2, column=5, padx=(0, 10), pady=(10, 10))

        self.title = customtkinter.CTkLabel(self, text="Значение коэф. \nрождаемости мыш:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=3, column=0, padx=10, pady=(10, 0))
        self.spinbox_5 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0.2)
        self.spinbox_5.grid(row=3, column=1, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Значение коэф. \nсмертности мыш:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=3, column=2, padx=10, pady=(10, 0))
        self.spinbox_6 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0.2)
        self.spinbox_6.grid(row=3, column=3, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Нач. значения\n популяции", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=3, column=4, padx=10, pady=(10, 0))
        self.spinbox_11 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 3)
        self.spinbox_11.grid(row=3, column=5, padx=(0, 10), pady=(10, 10))

        self.title = customtkinter.CTkLabel(self, text="Значение коэф. \nрождаемости сов:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=4, column=0, padx=10, pady=(10, 0))
        self.spinbox_7 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0.2)
        self.spinbox_7.grid(row=4, column=1, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Значение коэф. \nсмертности сов:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=4, column=2, padx=10, pady=(10, 0))
        self.spinbox_8 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0.2)
        self.spinbox_8.grid(row=4, column=3, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Нач. значения\n популяции", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=4, column=4, padx=10, pady=(10, 0))
        self.spinbox_12 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 4)
        self.spinbox_12.grid(row=4, column=5, padx=(0, 10), pady=(10, 10))

        self.title = customtkinter.CTkLabel(self, text="Коэф. антропогенного фактора:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.spinbox_13 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0)
        self.spinbox_13.grid(row=5, column=1, padx=(0, 10), pady=(10, 10))
        self.title = customtkinter.CTkLabel(self, text="Коэф. биотического фактора:", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=5, column=2, padx=10, pady=(10, 0))
        self.spinbox_14 = FloatSpinbox(self, width=150, step_size=0.1, def_value = 0)
        self.spinbox_14.grid(row=5, column=3, padx=(0, 10), pady=(10, 10))
        self.spin_date = []
    def update_spinbox_date(self):
        self.spin_date = [self.spinbox_1.get(),self.spinbox_2.get(),self.spinbox_3.get(),self.spinbox_4.get(),self.spinbox_5.get(),self.spinbox_6.get(),self.spinbox_7.get(),self.spinbox_8.get(),self.spinbox_9.get(),self.spinbox_10.get(),
                          self.spinbox_11.get(),self.spinbox_12.get(),self.spinbox_13.get(),self.spinbox_14.get()]
        return self.spin_date
        

    
class Lab1_Button_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.button = customtkinter.CTkButton(self, text="Графики популяций", command=master.Lab1_plot, width=50, height=50, font=("Times", 20))
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(self, text="Фазовый портрет", command=Lab2, width=50, height=50, font=("Times", 20))
        self.button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(self, text="Методичка", command=Lab2, width=50, height=50, font=("Times", 20))
        self.button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(self, text="В отдельном окне", command=Lab2, width=50, height=50, font=("Times", 20))
        self.button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
    


    
    
class WidgetName(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 def_value: int = 0,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.def_value = def_value
        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, str(float(def_value)))

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        if float(self.entry.get()) > 0:
            try:
                value = float(self.entry.get()) - self.step_size
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            except ValueError:
                return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

class RadiobuttonFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="azure", corner_radius=6)
        self.title.grid(row=0, column=0,columnspan=3, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=1, column=i, padx=10, pady=(10, 0))
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

class Lab2(customtkinter.CTkToplevel):
    def __init__(self, master):
        pass

app = Main()
app.mainloop()

# Mainlabel_Written_main = ttk.Label(Main,text = "Электронный учебный модуль по предмету 'Биофизика'", font="Times 20")
# Mainlabel_Written_main.pack(side=LEFT, expand=YES)

# Mainframe1 = ttk.Frame(Main,height=height*0.3, width=width)
# Mainframe1.grid(row=2,column=0, columnspan=2)
# Mainframe1.propagate(False)

# MainLabaratory1 = tk.Button(Mainframe1, text="Модифицированная модель хищник-жертва", command=Lab1, width=50, height=50)
# MainLabaratory2 = tk.Button(Mainframe1, text="Проточные и непроточные микроорганизмы", command=Lab2, width=50, height=50)
# MainLabaratory1.pack(side=LEFT, expand=YES)
# MainLabaratory2.pack(side=LEFT, expand=YES)

# Mainframe_Written = ttk.Frame(Main,height=height*0.1, width=width, relief=GROOVE)
# Mainframe_Written.grid(row=3,column=0, columnspan=5)
# Mainframe_Written.propagate(False)

# Mainlabel_Written_by = ttk.Label(Mainframe_Written,text = "Written Sergey Scherstobitov Volgograd University 2023", font="Times 12")
# Mainlabel_Written_by.pack(side=LEFT, padx = 20)

# Main.mainloop()
