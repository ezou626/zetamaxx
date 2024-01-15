import tkinter as tk
import pandas as pd
import numpy as np
import tkinter.ttk as ttk

from chart import Chart
from datacontainer import DataContainer
from menu import Menu

class App(tk.Tk):
    """Wrapper window for application
    """
    def __init__(self):
        """Create the app window
        """
        tk.Tk.__init__(self)
        self.state('zoomed') #fullscreen
        self.protocol("WM_DELETE_WINDOW", self.quit) #end process on close
        self.title("Zetamaxx")
        self.wm_title("Zetamaxx")
        
        #data
        self.data_container = DataContainer()
        
        #chart
        self.chart = Chart(self)
        self.chart.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        #menu
        self.menu = Menu(self, self.chart, self.data_container)
        self.menu.pack(fill=tk.X, expand=True)

#runs the app
if __name__ == "__main__":
    app = App()
    app.mainloop()