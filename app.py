import tkinter as tk

from visualization import Chart, Stats
from data_container import DataContainer
from controller import Controller
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
        
        self.data_container = DataContainer()
        self.chart = Chart(self)
        self.stats = Stats(self)
        
        self.controller = Controller(self.chart, self.stats, self.data_container)
        
        self.menu = Menu(self, self.controller)
        
        self.menu.pack(fill=tk.X, ipadx=15, ipady=15, padx = 15, pady = 15)
        self.stats.pack(fill = tk.X, ipadx=15, ipady=15)
        self.chart.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, 
                        ipadx=15, padx = 15)

if __name__ == "__main__":
    app = App()
    app.mainloop()