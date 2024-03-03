from visualization import Chart
from data_container import DataContainer
from controller import Controller
from get_timezone import local_tz, local_pytz
from pytz import utc

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showwarning

from datetime import datetime

class EditScoresMenu(tk.Frame):
    """Menu to add scores"""
    
    def __init__(self, parent: tk.Frame, window: tk.Tk, controller: Controller):
        """Constructs the widget to edit scores

        Args:
            parent (tk.Frame): parent frame
            window (tk.Tk): parent window to register command
            controller (Controller): object to control display
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # enter score
        self.score_entry = tk.Entry(self, width=25)
        callback = window.register(self.validate_input) #might smell
        self.score_entry.config(validate = 'key', validatecommand = (callback, '%P'))
        self.score_entry.grid(ipady=3, column = 1, row = 1)
        
        # enter time
        self.seconds_entry = ttk.Combobox(self, state="readonly", values = [30, 60, 120, 300, 600])
        self.seconds_entry.current(2)
        self.seconds_entry.grid(column = 2, row = 1)
        
        # enter setting
        self.default_entry = ttk.Combobox(self, state="readonly", values = [True, False])
        self.default_entry.current(0)
        self.default_entry.grid(column = 3, row = 1)
        
        # add score
        self.add_button = tk.Button(self, text = 'Add Score', command = self.add_score)
        self.add_button.grid(column = 4, row = 1)
        
        # remove score
        self.remove_button = tk.Button(self, text = 'Remove Score', command = self.remove_score)
        self.remove_button.grid(column = 5, row = 1)
        
    def add_score(self):
        """Adds new score to data and refreshes chart"""
        
        score = self.score_entry.get() #guaranteed to be integer or empty
        if score == "":
            showwarning('Invalid Score', 'Please Enter a Score')
            return
        local_dt = datetime.now(tz=local_tz)
        utc_dt = local_dt.astimezone(utc)
        time = utc_dt.replace(tzinfo=None)
        seconds = int(self.seconds_entry.get()) #guaranteed to be integer and not empty
        default = bool(self.default_entry.get()) #guaranteed to be boolean and not empty
        #print(score, time, seconds, default)
        
        self.controller.add_point(time, int(score), seconds, default)
        
    def remove_score(self):
        """Removes the last score added (undo)"""
        self.controller.remove_point()

    @staticmethod
    def validate_input(string):
        """Checks if the string is entirely composed of digits

        Args:
            string (str): string to be checked

        Returns:
            bool: True if is digits, False otherwise
        """
        return string == "" or string.isdigit()

class DataDisplayMenu(tk.Frame):
    """Menu to change display settings"""
    
    def __init__(self, parent: tk.Tk, controller: Controller):
        """Constructs the widget to edit scores

        Args:
            parent (tk.Frame): parent frame
            window (tk.Tk): parent window to register command
            controller (Controller): object to control display
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # time settings
        self.time_selection = ttk.Combobox(self, state="readonly",
                                           values = ['120s', 'Other', 'All'])
        self.time_selection.current(0)
        self.time_selection.bind("<<ComboboxSelected>>", self.update_display)
        self.time_selection.grid(column = 1, row = 1)
        
        # problem settings
        self.setting_selection = ttk.Combobox(self, state="readonly",
                                           values = ['Default', 'Not Default', 'All'])
        self.setting_selection.current(0)
        self.setting_selection.bind("<<ComboboxSelected>>", self.update_display)
        self.setting_selection.grid(column = 2, row = 1)
        
        # ratio settings
        self.ratio_selection = ttk.Combobox(self, state="readonly",
                                           values = ['Values', 'Ratio'])
        self.ratio_selection.current(0)
        self.ratio_selection.bind("<<ComboboxSelected>>", self.update_display)
        self.ratio_selection.grid(column = 3, row = 1)
        
    def update_display(self, event) -> None:
        time_to_bool = {
            '120s': True,
            'Other': False,
            'All': None
        }
        settings_to_bool = {
            'Default': True,
            'Not Default': False,
            'All': None
        }
        time = time_to_bool[self.time_selection.get()]
        settings = settings_to_bool[self.setting_selection.get()]
        ratio = True if self.ratio_selection.get() == 'Ratio' else False
        self.controller.set_display_options(time, settings, ratio)
        

class Menu(tk.Frame):
    """Menu widget to contain all of the controls for the chart and data

    Stores references to Chart and DataContainer to consume their APIs
    """
    def __init__(self, parent: tk.Tk, controller: Controller):
        """Constructs the Menu widget

        Args:
            parent (tk.Tk): parent window
            chart (Chart): application chart
            data_container (DataContainer): wrapper class for data
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        controller.update_displays()
        
        #edit scores menu
        self.edit_score_menu = EditScoresMenu(self, parent, controller)
        self.edit_score_menu.pack()
        
        # #data display menu
        self.data_display_menu = DataDisplayMenu(self, controller)
        self.data_display_menu.pack()