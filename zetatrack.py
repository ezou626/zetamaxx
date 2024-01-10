import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Chart(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        x = pd.date_range('2018-11-03', '2019-03-20')
        y = np.arange(len(x))
        
        self.data = pd.DataFrame({
            'Timestamp': pd.Series(dtype='datetime64[ns]'),
            'Score': pd.Series(dtype='int'),
            'Seconds': pd.Series(dtype='int'),
            'Default': pd.Series(dtype='bool')
        })
        
        self.data['Timestamp'] = x
        self.data['Score'] = y
        
        figure = plt.figure(1)
        
        plt.plot(self.data['Timestamp'], self.data['Score'])
        plt.xticks(rotation=45)
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
        
        scatter = FigureCanvasTkAgg(figure, self)
        scatter.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        
    def add_point(self):
        

class App(tk.Tk):
    """Wrapper window for application
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.state('zoomed') #fullscreen
        self.protocol("WM_DELETE_WINDOW", self.quit) #end process on close
        
        #add chart
        self.chart = Chart(self)
        self.chart.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#runs the app
if __name__ == "__main__":
    app = App()
    app.mainloop()