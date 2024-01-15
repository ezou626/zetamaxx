import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import tkinter.ttk as ttk

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def validate_input(string):
        return string == "" or string.isdigit() #check digits

class Menu(tk.Frame):
    def __init__(self, parent: tk.Tk, data: pd.DataFrame):
        tk.Frame.__init__(self, parent)
        self.data = data
        
        self.score_entry = tk.Entry(self, width=25)
        callback = self.parent.register(validate_input)
        self.score_entry.config(validate = 'key', validatecommand = (callback, '%P'))
        self.score_entry.grid(ipady=3, column = 1, row = 1)
        
        self.seconds_entry = ttk.Combobox(self, values = [30, 60, 120, 300, 600])
        self.seconds_entry.current(2)
        self.seconds_entry.grid(column = 2, row = 1)
        
        self.default_entry = ttk.Combobox(self, values = [True, False])
        self.default_entry.current(1)
        self.default_entry.grid(column = 3, row = 1)

class Chart(tk.Frame):
    def __init__(self, parent: tk.Tk, data: pd.DataFrame):
        tk.Frame.__init__(self, parent)
        self.data = data

        x = pd.date_range('2018-11-03', '2019-03-20')
        y = np.arange(len(x))
        
        self.data['Timestamp'] = x
        self.data['Score'] = y
        
        figure = plt.figure(1)
        
        plt.plot(self.data['Timestamp'], self.data['Score'])
        plt.xticks(rotation=45)
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
        
        scatter = FigureCanvasTkAgg(figure, self)
        scatter.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    
class DataWrapper():
    def __init__(self):
        self.data: pd.DataFrame = pd.read_csv('data.tsv', sep='\t')
        
        #correct to empty if no/bad data
        standard_columns = set(['Timestamp', 'Score', 'Seconds', 'Default'])
        if len(standard_columns.intersection(self.data.columns)) != 4:
            self.data = pd.DataFrame({
                'Timestamp': pd.Series(dtype='datetime64[ns]'),
                'Score': pd.Series(dtype='int'),
                'Seconds': pd.Series(dtype='int'),
                'Default': pd.Series(dtype='bool')
            })
            
    def add_point(self, timestamp, score, seconds, default):
        new_row = {
            'Timestamp': timestamp,
            'Score': score,
            'Seconds': seconds,
            'Default': default
        }
        self.data = self.data.append(new_row, ignore_index=True)
    
    def get_data(self):
        """
        TODO: Add support for other settings
        Returns:
            (pd.Series, pd.Series): (timestamps, scores)
        """
        return self.data['Timestamp'], self.data['Score']
        

class App(tk.Tk):
    """Wrapper window for application
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.state('zoomed') #fullscreen
        self.protocol("WM_DELETE_WINDOW", self.quit) #end process on close
        
        self.data: DataWrapper = DataWrapper()
        
        #chart
        self.chart = Chart(self, self.data)
        self.chart.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        #menu
        self.menu = Menu(self, self.data)
        self.menu.pack(fill=tk.X, expand=True)
        
        #add button
        self.submit_button = tk.Button(self, text = 'Add Result', )
        self.submit_button.pack(pady=10, expand=True)

#runs the app
if __name__ == "__main__":
    app = App()
    app.mainloop()