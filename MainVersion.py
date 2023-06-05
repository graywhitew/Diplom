from plotly.graph_objs import Scatter, Frame

from customtkinter import CTk, CTkFrame, CTkToplevel, CTkLabel, CTkButton,set_appearance_mode, StringVar, CTkRadioButton, CTkEntry, CTkOptionMenu, set_widget_scaling
from numpy import linspace, zeros, array, sin
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import LEFT, YES, TOP, BOTH, Menu, messagebox
# from ttkthemes import ThemedTk
from plotly.subplots import make_subplots
from collections.abc import Callable
from typing import Union
import webbrowser
from os import getcwd


set_appearance_mode("light") 
# set_default_color_theme ("dark") 

class Main(CTk):
    def __init__(self):
        super().__init__()
        self.title("Учебный модуль")
        self.width= self.winfo_screenwidth()/2
        self.height= self.winfo_screenheight()/2
        self.geometry("%dx%d" % (self.width, self.height))
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)

        # set_default_color_theme("light")
        

        self.MainFrame = MyMainFrame(self)
        self.MainFrame.grid(row=0, column=0, padx=10, pady=(10, 0))
    
class MyMainFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1), weight=1)
        self.toplevel_window_Lab1 = None
        self.toplevel_window_Lab2 = None
        self.title = CTkLabel(self, text="Электронный учебный модуль по предмету 'Биофизика'", fg_color="azure", corner_radius=6, font=("Times", 20))
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.button = CTkButton(self, text="Модифицированная модель хищник-жертва", command=self.open_toplevel_Lab1, width=50, height=50, font=("Times", 20))
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.button = CTkButton(self, text="Проточное и непроточное\n моделирование микроорганизмов", command=self.open_toplevel_Lab2, width=50, height=50, font=("Times", 20))
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
    def open_toplevel_Lab1(self):
        if self.toplevel_window_Lab1 is None or not self.toplevel_window_Lab1.winfo_exists():
            self.toplevel_window_Lab1 = Lab1(self)
            self.toplevel_window_Lab1.focus()
        else:
            self.toplevel_window_Lab1.focus()
    def open_toplevel_Lab2(self):
        if self.toplevel_window_Lab2 is None or not self.toplevel_window_Lab2.winfo_exists():
            self.toplevel_window_Lab2 = Lab2(self)
            self.toplevel_window_Lab2.focus()
        else:
            self.toplevel_window_Lab2.focus()
        # self.toplevel_window_Lab1.focus()

class Setting(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("250x150")
        self.title("Настройки")
        self.scaling_label = CTkLabel(self, text="UI Scaling:", anchor="w", font=("Times", 20))
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = CTkOptionMenu(self, values=["50","60","70","80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event, width = 200)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(new_scaling_float)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)

class WidgetName(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

class FloatSpinbox(CTkFrame):
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

        self.subtract_button = CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, str(float(def_value)))
        self.entry.bind("<Any-KeyRelease>", self.control_type)
        self.add_button.bind('<Button-1>', self.control_type)
        self.subtract_button.bind('<Button-2>', self.control_type)

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, round(value, 3))
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        if float(self.entry.get()) > 0:
            try:
                value = float(self.entry.get()) - self.step_size
                self.entry.delete(0, "end")
                self.entry.insert(0, round(value, 3))
            except ValueError:
                return
            
    def control_type(self, button):
        """Проверяет вводимые данные"""
        try:
            data = float(self.entry.get())
            if data >= 0:
                self.entry.configure(fg_color=("white"))
            else:
                self.entry.configure(fg_color=("red"))
        except ValueError:
            self.entry.configure(fg_color=("red"))

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))
    
    def SpinboxConfigure(self, WidgetsState="normal"):
        if WidgetsState == "normal":
            self.entry.configure(state=WidgetsState, fg_color="white")
        else:
            self.entry.configure(state=WidgetsState, fg_color="black")

class RadiobuttonFrame(CTkFrame):
    def __init__(self, master, title, values, command):
        super().__init__(master)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.values = values
        self.title = title
        self.command = command
        self.radiobuttons = []
        self.variable = StringVar(value="")

        self.title = CTkLabel(self, text=self.title, fg_color="azure", corner_radius=6)
        self.title.grid(row=0, column=0,columnspan=3, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = CTkRadioButton(self, text=value, value=value, variable=self.variable, command=self.command)
            radiobutton.grid(row=1, column=i, padx=10, pady=(10, 0))
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)


