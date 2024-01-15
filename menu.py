from chart import Chart
from datacontainer import DataContainer

import tkinter as tk
import tkinter.ttk as ttk

class EditScoreMenu(tk.Frame):
    pass

class FocusOptionsMenu(tk.Frame):
    pass

class Menu(tk.Frame):
    """Menu widget to contain all of the controls for the chart and data

    Stores references to chart and data_container to consume their APIs
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
        
        self.score_entry = tk.Entry(self, width=25)
        callback = parent.register(self.validate_input) #might smell
        self.score_entry.config(validate = 'key', validatecommand = (callback, '%P'))
        self.score_entry.grid(ipady=3, column = 1, row = 1)
        
        self.seconds_entry = ttk.Combobox(self, values = [30, 60, 120, 300, 600])
        self.seconds_entry.current(2)
        self.seconds_entry.grid(column = 2, row = 1)
        
        self.default_entry = ttk.Combobox(self, values = [True, False])
        self.default_entry.current(1)
        self.default_entry.grid(column = 3, row = 1)
    
    @staticmethod
    def validate_input(string):
        return string == "" or string.isdigit()