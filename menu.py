from chart import Chart
from containers import DataContainer

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showwarning

from datetime import datetime

class EditScoresMenu(tk.Frame):
    """Menu to add scores"""
    
    def __init__(self, parent: tk.Frame, window: tk.Tk, chart: Chart, 
                 data_container: DataContainer):
        """Constructs the widget to edit scores

        Args:
            parent (tk.Frame): parent frame
            window (tk.Tk): parent window to register command
            chart (Chart): application chart
            data_container (DataContainer): wrapper class for data
        """
        tk.Frame.__init__(self, parent)
        self.data_container = data_container
        self.chart = chart
        
        self.score_entry = tk.Entry(self, width=25)
        callback = window.register(self.validate_input) #might smell
        self.score_entry.config(validate = 'key', validatecommand = (callback, '%P'))
        self.score_entry.grid(ipady=3, column = 1, row = 1)
        
        self.seconds_entry = ttk.Combobox(self, values = [30, 60, 120, 300, 600])
        self.seconds_entry.current(2)
        self.seconds_entry.grid(column = 2, row = 1)
        
        self.default_entry = ttk.Combobox(self, values = [True, False])
        self.default_entry.current(0)
        self.default_entry.grid(column = 3, row = 1)
        
        self.add_button = tk.Button(self, text = 'Add Score', command = self.add_score)
        self.add_button.grid(column = 4, row = 1)
        
        self.remove_button = tk.Button(self, text = 'Remove Score', command = self.remove_score)
        self.remove_button.grid(column = 5, row = 1)
        
    def add_score(self):
        """Adds new score to data and refreshes chart

        """
        score = int(self.score_entry.get()) #guaranteed to be integer or empty
        if score == "":
            showwarning('Invalid Score', 'Please Enter a Score')
            return
        time = datetime.now()
        seconds = int(self.seconds_entry.get()) #guaranteed to be integer and not empty
        default = bool(self.default_entry.get()) #guaranteed to be boolean and not empty
        #print(score, time, seconds, default)
        
        self.data_container.add_point(time, score, seconds, default)
        
        x, y, limits = self.data_container.get_data()
        self.chart.update_chart(x, y, limits = limits)
        
    @staticmethod
    def validate_input(string):
        """Checks if the string is entirely composed of digits

        Args:
            string (str): string to be checked

        Returns:
            bool: True if is digits, False otherwise
        """
        return string == "" or string.isdigit()
    
    def remove_score(self):
        """Removes the last score added (undo)"""
        row = None
        if not self.data_container.has_last():
            return
        row = self.data_container.remove_last()
        
        x, y, limits = self.data_container.get_data()
        self.chart.update_chart(x, y, limits = limits)

class DataDisplayMenu(tk.Frame):
    pass

class Menu(tk.Frame):
    """Menu widget to contain all of the controls for the chart and data

    Stores references to Chart and DataContainer to consume their APIs
    """
    def __init__(self, parent: tk.Tk, chart: Chart, data_container: DataContainer):
        """Constructs the Menu widget

        Args:
            parent (tk.Tk): parent window
            chart (Chart): application chart
            data_container (DataContainer): wrapper class for data
        """
        tk.Frame.__init__(self, parent)
        self.data_container = data_container
        self.chart = chart
        
        x, y, limits = self.data_container.get_data()
        self.chart.update_chart(x, y, limits = limits)
        
        #edit scores menu
        self.edit_score_menu = EditScoresMenu(self, parent, chart, data_container)
        self.edit_score_menu.pack()
        
        # #data display menu
        # self.data_display_menu = DataDisplayMenu(self, parent, chart, data_container)
        # self.data_display_menu.pack()