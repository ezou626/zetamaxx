import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import datetime
matplotlib.use("TkAgg")

class Chart(tk.Frame):
    """Chart widget that displays data and refreshes upon update"""
    
    def __init__(self, parent: tk.Tk):
        """Initializes the chart, creating the figure and widget

        Args:
            parent (tk.Tk): parent widget
        """
        tk.Frame.__init__(self, parent)
        self.figure = plt.figure()
        self.scatter = FigureCanvasTkAgg(self.figure, self)
        self.scatter.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=5)
        
    def update_chart(self, x: pd.Series, y: pd.Series, limits: tuple[datetime.datetime, datetime.datetime],
                     title: str = 'Zetamac History', x_label: str = 'Date', y_label: str = 'Score'):
        """Updates the chart according to the data given

        Args:
            x (pd.Series): x coordinates in datetime
            y (pd.Series): y coordinates in int
            title (str, optional): title of the graph. Defaults to 'Zetamac History'.
            x_label (str, optional): title of the graph. Defaults to 'Date'.
            y_label (str, optional): title of graph. Defaults to 'Score'.
        """
        #plot new figure
        self.figure.clear(keep_observers = True)
        plt.plot(x, y, '-o')
        plt.xticks(rotation = 45)
        
        #get axes and set limits
        ax = plt.gca()
        ax.set_xlim(limits)
        # ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
        
        #line of best fit
        x = mdates.date2num(x)
        fit = np.polyfit(x, y, 1)
        line = np.poly1d(fit)
        test_x = np.linspace(x[0], x[-1], 100)
        dates = mdates.num2date(test_x)
        plt.plot(dates, line(test_x))
        
        #add labels
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        
        #draw figure
        self.scatter.draw_idle()
        
class Stats(tk.Frame):
    """Displays stats for the displayed data"""
    
    def __init__(self, parent):
        """Initializes the stats window, creating the figure and widget

        Args:
            parent (tk.Tk): parent widget
        """
        tk.Frame.__init__(self, parent)
        self.high = tk.Label(self)
        self.average = tk.Label(self)
        

#testing if the update method works as intended
if __name__ == '__main__':
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", root.quit)
    chart = Chart(root)
    chart.pack()
    button = tk.Button(root, text = 'Add', command = lambda: chart.update_chart(range(5), range(5)))
    button.pack()
    root.mainloop()