import tkinter as tk

from visualization import Chart
from data_container import DataContainer
from controller import ChartController
from menu import Menu

class App(tk.Tk):
    """Wrapper window for application"""
    
    def __init__(self):
        """Create the app window"""
        
        tk.Tk.__init__(self)
        self.state('zoomed') #fullscreen
        self.protocol("WM_DELETE_WINDOW", self.quit) #end process on close
        self.title("Zetamaxx")
        self.wm_title("Zetamaxx")
        
        #data
        self.data_container = DataContainer()
        
        #chart
        self.chart = Chart(self)
        self.chart.pack(side=tk.TOP, fill=tk.BOTH, expand=True, ipadx=15, ipady=15)
        
        # chart controller
        self.chart_controller = ChartController(self.chart, self.data_container)
        
        #menu
        self.menu = Menu(self, self.chart_controller)
        self.menu.pack(fill=tk.X)

#runs the app
if __name__ == "__main__":
    app = App()
    app.mainloop()