class Lab1(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.toplevel_window_Lab1_setting = None

        self.Lab1_menu = Menu(self)
        self.Lab1_menu.add_command(label="Справка")
        self.Lab1_menu.add_command(label="Настройки", command=self.Lab1_Setting)
        self.config(menu=self.Lab1_menu)

        self.width= self.winfo_screenwidth()-100
        self.height= self.winfo_screenheight()/2
        self.geometry("%dx%d" % (self.width, self.height))
        self.title("Хищник-жертва")
        

        self.Formula = ""

        self.operating_mode_frame = RadiobuttonFrame(self,"Выбор режима",
                                                      values=["Лисы-Кролики",
                                                            "Лисы-Кролики-Мыши",
                                                            "Лисы-Кролики-Мыши-Совы"],
                                                        command=self.SwapMode)
        self.operating_mode_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="ew")
        self.operating_mode_frame.set("Лисы-Кролики")
        
        self.Lab1ParamFrame = Lab1_Param_Frame(self)
        self.Lab1ParamFrame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")

        self.Lab1ButtonFrame = Lab1_Button_Frame(self)
        self.Lab1ButtonFrame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.Lab1GraphFrame = Lab1_Graph_Frame(self)
        self.Lab1GraphFrame.grid(row=0, rowspan = 2, column=6, padx=10, pady=(10, 0), sticky="w")

        self.Lab1FormulaFrame = Lab1_Formula_Frame(self)
        self.Lab1FormulaFrame.grid(row=2, column=6, padx=10, pady=(10, 0), sticky="n")
        
        self.SwapMode()
        # self.Lab1WrittenBy = Lab1_WrittenBy_Frame(self)
        # self.Lab1WrittenBy.grid(row=3, column=0, columnspan = 2, padx=10, pady=(10, 0), sticky="w")
    def Lab1_Setting(self):
        if self.toplevel_window_Lab1_setting is None or not self.toplevel_window_Lab1_setting.winfo_exists():
            self.toplevel_window_Lab1_setting = Setting(self)
            self.toplevel_window_Lab1_setting.focus()
        else:
            self.toplevel_window_Lab1_setting.focus()

    def SwapMode(self):
        self.Lab1ParamFrame.spinbox_1.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_2.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_3.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_4.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_5.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_6.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_7.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_8.SpinboxConfigure("disabled")

        self.Lab1ParamFrame.spinbox_9.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_10.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_11.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_12.SpinboxConfigure("disabled")

        self.Lab1ParamFrame.spinbox_13.SpinboxConfigure("disabled")
        self.Lab1ParamFrame.spinbox_14.SpinboxConfigure("disabled")

        if self.operating_mode_frame.get() == "Лисы-Кролики":
            self.Lab1ParamFrame.spinbox_1.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_2.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_3.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_4.SpinboxConfigure("normal")

            self.Lab1ParamFrame.spinbox_9.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_10.SpinboxConfigure("normal")

            self.Lab1ParamFrame.spinbox_13.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_14.SpinboxConfigure("normal")
   
        elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши":
            self.Lab1ParamFrame.spinbox_1.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_2.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_3.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_4.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_5.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_6.SpinboxConfigure("normal")

            self.Lab1ParamFrame.spinbox_9.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_10.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_11.SpinboxConfigure("normal")

            self.Lab1ParamFrame.spinbox_13.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_14.SpinboxConfigure("normal")
            
        elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши-Совы":
            self.Lab1ParamFrame.spinbox_1.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_2.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_3.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_4.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_5.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_6.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_7.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_8.SpinboxConfigure("normal")

            self.Lab1ParamFrame.spinbox_9.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_10.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_11.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_12.SpinboxConfigure("normal")
        
            self.Lab1ParamFrame.spinbox_13.SpinboxConfigure("normal")
            self.Lab1ParamFrame.spinbox_14.SpinboxConfigure("normal")



    def Lab1_plot(self):
        self.G = self.Lab1ParamFrame.spinbox_0.get()
        self.t0 = 0.0
        self.tmax = 500
        self.num = 2000
        self.tspan = [self.t0, self.tmax]
        self.t = linspace(self.t0, self.tmax, self.num)  # the points of evaluation of solution                   # initial value
        
        self.h = (self.tmax - self.t0) / self.num

        if self.operating_mode_frame.get() == "Лисы-Кролики":
            try:
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
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
            # self.toolbar = NavigationToolbar2TkAgg(self.canvas5, self.frame_Graphics)
            # self.toolbar.update()
        elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши":
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * F\nПопуляция Лис: kfb * (R + M) * F - kfd * F\nПопуляция Мышей:kmb * (G + A * sin(omega * t) + B * sin(omega * t)) * M - self.kmd * F * M """
                self.Lab1FormulaFrame.title.configure(text=self.Formula)

                self.krb = self.Lab1ParamFrame.spinbox_1.get()
                self.krd = self.Lab1ParamFrame.spinbox_2.get()
                self.kfb = self.Lab1ParamFrame.spinbox_3.get()
                self.kfd = self.Lab1ParamFrame.spinbox_4.get()
                self.kmb = self.Lab1ParamFrame.spinbox_5.get()
                self.kmd = self.Lab1ParamFrame.spinbox_6.get()

                self.a = self.Lab1ParamFrame.spinbox_13.get()
                self.b = self.Lab1ParamFrame.spinbox_14.get()

                self.x0 = [self.Lab1ParamFrame.spinbox_9.get(), self.Lab1ParamFrame.spinbox_10.get(), self.Lab1ParamFrame.spinbox_11.get()]
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
                except AttributeError:
                    pass
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x[:,0], label ="Кролики")
                a.plot(self.t, self.x[:,1], label ="Лисы")
                a.plot(self.t, self.x[:,2], label ="Мыши")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab1GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши-Совы":
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * (F + O)\nПопуляция Лис: kfb * (R + M) * F - kfd * F\nПопуляция Мышей:kmb * (G + A * sin(omega * t) + B * sin(omega * t)) * M - self.kmd * F * M \nПопуляция Сов: kob * (R + M) * O - kod * O"""
                self.Lab1FormulaFrame.title.configure(text=self.Formula)

                self.krb = self.Lab1ParamFrame.spinbox_1.get()
                self.krd = self.Lab1ParamFrame.spinbox_2.get()
                self.kfb = self.Lab1ParamFrame.spinbox_3.get()
                self.kfd = self.Lab1ParamFrame.spinbox_4.get()
                self.kmb = self.Lab1ParamFrame.spinbox_5.get()
                self.kmd = self.Lab1ParamFrame.spinbox_6.get()
                self.kob = self.Lab1ParamFrame.spinbox_7.get()
                self.kod = self.Lab1ParamFrame.spinbox_8.get()

                self.a = self.Lab1ParamFrame.spinbox_13.get()
                self.b = self.Lab1ParamFrame.spinbox_14.get()
                
                self.x0 = [self.Lab1ParamFrame.spinbox_9.get(), 
                           self.Lab1ParamFrame.spinbox_10.get(),
                           self.Lab1ParamFrame.spinbox_11.get(), 
                           self.Lab1ParamFrame.spinbox_12.get()]
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
                except AttributeError:
                    pass
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x[:,0], label ="Кролики")
                a.plot(self.t, self.x[:,1], label ="Лисы")
                a.plot(self.t, self.x[:,2], label ="Мыши")
                a.plot(self.t, self.x[:,3], label ="Совы")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab1GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
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
        
    def Lab1_PhasePortrait(self):
        self.G = self.Lab1ParamFrame.spinbox_0.get()
        self.t0 = 0.0
        self.tmax = 500
        self.num = 4000
        self.tspan = [self.t0, self.tmax]
        self.t = linspace(self.t0, self.tmax, self.num)  # the points of evaluation of solution                   # initial value
        
        self.h = (self.tmax - self.t0) / self.num

        if self.operating_mode_frame.get() == "Лисы-Кролики":
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (G + A * sin(w * t) + B * sin(w * t)) * R - kdb * R * F\nПопуляция Лис: krf * R * F - kdf * F"""
                self.Lab1FormulaFrame.title.configure(text=self.Formula)
            
                self.krb = self.Lab1ParamFrame.spinbox_1.get()
                self.krd = self.Lab1ParamFrame.spinbox_2.get()
                self.kfb = self.Lab1ParamFrame.spinbox_3.get()
                self.kfd = self.Lab1ParamFrame.spinbox_4.get()
                self.a = self.Lab1ParamFrame.spinbox_13.get()
                self.b = self.Lab1ParamFrame.spinbox_14.get()

                self.x0 = [self.Lab1ParamFrame.spinbox_9.get(),
                            self.Lab1ParamFrame.spinbox_10.get()]
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
                a.plot(self.x[:,0], self.x[:,1], label ="X-S, Y-Myu")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab1GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
            # self.toolbar = NavigationToolbar2TkAgg(self.canvas5, self.frame_Graphics)
            # self.toolbar.update()
        elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши":
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * F\nПопуляция Лис: kfb * (R + M) * F - kfd * F\nПопуляция Мышей:kmb * (G + A * sin(omega * t) + B * sin(omega * t)) * M - self.kmd * F * M """
                self.Lab1FormulaFrame.title.configure(text=self.Formula)

                self.krb = self.Lab1ParamFrame.spinbox_1.get()
                self.krd = self.Lab1ParamFrame.spinbox_2.get()
                self.kfb = self.Lab1ParamFrame.spinbox_3.get()
                self.kfd = self.Lab1ParamFrame.spinbox_4.get()
                self.kmb = self.Lab1ParamFrame.spinbox_5.get()
                self.kmd = self.Lab1ParamFrame.spinbox_6.get()

                self.a = self.Lab1ParamFrame.spinbox_13.get()
                self.b = self.Lab1ParamFrame.spinbox_14.get()

                self.x0 = [self.Lab1ParamFrame.spinbox_9.get(),
                            self.Lab1ParamFrame.spinbox_10.get(),
                              self.Lab1ParamFrame.spinbox_11.get()]
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
                except AttributeError:
                    pass
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.x[:,0], self.x[:,1], label ="X-S, Y-Myu")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab1GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши-Совы":
            try:
                self.Formula = """Формулы расчётов:\nПопуляция зайцев: krb * (Ground + A * sin(omega * t) + B * sin(omega * t)) * R - krd * R * (F + O)\nПопуляция Лис: kfb * (R + M) * F - kfd * F\nПопуляция Мышей:kmb * (G + A * sin(omega * t) + B * sin(omega * t)) * M - self.kmd * F * M \nПопуляция Сов: kob * (R + M) * O - kod * O"""
                self.Lab1FormulaFrame.title.configure(text=self.Formula)

                self.krb = self.Lab1ParamFrame.spinbox_1.get()
                self.krd = self.Lab1ParamFrame.spinbox_2.get()
                self.kfb = self.Lab1ParamFrame.spinbox_3.get()
                self.kfd = self.Lab1ParamFrame.spinbox_4.get()
                self.kmb = self.Lab1ParamFrame.spinbox_5.get()
                self.kmd = self.Lab1ParamFrame.spinbox_6.get()
                self.kob = self.Lab1ParamFrame.spinbox_7.get()
                self.kod = self.Lab1ParamFrame.spinbox_8.get()

                self.a = self.Lab1ParamFrame.spinbox_13.get()
                self.b = self.Lab1ParamFrame.spinbox_14.get()
                
                self.x0 = [self.Lab1ParamFrame.spinbox_9.get(), 
                           self.Lab1ParamFrame.spinbox_10.get(),
                           self.Lab1ParamFrame.spinbox_11.get(), 
                           self.Lab1ParamFrame.spinbox_12.get()]
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
                except AttributeError:
                    pass
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.x[:,0], self.x[:,1], label ="X-S, Y-Myu")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab1GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
    def Lab1_NewWindow(self):
        self.G = self.Lab1ParamFrame.spinbox_0.get()
        self.t0 = 0.0
        self.tmax = 500
        self.num = 2000
        self.tspan = [self.t0, self.tmax]

        self.t = linspace(self.t0, self.tmax, self.num)  # the points of evaluation of solution                   # initial value
        self.h = (self.tmax - self.t0) / self.num
       

        if self.operating_mode_frame.get() == "Лисы-Кролики":
            self.krb = self.Lab1ParamFrame.spinbox_1.get()
            self.krd = self.Lab1ParamFrame.spinbox_2.get()
            self.kfb = self.Lab1ParamFrame.spinbox_3.get()
            self.kfd = self.Lab1ParamFrame.spinbox_4.get()
            self.a = self.Lab1ParamFrame.spinbox_13.get()
            self.b = self.Lab1ParamFrame.spinbox_14.get()

            self.x0 = [self.Lab1ParamFrame.spinbox_9.get(),
                        self.Lab1ParamFrame.spinbox_10.get()]
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

            self.num_steps = len(self.x[:, 0])
            fig = make_subplots(rows=1,cols=2)
            fig.add_trace(Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='Кролики'), row=1, col=1)
            fig.add_trace(Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='Лисы'), row=1, col=1)
            fig.add_trace(Scatter(x=self.x[:, 0], y=self.x[:, 1], mode='lines', name='X - Кролики\nY - Лисы'), row=1,col=2)

            self.frames=[]

            for self.i in range(0, len(self.x[:, 0]), 2):
                self.frames.append(Frame(name=str(self.i),
                                    data=[Scatter(x=self.t[:self.i+1], y=self.x[:self.i+1,0], mode='lines', name='Кролики'),
                                            Scatter(x=self.t[:self.i+1], y=self.x[:self.i+1,1], mode='lines', name='Лисы'),
                                            Scatter(x=self.x[:self.i+1, 0], y=self.x[:self.i+1, 1], mode='lines', name='X - Кролики\nY - Лисы')]))

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

            fig.update_layout(xaxis_title="t - Время", yaxis_title="X - Значение популяции",
                              updatemenus=[dict(direction=LEFT,
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
        if self.operating_mode_frame.get() == "Лисы-Кролики-Мыши":
            try:
                self.krb = self.Lab1ParamFrame.spinbox_1.get()
                self.krd = self.Lab1ParamFrame.spinbox_2.get()
                self.kfb = self.Lab1ParamFrame.spinbox_3.get()
                self.kfd = self.Lab1ParamFrame.spinbox_4.get()
                self.kmb = self.Lab1ParamFrame.spinbox_5.get()
                self.kmd = self.Lab1ParamFrame.spinbox_6.get()

                self.a = self.Lab1ParamFrame.spinbox_13.get()
                self.b = self.Lab1ParamFrame.spinbox_14.get()

                self.x0 = [self.Lab1ParamFrame.spinbox_9.get(),
                            self.Lab1ParamFrame.spinbox_10.get(),
                              self.Lab1ParamFrame.spinbox_11.get()]
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
                
                fig = make_subplots(rows=1,cols=2)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='Кролики'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='Лисы'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 2], mode='lines', name='Мыши'), row=1, col=1)
                fig.add_trace(Scatter(x=self.x[:, 0], y=self.x[:, 1], mode='lines', name='X - Кролики\nY - Лисы'), row=1,col=2)

                self.num_steps = len(self.x[:, 0])

                self.frames = []
                for self.i in range(0, len(self.x[:, 0]), 2):
                    self.frames.append(Frame(name=str(self.i),
                                                data=[Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 0],
                                                                 mode='lines', name='Кролики'),
                                                      Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 1],
                                                                 mode='lines', name='Лисы'),
                                                      Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 2],
                                                                 mode='lines', name='Мыши'),
                                                      Scatter(x=self.x[:self.i + 1, 0], y=self.x[:self.i + 1, 1], mode='lines', name='X - Кролики\nY - Лисы')]))
                                                      

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

                fig.update_layout(xaxis_title="t - Время", yaxis_title="X - Значение популяции",updatemenus=[dict(direction=LEFT,
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
                messagebox.showerror(title=None, message='Введите коэффициенты')
        if self.operating_mode_frame.get() == "Лисы-Кролики-Мыши-Совы":
            try: 
                self.krb = self.Lab1ParamFrame.spinbox_1.get()
                self.krd = self.Lab1ParamFrame.spinbox_2.get()
                self.kfb = self.Lab1ParamFrame.spinbox_3.get()
                self.kfd = self.Lab1ParamFrame.spinbox_4.get()
                self.kmb = self.Lab1ParamFrame.spinbox_5.get()
                self.kmd = self.Lab1ParamFrame.spinbox_6.get()
                self.kob = self.Lab1ParamFrame.spinbox_7.get()
                self.kod = self.Lab1ParamFrame.spinbox_8.get()

                self.a = self.Lab1ParamFrame.spinbox_13.get()
                self.b = self.Lab1ParamFrame.spinbox_14.get()
                
                self.x0 = [self.Lab1ParamFrame.spinbox_9.get(), 
                           self.Lab1ParamFrame.spinbox_10.get(),
                           self.Lab1ParamFrame.spinbox_11.get(), 
                           self.Lab1ParamFrame.spinbox_12.get()]
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

                fig = make_subplots(rows=1,cols=2)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='Кролики'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='Лисы'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 2], mode='lines', name='Мыши'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 3], mode='lines', name='Совы'), row=1, col=1)
                fig.add_trace(Scatter(x=self.x[:, 0], y=self.x[:, 1], mode='lines', name='X - Кролики\nY - Лисы'), row=1,col=2)

                self.num_steps = len(self.x[:, 0])

                self.frames = []
                for self.i in range(0, len(self.x[:, 0]), 2):
                    self.frames.append(Frame(name=str(self.i),
                                                data=[Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 0],
                                                                 mode='lines', name='Кролики'),
                                                      Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 1],
                                                                 mode='lines', name='Лисы'),
                                                      Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 2],
                                                                 mode='lines', name='Мыши'),
                                                      Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 3],
                                                                 mode='lines', name='Совы'),
                                                      Scatter(x=self.x[:self.i + 1, 0], y=self.x[:self.i + 1, 1], mode='lines', name='X - Кролики\nY - Лисы')]))

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

                fig.update_layout(xaxis_title="t - Время", yaxis_title="X - Значение популяции",updatemenus=[dict(direction=LEFT,
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
                messagebox.showerror(title=None, message='Введите коэффициенты')

    def Lab1_Metodichka(self):
        webbrowser.open_new(getcwd()+"/Методички/Методичка№1.pdf")


class Lab1_Graph_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class Lab1_Formula_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.title = CTkLabel(self, text="", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

class Lab1_WrittenBy_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class Lab1_Param_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = CTkLabel(self, text="Количество растительности:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.spinbox_0 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 1.2)
        self.spinbox_0.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Значение коэф. \nрождаемости кроликов:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.spinbox_1 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_1.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Значение коэф. \nсмертности кроликов:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=1, column=2, padx=10, pady=(10, 0))
        self.spinbox_2 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_2.grid(row=1, column=3, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Нач. значения\n популяции", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=1, column=4, padx=10, pady=(10, 0))
        self.spinbox_9 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 1)
        self.spinbox_9.grid(row=1, column=5, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Значение коэф. \nрождаемости лис:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.spinbox_3 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_3.grid(row=2, column=1, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Значение коэф. \nсмертности лис:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=2, column=2, padx=10, pady=(10, 0))
        self.spinbox_4 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_4.grid(row=2, column=3, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Нач. значения\n популяции", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=2, column=4, padx=10, pady=(10, 0))
        self.spinbox_10 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 2)
        self.spinbox_10.grid(row=2, column=5, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Значение коэф. \nрождаемости мыш:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=3, column=0, padx=10, pady=(10, 0))
        self.spinbox_5 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_5.grid(row=3, column=1, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Значение коэф. \nсмертности мыш:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=3, column=2, padx=10, pady=(10, 0))
        self.spinbox_6 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_6.grid(row=3, column=3, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Нач. значения\n популяции", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=3, column=4, padx=10, pady=(10, 0))
        self.spinbox_11 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 3)
        self.spinbox_11.grid(row=3, column=5, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Значение коэф. \nрождаемости сов:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=4, column=0, padx=10, pady=(10, 0))
        self.spinbox_7 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_7.grid(row=4, column=1, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Значение коэф. \nсмертности сов:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=4, column=2, padx=10, pady=(10, 0))
        self.spinbox_8 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_8.grid(row=4, column=3, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Нач. значения\n популяции", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=4, column=4, padx=10, pady=(10, 0))
        self.spinbox_12 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 4)
        self.spinbox_12.grid(row=4, column=5, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Коэф. антропогенного фактора:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.spinbox_13 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0)
        self.spinbox_13.grid(row=5, column=1, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Коэф. биотического фактора:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=5, column=2, padx=10, pady=(10, 0))
        self.spinbox_14 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0)
        self.spinbox_14.grid(row=5, column=3, padx=(0, 10), pady=(10, 10))
          
class Lab1_Button_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.button = CTkButton(self, text="Графики популяций", command=master.Lab1_plot, width=50, height=50, font=("Times", 14))
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.button = CTkButton(self, text="Фазовый портрет", command=master.Lab1_PhasePortrait, width=50, height=50, font=("Times", 14))
        self.button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.button = CTkButton(self, text="Методичка", command=master.Lab1_Metodichka, width=50, height=50, font=("Times", 14))
        self.button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.button = CTkButton(self, text="В отдельном окне", command=master.Lab1_NewWindow, width=50, height=50, font=("Times", 14))
        self.button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")


class Lab2(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.toplevel_window_Lab2_setting = None

        self.width= self.winfo_screenwidth()-100
        self.height= self.winfo_screenheight()/2
        self.geometry("%dx%d" % (self.width, self.height))
        self.title("Проточное моделирование микроорганизмов")

        self.Lab2_menu = Menu(self)
        self.Lab2_menu.add_command(label="Справка")
        self.Lab2_menu.add_command(label="Настройки", command=self.Lab2_Setting)
        self.config(menu=self.Lab2_menu)
        
        self.Formula = ""

        self.operating_mode_frame = RadiobuttonFrame(self, "Выбор режима", values=["Проточная модель Моно\n без субст. угнетения", 
                                                                                    "Проточная модель Моно\n с субст. угнетением",
                                                                                    "Непроточная модель Моно\n без субст. угнетения",
                                                                                    "Непроточная модель Моно\n с субст. угнетением"], 
                                                                                    command=self.SwapMode)
        self.operating_mode_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="ew")
        self.SwapMode()
        self.operating_mode_frame.set("Проточная модель Моно\n без субст. угнетения")
        self.Lab2ParamFrame = Lab2_Param_Frame(self)
        self.Lab2ParamFrame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="we")

        self.Lab2ButtonFrame = Lab2_Button_Frame(self)
        self.Lab2ButtonFrame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.Lab2GraphFrame = Lab2_Graph_Frame(self)
        self.Lab2GraphFrame.grid(row=0, rowspan = 2, column=6, padx=10, pady=(10, 0), sticky="w")

        self.Lab2FormulaFrame = Lab2_Formula_Frame(self)
        self.Lab2FormulaFrame.grid(row=2, column=6, padx=10, pady=(10, 0), sticky="n")
    
    def SwapMode(self):
        pass
        # self.Lab2ParamFrame.spinbox_1.SpinboxConfigure("disabled")
        # self.Lab2ParamFrame.spinbox_2.SpinboxConfigure("disabled")
        # self.Lab2ParamFrame.spinbox_3.SpinboxConfigure("disabled")
        # self.Lab2ParamFrame.spinbox_4.SpinboxConfigure("disabled")
        # self.Lab2ParamFrame.spinbox_5.SpinboxConfigure("disabled")
        # self.Lab2ParamFrame.spinbox_6.SpinboxConfigure("disabled")
        # self.Lab2ParamFrame.spinbox_7.SpinboxConfigure("disabled")
        # self.Lab2ParamFrame.spinbox_8.SpinboxConfigure("disabled")

        # if self.operating_mode_frame.get() == "Лисы-Кролики":
        #     self.Lab2ParamFrame.spinbox_1.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_2.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_3.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_4.SpinboxConfigure("normal")

        #     self.Lab2ParamFrame.spinbox_9.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_10.SpinboxConfigure("normal")

        #     self.Lab2ParamFrame.spinbox_13.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_14.SpinboxConfigure("normal")
   
        # elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши":
        #     self.Lab2ParamFrame.spinbox_1.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_2.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_3.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_4.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_5.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_6.SpinboxConfigure("normal")

        #     self.Lab2ParamFrame.spinbox_9.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_10.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_11.SpinboxConfigure("normal")

        #     self.Lab2ParamFrame.spinbox_13.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_14.SpinboxConfigure("normal")
            
        # elif self.operating_mode_frame.get() == "Лисы-Кролики-Мыши-Совы":
        #     self.Lab2ParamFrame.spinbox_1.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_2.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_3.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_4.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_5.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_6.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_7.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_8.SpinboxConfigure("normal")

        #     self.Lab2ParamFrame.spinbox_9.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_10.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_11.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_12.SpinboxConfigure("normal")
        
        #     self.Lab2ParamFrame.spinbox_13.SpinboxConfigure("normal")
        #     self.Lab2ParamFrame.spinbox_14.SpinboxConfigure("normal")

    def Lab2_Setting(self):
        if self.toplevel_window_Lab2_setting is None or not self.toplevel_window_Lab2_setting.winfo_exists():
            self.toplevel_window_Lab2_setting = Setting(self)
            self.toplevel_window_Lab2_setting.focus()
        else:
            self.toplevel_window_Lab2_setting.focus()
    
    def Lab2_plot(self): 
        self.t0 = 0.0
        self.tmax = 100
        self.num = 2000
        self.tspan = [self.t0, self.tmax]
        self.t = linspace(self.t0, self.tmax, self.num)  # the points of evaluation of solution                   # initial value
        
        self.h = (self.tmax - self.t0) / self.num

        if self.operating_mode_frame.get() == "Проточная модель Моно\n без субст. угнетения":
            try:
                self.Formula = """Формулы расчётов:\nБиомаса клеток:µ(S)*X-D`*X\nКонц.субстрата:-α*µ(S)*X+D`*(So-S)\nУдельная скорость роста: (µm*S)/(Km+S`)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
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
                a.plot(self.t, self.x[:,0], label ="X")
                a.plot(self.t, self.x[:,1], label ="S")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab2GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Проточная модель Моно\n с субст. угнетением":
            try:
                self.Formula = """Формулы расчётов:\nБиомаса клеток:x*µ(y)-D*x\nКонц.субстрата:-x*µ(y)+D*(yo-y)\nУдельная скорость роста: y/(1+y+γ*y^2)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.g = self.Lab2ParamFrame.spinbox_8.get()

                self.y0 = self.So/self.Ks
                self.D = self.Ds/self.Mym
                self.Gamma = self.g/self.Ks

                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
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
                except AttributeError:
                    pass
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x[:,0], label ="X")
                a.plot(self.t, self.x[:,1], label ="S")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab2GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Непроточная модель Моно\n без субст. угнетения":
            try:
                self.Formula = """Формулы расчётов:\nБиомаса клеток:µ(S)*X\nКонц.субстрата:-α*µ(S)*X\nУдельная скорость роста: (µm*S)/(Km+S`)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.g = self.Lab2ParamFrame.spinbox_8.get()

                self.y0 = self.So/self.Ks
                self.D = self.Ds/self.Mym
                self.Gamma = self.g/self.Ks
                        
                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.x = zeros((len(self.t), len(self.x0)))  # array for solution
                self.x[0, :] = self.x0
                self.i = 0
                while self.i < self.num - 1:

                    self.k1 = self.h * self.Fthree(self.t, self.x[self.i, :], self.i)

                    self.k2 = self.h * self.Fthree(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                    self.k3 = self.h * self.Fthree(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                    self.k4 = self.h * self.Fthree(self.t, self.x[self.i, :] + self.k3, self.i)

                    self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                    self.i = self.i + 1
                try:
                    self.canvas5.get_tk_widget().pack_forget()
                except AttributeError:
                    pass
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.t, self.x[:,0], label ="X")
                a.plot(self.t, self.x[:,1], label ="S")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab2GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Непроточная модель Моно\n с субст. угнетением":
                try:
                    self.Formula = """Формулы расчётов:\nБиомаса клеток:x*µ(y)\nКонц.субстрата:-x*µ(y)\nУдельная скорость роста: y/(1+y+γ*y^2)"""
                    self.Lab2FormulaFrame.title.configure(text=self.Formula)
                
                    self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                    self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                    self.a = self.Lab2ParamFrame.spinbox_2.get()
                    self.Ds = 0
                    self.So = self.Lab2ParamFrame.spinbox_4.get()



                    self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                                self.Lab2ParamFrame.spinbox_6.get(),
                                self.Lab2ParamFrame.spinbox_7.get()]
                    self.g = self.Lab2ParamFrame.spinbox_8.get()
                    self.y0 = self.So/self.Ks
                    self.D = self.Ds/self.Mym
                    self.Gamma = self.g/self.Ks
                            
                    self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                    self.x = zeros((len(self.t), len(self.x0)))  # array for solution
                    self.x[0, :] = self.x0
                    self.i = 0
                    while self.i < self.num - 1:

                        self.k1 = self.h * self.Ffour(self.t, self.x[self.i, :], self.i)

                        self.k2 = self.h * self.Ffour(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                        self.k3 = self.h * self.Ffour(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                        self.k4 = self.h * self.Ffour(self.t, self.x[self.i, :] + self.k3, self.i)

                        self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                        self.i = self.i + 1
                    try:
                        self.canvas5.get_tk_widget().pack_forget()
                    except AttributeError:
                        pass
                    self.fig = Figure(figsize=(4, 4))
                    a = self.fig.add_subplot(111)
                    a.plot(self.t, self.x[:,0], label ="X")
                    a.plot(self.t, self.x[:,1], label ="S")
                    a.grid(alpha=.6, linestyle='--')
                    a.legend(fontsize=12)

                    self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab2GraphFrame)
                    self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                    self.canvas5.draw()
                except:
                    messagebox.showerror(title=None, message='Введите коэффициенты')

    def Fone(self, t, x, i):
        return array([x[2]*x[0]-self.Ds*x[0],
                         -self.a*x[2]*x[0]+self.Ds*(self.So-x[1]),
                         (self.Mym*x[1])/(self.Ks+x[1])])  # start and end

    def Ftwo(self, t, x, i):
        self.XB = self.a*x[0]/self.Ks
        self.YB = x[1]/self.Ks
        return array([(self.XB*self.YB)/(1+self.YB+self.Gamma*self.YB**2)-self.D*self.XB,
                         -(self.XB*self.YB)/(1+self.YB+self.Gamma*self.YB**2)+self.D*(self.y0-self.YB),
                         self.YB/(1+self.YB+self.Gamma*self.YB**2)])
    
    def Fthree(self, t, x, i):
        return array([x[2]*x[0],
                         -self.a*x[2]*x[0],
                         (self.Mym*x[1])/(self.Ks+x[1])])


    def Ffour(self, t, x, i):
        self.XB = self.a*x[0]/self.Ks
        self.YB = x[1]/self.Ks
        return array([(self.XB*self.YB)/(1+self.YB+self.Gamma*self.YB**2)-self.D*self.XB,
                         -(self.XB*self.YB)/(1+self.YB+self.Gamma*self.YB**2)+self.D*(self.y0-self.YB),
                         self.YB/(1+self.YB+self.Gamma*self.YB**2)])
    def Lab2_PhasePortrait(self):
        self.t0 = 0.0
        self.tmax = 100
        self.num = 2000
        self.tspan = [self.t0, self.tmax]
        self.t = linspace(self.t0, self.tmax, self.num)  # the points of evaluation of solution                   # initial value
        
        self.h = (self.tmax - self.t0) / self.num

        if self.operating_mode_frame.get() == "Проточная модель Моно\n без субст. угнетения":
            try:
                self.Formula = """Формулы расчётов:\nБиомаса клеток:µ(S)*X-D`*X\nКонц.субстрата:-α*µ(S)*X+D`*(So-S)\nУдельная скорость роста: (µm*S)/(Km+S`)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
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
                a.plot(self.x[:,0], self.x[:,1], label = "x - X\ny- S")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab2GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Проточная модель Моно\n с субст. угнетением":
            try:
                self.Formula = """Формулы расчётов:\nБиомаса клеток:x*µ(y)-D*x\nКонц.субстрата:-x*µ(y)+D*(yo-y)\nУдельная скорость роста: y/(1+y+γ*y^2)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.g = self.Lab2ParamFrame.spinbox_8.get()

                self.y0 = self.So/self.Ks
                self.D = self.Ds/self.Mym
                self.Gamma = self.g/self.Ks

                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
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
                except AttributeError:
                    pass
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.x[:,0], self.x[:,1], label = "x - X\ny- S")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab2GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Непроточная модель Моно\n без субст. угнетения":
            try:
                self.Formula = """Формулы расчётов:\nБиомаса клеток:µ(S)*X\nКонц.субстрата:-α*µ(S)*X\nУдельная скорость роста: (µm*S)/(Km+S`)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.g = self.Lab2ParamFrame.spinbox_8.get()

                self.y0 = self.So/self.Ks
                self.D = self.Ds/self.Mym
                self.Gamma = self.g/self.Ks
                        
                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.x = zeros((len(self.t), len(self.x0)))  # array for solution
                self.x[0, :] = self.x0
                self.i = 0
                while self.i < self.num - 1:

                    self.k1 = self.h * self.Fthree(self.t, self.x[self.i, :], self.i)

                    self.k2 = self.h * self.Fthree(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                    self.k3 = self.h * self.Fthree(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                    self.k4 = self.h * self.Fthree(self.t, self.x[self.i, :] + self.k3, self.i)

                    self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                    self.i = self.i + 1
                try:
                    self.canvas5.get_tk_widget().pack_forget()
                except AttributeError:
                    pass
                self.fig = Figure(figsize=(4, 4))
                a = self.fig.add_subplot(111)
                a.plot(self.x[:,0], self.x[:,1], label = "x - X\ny- S")
                a.grid(alpha=.6, linestyle='--')
                a.legend(fontsize=12)

                self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab2GraphFrame)
                self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                self.canvas5.draw()
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        elif self.operating_mode_frame.get() == "Непроточная модель Моно\n с субст. угнетением":
                try:
                    self.Formula = """Формулы расчётов:\nБиомаса клеток:x*µ(y)\nКонц.субстрата:-x*µ(y)\nУдельная скорость роста: y/(1+y+γ*y^2)"""
                    self.Lab2FormulaFrame.title.configure(text=self.Formula)

                    self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                    self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                    self.a = self.Lab2ParamFrame.spinbox_2.get()
                    self.Ds = 0
                    self.So = self.Lab2ParamFrame.spinbox_4.get()



                    self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                                self.Lab2ParamFrame.spinbox_6.get(),
                                self.Lab2ParamFrame.spinbox_7.get()]
                    self.g = self.Lab2ParamFrame.spinbox_8.get()
                    self.y0 = self.So/self.Ks
                    self.D = self.Ds/self.Mym
                    self.Gamma = self.g/self.Ks
                            
                    self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                    self.x = zeros((len(self.t), len(self.x0)))  # array for solution
                    self.x[0, :] = self.x0
                    self.i = 0
                    while self.i < self.num - 1:

                        self.k1 = self.h * self.Ffour(self.t, self.x[self.i, :], self.i)

                        self.k2 = self.h * self.Ffour(self.t, self.x[self.i, :] + self.k1 / 2, self.i)

                        self.k3 = self.h * self.Ffour(self.t, self.x[self.i, :] + self.k2 / 2, self.i)

                        self.k4 = self.h * self.Ffour(self.t, self.x[self.i, :] + self.k3, self.i)

                        self.x[self.i + 1, :] = self.x[self.i, :] + 1 / 6 * (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)
                        self.i = self.i + 1
                    try:
                        self.canvas5.get_tk_widget().pack_forget()
                    except AttributeError:
                        pass
                    self.fig = Figure(figsize=(4, 4))
                    a = self.fig.add_subplot(111)
                    a.plot(self.x[:,0], self.x[:,1], label = "x - X\ny- S")
                    a.grid(alpha=.6, linestyle='--')
                    a.legend(fontsize=12)

                    self.canvas5 = FigureCanvasTkAgg(self.fig, master = self.Lab2GraphFrame)
                    self.canvas5.get_tk_widget().pack(side = TOP, fill= BOTH, expand=YES)
                    self.canvas5.draw()
                except:
                    messagebox.showerror(title=None, message='Введите коэффициенты')


    def Lab2_NewWindow(self):
        self.t0 = 0.0
        self.tmax = 100
        self.num = 2000
        self.tspan = [self.t0, self.tmax]

        self.t = linspace(self.t0, self.tmax, self.num)  # the points of evaluation of solution                   # initial value
        self.h = (self.tmax - self.t0) / self.num
       

        if self.operating_mode_frame.get() == "Проточная модель Моно\n без субст. угнетения":
            try:
                self.Formula = """Формулы расчётов:\nБиомаса клеток:µ(S)*X-D`*X\nКонц.субстрата:-α*µ(S)*X+D`*(So-S)\nУдельная скорость роста: (µm*S)/(Km+S`)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
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

                self.num_steps = len(self.x[:, 0])
                fig = make_subplots(rows=1,cols=2)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='X-Биомасса'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='S-Субстрат'), row=1, col=1)
                fig.add_trace(Scatter(x=self.x[:, 0], y=self.x[:, 1], mode='lines', name='x - X\ny - S'), row=1,col=2)

                self.frames=[]

                for self.i in range(0, len(self.x[:, 0]), 2):
                    self.frames.append(Frame(name=str(self.i),
                                        data=[Scatter(x=self.t[:self.i+1], y=self.x[:self.i+1,0], mode='lines', name='X-Биомасса'),
                                                Scatter(x=self.t[:self.i+1], y=self.x[:self.i+1,1], mode='lines', name='S-Субстрат'),
                                                Scatter(x=self.x[:self.i+1, 0], y=self.x[:self.i+1, 1], mode='lines', name='x - X\ny - S')]))

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

                fig.update_layout(xaxis_title="t - Время", yaxis_title="X - Значение",
                                updatemenus=[dict(direction=LEFT,
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
            except:
                messagebox.showerror(title=None, message='Введите коэффициенты')
        if self.operating_mode_frame.get() == "Проточная модель Моно\n с субст. угнетением":
            try:
                self.Formula = """Формулы расчётов:\nБиомаса клеток:x*µ(y)-D*x\nКонц.субстрата:-x*µ(y)+D*(yo-y)\nУдельная скорость роста: y/(1+y+γ*y^2)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.g = self.Lab2ParamFrame.spinbox_8.get()

                self.y0 = self.So/self.Ks
                self.D = self.Ds/self.Mym
                self.Gamma = self.g/self.Ks

                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
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
                
                fig = make_subplots(rows=1,cols=2)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='X-Биомасса'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='S-Субстрат'), row=1, col=1)
                fig.add_trace(Scatter(x=self.x[:, 0], y=self.x[:, 1], mode='lines', name='x - X\ny - S'), row=1,col=2)

                self.num_steps = len(self.x[:, 0])

                self.frames = []
                for self.i in range(0, len(self.x[:, 0]), 2):
                    self.frames.append(Frame(name=str(self.i),
                                                data=[Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 0],
                                                                 mode='lines', name='X-Биомасса'),
                                                      Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 1],
                                                                 mode='lines', name='S-Субстрат'),
                                                      Scatter(x=self.x[:self.i + 1, 0], y=self.x[:self.i + 1, 1], mode='lines', name='x - X\ny - S')]))
                                                      

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

                fig.update_layout(xaxis_title="t - Время", yaxis_title="X - Значение популяции",updatemenus=[dict(direction=LEFT,
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
                messagebox.showerror(title=None, message='Введите коэффициенты')
        if self.operating_mode_frame.get() == "Непроточная модель Моно\n без субст. угнетения":
            try: 
                self.Formula = """Формулы расчётов:\nБиомаса клеток:µ(S)*X\nКонц.субстрата:-α*µ(S)*X\nУдельная скорость роста: (µm*S)/(Km+S`)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = self.Lab2ParamFrame.spinbox_3.get()
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.g = self.Lab2ParamFrame.spinbox_8.get()

                self.y0 = self.So/self.Ks
                self.D = self.Ds/self.Mym
                self.Gamma = self.g/self.Ks
                        
                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
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

                fig = make_subplots(rows=1,cols=2)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='X-Биомасса'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='S-Субстрат'), row=1, col=1)
                fig.add_trace(Scatter(x=self.x[:, 0], y=self.x[:, 1], mode='lines', name='x - X\ny - S'), row=1,col=2)

                self.num_steps = len(self.x[:, 0])

                self.frames = []
                for self.i in range(0, len(self.x[:, 0]), 2):
                    self.frames.append(Frame(name=str(self.i),
                                                data=[Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 0],
                                                                 mode='lines', name='X-Биомасса'),
                                                      Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 1],
                                                                 mode='lines', name='S-Субстрат'),
                                                      Scatter(x=self.x[:self.i + 1, 0], y=self.x[:self.i + 1, 1], mode='lines', name='x - X\ny - S')]))
                                                      
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

                fig.update_layout(xaxis_title="t - Время", yaxis_title="X - Значение популяции",updatemenus=[dict(direction=LEFT,
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
                messagebox.showerror(title=None, message='Введите коэффициенты')

        if self.operating_mode_frame.get() == "Непроточная модель Моно\n c субст. угнетением":
            try: 
                self.Formula = """Формулы расчётов:\nБиомаса клеток:x*µ(y)\nКонц.субстрата:-x*µ(y)\nУдельная скорость роста: y/(1+y+γ*y^2)"""
                self.Lab2FormulaFrame.title.configure(text=self.Formula)
            
                self.Mym = self.Lab2ParamFrame.spinbox_0.get()
                self.Ks = self.Lab2ParamFrame.spinbox_1.get()
                self.a = self.Lab2ParamFrame.spinbox_2.get()
                self.Ds = 0
                self.So = self.Lab2ParamFrame.spinbox_4.get()



                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                            self.Lab2ParamFrame.spinbox_6.get(),
                            self.Lab2ParamFrame.spinbox_7.get()]
                self.g = self.Lab2ParamFrame.spinbox_8.get()
                self.y0 = self.So/self.Ks
                self.D = self.Ds/self.Mym
                self.Gamma = self.g/self.Ks
                        
                self.x0 = [self.Lab2ParamFrame.spinbox_5.get(),
                        self.Lab2ParamFrame.spinbox_6.get(),
                        self.Lab2ParamFrame.spinbox_7.get()]
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

                fig = make_subplots(rows=1,cols=2)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 0], mode='lines', name='X-Биомасса'), row=1, col=1)
                fig.add_trace(Scatter(x=self.t, y=self.x[:, 1], mode='lines', name='S-Субстрат'), row=1, col=1)
                fig.add_trace(Scatter(x=self.x[:, 0], y=self.x[:, 1], mode='lines', name='x - X\ny - S'), row=1,col=2)

                self.num_steps = len(self.x[:, 0])

                self.frames = []
                for self.i in range(0, len(self.x[:, 0]), 2):
                    self.frames.append(Frame(name=str(self.i),
                                                data=[Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 0],
                                                                 mode='lines', name='X-Биомасса'),
                                                      Scatter(x=self.t[:self.i + 1], y=self.x[:self.i + 1, 1],
                                                                 mode='lines', name='S-Субстрат'),
                                                      Scatter(x=self.x[:self.i + 1, 0], y=self.x[:self.i + 1, 1], mode='lines', name='x - X\ny - S')]))
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

                fig.update_layout(xaxis_title="t - Время", yaxis_title="X - Значение популяции",updatemenus=[dict(direction=LEFT,
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
                messagebox.showerror(title=None, message='Введите коэффициенты')

class Lab2_Graph_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class Lab2_Formula_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.title = CTkLabel(self, text="", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

class Lab2_WrittenBy_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class Lab2_Param_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = CTkLabel(self, text="Максимальная скорость роста:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.spinbox_0 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.9)
        self.spinbox_0.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Значение коэф. Ks:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.spinbox_1 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.25)
        self.spinbox_1.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Значение экономического коэф.:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=1, column=2, padx=10, pady=(10, 0))
        self.spinbox_2 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_2.grid(row=1, column=3, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Значение скорости потока(разбавления):", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.spinbox_3 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.75)
        self.spinbox_3.grid(row=2, column=1, padx=(0, 10), pady=(10, 10))
        self.title = CTkLabel(self, text="Значение конц. субстрата\nпоступающего в культиватор:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=2, column=2, padx=10, pady=(10, 0))
        self.spinbox_4 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_4.grid(row=2, column=3, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Начальные значения\nX-концентрацию биомассы микроорганизмов\nµ-удельная скорость роста биомассы\nS-субстрат:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=3, column=0, padx=10, pady=(10, 0))
        self.spinbox_5 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_5.grid(row=3, column=1, padx=(0, 10), pady=(10, 10))
        self.spinbox_6 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_6.grid(row=3, column=2, padx=(0, 10), pady=(10, 10))
        self.spinbox_7 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_7.grid(row=3, column=3, padx=(0, 10), pady=(10, 10))

        self.title = CTkLabel(self, text="Значение коэф. g:", fg_color="azure", corner_radius=6, font=("Times", 14))
        self.title.grid(row=4, column=0, padx=10, pady=(10, 0))
        self.spinbox_8 = FloatSpinbox(self, width=150, step_size=0.05, def_value = 0.2)
        self.spinbox_8.grid(row=4, column=1, padx=(0, 10), pady=(10, 10))
               
class Lab2_Button_Frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.button = CTkButton(self, text="Графики популяций", command=master.Lab2_plot, width=50, height=50, font=("Times", 14))
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.button = CTkButton(self, text="Фазовый портрет", command=master.Lab2_PhasePortrait, width=50, height=50, font=("Times", 14))
        self.button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.button = CTkButton(self, text="Методичка", command=master.Lab1_Metodichka, width=50, height=50, font=("Times", 14))
        self.button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.button = CTkButton(self, text="В отдельном окне", command=master.Lab2_NewWindow, width=50, height=50, font=("Times", 14))
        self.button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")


app = Main()
app.mainloop()