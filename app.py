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
        self.protocol("WM_DELETE_WINDOW", self.quit) #end process on close
        self.title("Zetamaxx")
        self.wm_title("Zetamaxx")
        
        photo = tk.PhotoImage(file = 'icon.png')
        self.iconphoto(False, photo)
        self.wm_iconphoto(False, photo)
        
        text_frame = tk.Frame(self)
        data_container = DataContainer()
        chart = Chart(self)
        stats = Stats(text_frame)
        controller = Controller(chart, stats, data_container)
        menu = Menu(text_frame, controller)
        
        menu.grid(column = 1, row = 1, sticky='NSEW')
        stats.grid(column = 2, row = 1, sticky='NSEW')
        text_frame.grid_columnconfigure(1, weight=2)
        text_frame.grid_columnconfigure(2, weight=1)
        chart.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, 
                        ipadx=15, padx = 15)
        text_frame.pack(side = tk.TOP, fill=tk.X)
        
        self.state('zoomed')

if __name__ == "__main__":
    app = App()
    app.mainloop()