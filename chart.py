import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

class Chart(tk.Frame):
    """Chart widget
    
    Displays data and refreshes upon update
    """
    def __init__(self, parent: tk.Tk):
        """Initializes the chart, creating the figure and widget

        Args:
            parent (tk.Tk): parent widget
        """
        tk.Frame.__init__(self, parent)
        self.figure = plt.figure()
        self.scatter = FigureCanvasTkAgg(self.figure, self)
        self.scatter.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
    def update_chart(self, x, y, title: str = '', x_label: str = '', y_label: str = ''):
        self.figure.clear(keep_observers = True)
        plt.plot(x, y)
        plt.xticks(rotation = 45)
        # ax = plt.gca()
        # ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        self.scatter.draw_idle()

#testing if the update method works as intended
if __name__ == '__main__':
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", root.quit)
    chart = Chart(root)
    chart.pack()
    button = tk.Button(root, text = 'Add', command = lambda: chart.update_chart(range(5), range(5)))
    button.pack()
    root.mainloop()